import configparser
import requests
import time
import json
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini")

API_URL = config['DEFAULT']['API_URL']

USERNAME = config['DEFAULT']['API_USERNAME']
PASSWORD = config['DEFAULT']['API_PASSWORD']

TARGET_MAC: int = config['DEFAULT']['TARGET_MAC']

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


# get some data from the API
def get_data():

    global API_TOKEN

    if API_TOKEN is None:
        API_TOKEN = gettoken()

    if API_TOKEN is None:
        print("Could not get access token!")
        exit()
    else:

        url = API_URL + "sensordata/byrange"
        # now
        end = now_ms()
        # 7 days of data
        start = end - (7 * 24 * 60 * 60 * 1000)

        response = requests.get(url + "?mac=" + str(TARGET_MAC) + "&begin=" + str(start) + "&end=" + str(end) +
                                "&limit=10000000&type=246&downsample=false&movingAverage=true&windowSize=5",
                                headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(TARGET_MAC)})

        if response.status_code == 200:

            sensor_data = []

            json_response = json.loads(response.content.decode())

            for sensorDatum in json_response:
                datum = {'timestamp': datetime.utcfromtimestamp(sensorDatum.get("timestamp") / 1000), 'data': sensorDatum.get("data")}

                sensor_data.append(datum)

            return sensor_data

        else:
            print("Invalid response code:")
            print(response.status_code)
            print('\n')
            return None
