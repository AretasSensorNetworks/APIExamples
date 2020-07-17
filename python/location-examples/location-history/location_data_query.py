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
def get_location_data_history(tag_id=None,
                              begin_ms=-1,
                              end_ms=-1,
                              record_limit=100000,
                              iqr_filter=False,
                              iqr_multi=10.0,
                              moving_average=False,
                              mv_window_size=1,
                              offset_data=False):

    global API_TOKEN

    if API_TOKEN is None:
        API_TOKEN = gettoken()

    if API_TOKEN is None:
        print("Could not get access token!")
        exit()
    else:

        url = API_URL + "locationreporthistory/byrange"

        str_iqr_bool = "true" if iqr_filter is True else "false"
        str_mv_bool = "true" if moving_average is True else "false"
        str_offset_data = "true" if offset_data is True else "false"

        response = requests.get(url + "?tagId=" + str(tag_id) +
                                "&begin=" + str(begin_ms) +
                                "&end=" + str(end_ms) +
                                "&limit=" + str(record_limit) +
                                "&iqrFilter=" + str_iqr_bool +
                                "&iqrMulti=" + str(iqr_multi) +
                                "&movingAverage=" + str_mv_bool +
                                "&windowSize=" + str(mv_window_size) +
                                "&offsetData=" + str_offset_data,
                                headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(tag_id)})

        if response.status_code == 200:

            sensor_data = []

            json_response = json.loads(response.content.decode())

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

