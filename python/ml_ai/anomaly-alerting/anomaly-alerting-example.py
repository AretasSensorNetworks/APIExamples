import requests
from datetime import datetime
import numpy as np
import pandas as pd
import configparser
import math
import kde_model_utils as kmu
import websocket
import sys
import json
import collections
try:
    import thread
except ImportError:
    import _thread as thread
import time

config = configparser.ConfigParser()
config.read("config.ini")

API_URL = config['DEFAULT']['API_URL']

USERNAME = config['DEFAULT']['API_USERNAME']
PASSWORD = config['DEFAULT']['API_PASSWORD']
TARGET_LOCATION_ID = config['DEFAULT']['TARGET_LOCATION_ID']
TARGET_MACS = config['DEFAULT']['TARGET_MACS']

API_TOKEN = None

model = None


def check_probability(datum):

    # pick a "width" for the integral
    # which is essentially a bin width...
    # this is the "sensitivity" - the probabilities will become increasingly smaller
    # as the bin width shrinks
    pwidth = 10
    targetX = datum['data']
    pmin = math.floor(targetX - pwidth / 2)
    pmax = math.ceil(targetX + pwidth / 2)

    probability = kmu.get_probability(pmin, pmax, 1000, model)

    print("Probability of CO2 between {} and {}: {}".format(pmin, pmax, probability))


def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    # print(type(data))
    # check if it is an array, list, etc.
    if isinstance(data, collections.Sequence):
        for datum in data:
            if 'type' in datum:
                print("Received sensor data message:")
                print(datum)
                if datum['type'] == 181:
                    print("Got CO2 sensor data")
                    check_probability(datum)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("WEBSOCKET CLOSED")


def on_open(ws):
    # the aretas sensordataevents websocket-connection-example requires the first message
    # to be the location entity ID and the list of
    # entity (device) IDs you want to monitor
    # send the request for the location ID and associated entity addresses
    req_str = "{},{}".format(TARGET_LOCATION_ID, TARGET_MACS)
    ws.send(req_str)

    def run(*args):
        while True:
            time.sleep(30)
            ws.send("PING")

    thread.start_new_thread(run, ())


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

    url = API_URL + "sensordata/byrange"
    # now
    end = int(round(time.time() * 1000))
    # 8 hours of data
    start = end - (7 * 24 * 60 * 60 * 1000)

    # this is the "device" we're querying
    # 181 is CO2 sensor type
    mac: int = config['DEFAULT']['TARGET_MAC']
    response = requests.get(url + "?mac=" + str(mac) + "&begin=" + str(start) + "&end=" + str(
        end) + "&limit=10000000&downsample=false&movingAverage=true&windowSize=5&type=181",
                            headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(mac)})

    if response.status_code == 200:

        sensor_data = []

        json_response = json.loads(response.content.decode())

        for sensorDatum in json_response:

            formattedDatum = {'timestamp': datetime.utcfromtimestamp(sensorDatum.get("timestamp") / 1000),
                              'data': sensorDatum.get("data")}

            sensor_data.append(formattedDatum)

        df = pd.DataFrame(sensor_data)
        # df['data']
        sensorData = np.array(df['data'])
        sensorDataN = sensorData.reshape(len(sensorData), 1)

        model = kmu.kde_model_selection(sensorDataN)

        sensorDataMin = min(sensorDataN)
        sensorDataMax = max(sensorDataN)

        # create an array of ints in the range of the samples
        values = np.asarray([value for value in range(int(sensorDataMin - ((sensorDataMax - sensorDataMin) / 2)),
                                                      int(sensorDataMax + ((sensorDataMax - sensorDataMin) / 2)))])
        values = values.reshape(len(values), 1)

        # get the probabilities to chart against the histogram
        probabilities = model.score_samples(values)
        probabilities = np.exp(probabilities)

        print("Minimum Probability:{}".format(min(probabilities)))
        print("Maximum Probability:{}".format(max(probabilities)))

    else:
        print("Invalid response code:")
        print(response.status_code)
        print('\n')

if model is not None:

    # open the websocket and watch for messages
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://iot.aretas.ca/sensordataevents/" + API_TOKEN,
                                on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    # run it async so we don't block other processing
    def run(*args):
        ws.run_forever()
        print("run forever thread terminating")

    thread.start_new_thread(run, ())

    while True:
        try:
            # listen for exit events or do other processing
            time.sleep(10)
        except KeyboardInterrupt:
            print("Exiting, thank you bye")
            sys.exit()


