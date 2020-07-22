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
def get_hourly_aggregation(mac, target_type, begin_ms, end_ms, offset_data=False, record_limit=100000):

    global API_TOKEN

    if API_TOKEN is None:
        API_TOKEN = gettoken()

    if API_TOKEN is None:
        print("Could not get access token!")
        exit()
    else:

        str_offset_data = "true" if offset_data is True else "false"

        url = API_URL + "timeseriesaggregation/hourly"

        response = requests.get(url + "?mac=" + str(mac) +
                                "&type=" + str(target_type) +
                                "&begin=" + str(begin_ms) +
                                "&end=" + str(end_ms) +
                                "&limit=" + str(record_limit) +
                                "&offsetData=" + str_offset_data,
                                headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(mac)})

        if response.status_code == 200:

            sensor_data = []

            json_response = json.loads(response.content.decode())

            print(json_response)

            for locationDatum in json_response:

                # only keep the required fields and convert the timestamp into something python likes
                datum = {'timestamp': datetime.utcfromtimestamp(locationDatum.get("timestamp") / 1000),
                         'x': locationDatum.get("x"),
                         'y': locationDatum.get("y"),
                         'z': locationDatum.get("z")}

                sensor_data.append(datum)

            return sensor_data

        else:
            print("Invalid response code:")
            print(response.status_code)
            print('\n')
            return None

