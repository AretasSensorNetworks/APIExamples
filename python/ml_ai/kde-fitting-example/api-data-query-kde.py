import requests
import time
import json
from datetime import datetime
from matplotlib import pyplot
import plotly.graph_objs as go
import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import pandas as pd
import configparser

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
    # 8 hours of data
    start = end - (7 * 24 * 60 * 60 * 1000)

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
            sensorDataN = sensorData.reshape(len(sensorData), 1)

            # kernel_selection = ['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
            kernel_selection = ['gaussian', 'tophat', 'epanechnikov']

            # very basic estimate for best bandwidth selection
            grid = GridSearchCV(KernelDensity(), {'bandwidth': np.geomspace(0.1, 100, 20),
                                                  'kernel': kernel_selection}, cv=5)
            grid.fit(sensorDataN)
            bw = grid.best_params_

            print(bw)

            model = KernelDensity(bandwidth=bw['bandwidth'], kernel=bw['kernel'])
            model.fit(sensorDataN)

            print(model)

            sensorDataMin = min(sensorDataN)
            sensorDataMax = max(sensorDataN)

            # create an array of ints in the range of the samples
            values = np.asarray([value for value in range(int(sensorDataMin - ((sensorDataMax - sensorDataMin) / 2)),
                                                          int(sensorDataMax + ((sensorDataMax - sensorDataMin) / 2)))])
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
