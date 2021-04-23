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

sensor_type_metadata = None


# basic function to get an access token
def gettoken():
    api_response = requests.get(API_URL + "authentication/g?username=" + USERNAME + "&password=" + PASSWORD)
    if api_response.status_code >= 200:
        return api_response.content.decode()
    else:
        return None


# utility function to get the time in milliseconds
def now_ms():
    return int(time.time() * 1000)


# get the entity metadata object for that type
def get_entity_type_metadata_obj(type_target):

    global sensor_type_metadata

    if sensor_type_metadata is None:
        get_sensor_metadata()

    if sensor_type_metadata is not None:
        metadata_obj = [x for x in sensor_type_metadata if x["type"] == type_target]

    return metadata_obj


# get the type label for that entity type
def get_type_label(type_target):

    metadata_obj = get_entity_type_metadata_obj(type_target)

    if len(metadata_obj) > 0:
        ret = metadata_obj[0]["label"]
    else:
        ret = str(type_target)

    return ret


# utility function to get the sensor metadata from the API
def get_sensor_metadata():

    global API_TOKEN, API_URL, sensor_type_metadata

    # note that the sensor metadata api doesn't need authorization, but we can pass it anyway
    response = requests.get(API_URL + "sensortype/list", headers={"Authorization": "Bearer " + API_TOKEN})

    if response.status_code == 200:
        sensor_type_metadata = json.loads(response.content.decode())

        # print(sensor_type_metadata)


# returns an iterable "map" indexed by entity type, formatted for charting etc.
def get_map_formatted(raw_sensor_data):

    type_map = {}
    for datum in raw_sensor_data:

        type_dict = type_map.get(datum.get("type"))

        if type_dict is None:
            type_dict = []
            type_map[datum.get("type")] = type_dict

        # craft a datum more suitable for graphing etc.
        nice_datum = {'timestamp': datetime.utcfromtimestamp(datum.get("timestamp") / 1000), 'data': datum.get("data")}
        type_dict.append(nice_datum)

        # print(type_map)
    return type_map


# just return a plain list of the sensor data
def get_formatted(raw_sensor_data):

    ret = []

    for datum in raw_sensor_data:
        # craft a datum more suitable for graphing etc.
        nice_datum = {'timestamp': datetime.utcfromtimestamp(datum.get("timestamp") / 1000), 'data': datum.get("data")}
        ret.append(nice_datum)

    return ret


# get some data from the API. does not include ML derived indexes for now
# if the type_target is excluded then the query gets all the types for that mac
# the function returns an iterable "map" indexed by entity type
def query_sensor_data_basic(mac=None,
                            type_target=None,
                            begin_ms=-1,
                            end_ms=-1,
                            record_limit=100000,
                            iqr_filter=False,
                            iqr_multi=10.0,
                            moving_average=False,
                            mv_window_size=1,
                            moving_average_type=0,
                            offset_data=False,
                            downsample=False,
                            downsample_size=100):

    """Gets sensor data from the API
    Parameters
    ----------
    mac : int
        The entity id / mac address
    type_target: int
        The entity sub type (like temperature, relative humidity, index, etc)
    begin_ms : int
        The query start time in linux epoch milliseconds
    end_ms : int
        The query end time in linux epoch milliseconds
    record_limit : int, optional
        The maximum number of records to return in the query, before decimation and downsampling or indexes
    iqr_filter: bool, optional
        Apply an Inter-quartile range filter (outlier filter), if you set this to true,
        you should supply the iqr_multi parameter. the IQR filter is the first filter in the chain
    iqr_multi: float, optional
        This is the interquartile range multiple for the IQR filter (default is 10)
    moving_average: bool, optional
        Apply a moving average filter to the results the moving average filter is the LAST filter in the chain
        if you set this to True, you should also set the mv_window_size
    mv_window_size: float, optional
        The window size for the moving average filter (defaults to 1)
    moving_average_type: int, optional
        The moving average type (e.g. basic window or time based)
    offset_data: bool, optional
        If set to True, the query will be offset from the time the entity last reported
        (rather than the specified date). For example, if the sensor reported 8 hours ago, the start time
        will be shifted backwards by 8 hours and the end time will be shifted backwards by 8 hours
    downsample: bool, optional
        If set to True, the data will be downsampled with feature preservation - this means the results will
        likely *not* be temporally contiguous
    downsample_size: int, optional
        This is the maximum size/len of data to return from the API when downsampling is set to True
        (default is 100), change to suit your requirements

    Returns
    --------
    dict
        Returns a dict indexed by type if type_target is specified each dict entry is a list of ordered data
    list
        Returns a list if type_target is None - the list is a list of ordered data
    """

    global API_TOKEN

    if API_TOKEN is None:
        API_TOKEN = gettoken()

    if API_TOKEN is None:
        print("Could not get access token!")
        exit()
    else:

        url = API_URL + "sensordata/byrange"

        str_iqr_bool = "true" if iqr_filter is True else "false"
        str_mv_bool = "true" if moving_average is True else "false"
        str_offset_data = "true" if offset_data is True else "false"
        str_downsample_data = "true" if downsample is True else "false"

        query_uri = "?mac=" + str(mac) + \
                    "&begin=" + str(begin_ms) + \
                    "&end=" + str(end_ms) + \
                    "&limit=" + str(record_limit) + \
                    "&offsetData=" + str_offset_data

        if moving_average is not False and mv_window_size is not None:
            query_uri += "&movingAverage=" + str_mv_bool + \
                    "&windowSize=" + str(mv_window_size) + "&movingAverageType=" + str(moving_average_type)

        if iqr_filter is not False and iqr_multi is not None:
            query_uri += "&iqrFilter=" + str_iqr_bool + \
                        "&iqrMulti=" + str(iqr_multi)

        if downsample is not False and downsample_size is not None:
            query_uri += "&downsample=" + str_downsample_data + \
                        "&threshold=" + str(downsample_size)

        if type_target is not None:
            query_uri += "&type=" + str(type_target)

        print(query_uri)

        response = requests.get(url + query_uri,
                                headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(mac)})

        if response.status_code == 200:

            json_response = json.loads(response.content.decode())

            if type_target is None:
                return get_map_formatted(json_response)
            else:
                return get_formatted(json_response)

        else:
            print("Invalid response code from API:")
            print(response.status_code)
            print('\n')
            return None
