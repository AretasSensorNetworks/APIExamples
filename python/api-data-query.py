import requests
import time
import json
from datetime import datetime
import plotly.graph_objs as go

import pandas as pd

API_URL = "https://iot.sensera-iot.com/rest/"

USERNAME="username"
PASSWORD="password"

API_TOKEN = None

# the device ID / mac of one of the devices in the account
mac: int = 0

def gettoken():
    response = requests.get(API_URL + "authentication/g?username=" + USERNAME + "&password=" + PASSWORD)
    if response.status_code >= 200 :
        return response.content.decode()
    else:
        return None

# get an authorization token from the API
API_TOKEN = gettoken()

if API_TOKEN is None:
    print("Could not get access token!")
    exit()
else:
# get the sensor type metadata
    sensorTypes = None
    response = requests.get(API_URL + "sensortype/list", headers={"Authorization" : "Bearer " + API_TOKEN})
    if response.status_code == 200:
        sensorTypes = json.loads(response.content.decode())
        # print(sensorTypes)

    url = API_URL + "sensordata/byrange"
# now
    end = int(round(time.time() * 1000))
# 8 hours of data
    start = end - (8 * 60 * 60 * 1000)

    response = requests.get(url + "?mac=" + str(mac) + "&begin=" + str(start) + "&end=" + str(end) + "&limit=10000000", headers={"Authorization" : "Bearer " + API_TOKEN, "X-AIR-Token" : str(mac)})
    if response.status_code == 200:
        json_response = json.loads(response.content.decode())

        typeMap = {}
        for datum in json_response:
            typeDict = typeMap.get(datum.get("type"))
            if typeDict is None:
                typeDict = []
                typeMap[datum.get("type")] = typeDict
            typeDatum = {'timestamp': datetime.utcfromtimestamp(datum.get("timestamp")/1000), 'data': datum.get("data")}
            typeDict.append(typeDatum)

        # print(typeMap)

        chartData = []

        for key in typeMap:

            df = pd.DataFrame(typeMap[key])

            if sensorTypes is not None:
                sensorTypeObj = [sensorType for sensorType in sensorTypes  if sensorType["type"] == key]

            if len(sensorTypeObj) > 0:
                label = sensorTypeObj[0]["label"]
            else:
                label = str(key)

            trace = go.Scatter(x=df['timestamp'], y=df['data'], mode='lines', name='Sensor: {}'.format(label))

            layout = go.Layout(title='Aretas API Sensor Data for MAC:{}'.format(mac), plot_bgcolor='rgb(230, 230,230)')
            chartData.append(trace)

        fig = go.Figure(chartData, layout=layout)

        # write to html file
        fig.write_html('sensor-data-export.html', auto_open=True)

    else:
        print("Invalid response code:")
        print(response.status_code)
        print('\n')
