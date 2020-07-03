import requests
import time
import json
from datetime import datetime
from matplotlib import pyplot
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import configparser
import kde_model_utils as kmu

config = configparser.ConfigParser()
config.read("config.ini")

API_URL = config['DEFAULT']['API_URL']

USERNAME = config['DEFAULT']['API_USERNAME']
PASSWORD = config['DEFAULT']['API_PASSWORD']

API_TOKEN = None


# basic function to get an access token
def gettoken():
    api_response = requests.get(API_URL + "authentication/g?username=" + USERNAME + "&password=" + PASSWORD)
    if api_response.status_code >= 200:
        return api_response.content.decode()
    else:
        return None


def now_ms():
    return int(time.time() * 1000)


# get an authorization token from the API
API_TOKEN = gettoken()

if API_TOKEN is None:
    print("Could not get access token!")
    exit()
else:
    # this gets the sensor type metadata from the API (descriptions, codes, etc)
    sensorTypes = None
    response = requests.get(API_URL + "sensortype/list", headers={"Authorization": "Bearer " + API_TOKEN})
    if response.status_code == 200:
        sensorTypes = json.loads(response.content.decode())
        # print(sensorTypes)

    url = API_URL + "sensordata/byrange"
    # now
    end = int(round(time.time() * 1000))
    # 7 days of data
    start = end - (7 * 24 * 60 * 60 * 1000)

    startMs = now_ms()

    # this is the "device" we're querying
    mac: int = config['DEFAULT']['TARGET_MAC']
    response = requests.get(url + "?mac=" + str(mac) + "&begin=" + str(start) + "&end=" + str(
        end) + "&limit=10000000&downsample=false&movingAverage=true&windowSize=5",
                            headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(mac)})

    if response.status_code == 200:
        json_response = json.loads(response.content.decode())

        # sort the sensor data by type - if we do an aggregated query without specifying the type
        # we will get all of the sensor types associated with that mac
        typeMap = {}
        for datum in json_response:
            typeDict = typeMap.get(datum.get("type"))
            if typeDict is None:
                typeDict = []
                typeMap[datum.get("type")] = typeDict
            typeDatum = {'timestamp': datetime.utcfromtimestamp(datum.get("timestamp") / 1000),
                         'data': datum.get("data")}
            typeDict.append(typeDatum)

        chartData = []

        # chart and process  each sensor type separately
        for key in typeMap:

            df = pd.DataFrame(typeMap[key])

            # generate a label from the sensor metadata
            if sensorTypes is not None:
                sensorTypeObj = [sensorType for sensorType in sensorTypes if sensorType["type"] == key]

            if len(sensorTypeObj) > 0:
                label = sensorTypeObj[0]["label"]
            else:
                label = str(key)

            # df['data']
            sensorData = np.array(df['data'])

            print("Running KDE on {} samples".format(sensorData.size))

            sensorDataN = sensorData.reshape(len(sensorData), 1)

            model = kmu.kde_model_selection(sensorDataN)

            sensorDataMin = min(sensorDataN)
            sensorDataMax = max(sensorDataN)

            # create an array of ints in the range of the samples
            values = np.asarray([value for value in range(int(sensorDataMin - ((sensorDataMax - sensorDataMin) / 2)),
                                                          int(sensorDataMax + ((sensorDataMax - sensorDataMin) / 2)))])

            print(values)

            values = values.reshape(len(values), 1)

            # get the probabilities to chart against the histogram
            probabilities = model.score_samples(values)
            probabilities = np.exp(probabilities)

            trace = go.Scatter(x=df['timestamp'], y=df['data'], mode='lines', name='Sensor: {}'.format(label))

            layout = go.Layout(title='Aretas API Sensor Data for MAC:{}'.format(mac), plot_bgcolor='rgb(230, 230,230)')
            chartData.append(trace)

            pyplot.title(label + " Probability Fit")
            pyplot.hist(sensorDataN, bins=20, density=True)
            pyplot.plot(values[:], probabilities)

            pyplot.savefig(fname='{}.png'.format(key))

            pyplot.show()

        fig = go.Figure(chartData, layout=layout)

        # write to html file
        fig.write_html('sensor-data-export.html', auto_open=True)

    else:
        print("Invalid response code:")
        print(response.status_code)
        print('\n')
