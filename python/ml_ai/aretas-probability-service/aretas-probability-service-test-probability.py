import requests
import time
import json
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


def now_ms():
    return int(time.time() * 1000)


# get an authorization token from the API
API_TOKEN = gettoken()

if API_TOKEN is None:
    print("Could not get access token!")
    exit()
else:

    url = API_URL + "probability/univariatehistoprobability"
    # now
    end = int(round(time.time() * 1000))
    # 2 days of data
    start = end - (30 * 24 * 60 * 60 * 1000)

    # this is the "device" we're querying
    macs = config['DEFAULT']['TARGET_MACS']

    macsToK = [int(x.strip()) for x in macs.split(",")]

    query_macs = ""
    for mac in macsToK:
        query_macs = query_macs + "&macs=" + str(mac)

    test_values = [-100.0, 1, 32, 35, 1000, 44.0034]

    query_test_values = ""
    for X in test_values:
        query_test_values = query_test_values + "&X={0}".format(X)

    # profile some humidity sensors and get the density of some values of X
    queryUrl = url + "?type=248&startTime=" + str(start) + "&endTime=" + str(end) + "&nBins=100" + query_macs + "&recordLimit=1000000" + query_test_values

    print(queryUrl)

    response = requests.get(queryUrl, headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(mac)})

    if response.status_code == 200:
        json_response = json.loads(response.content.decode())
        print(json_response)

    else:
        print("Invalid response code:")
        print(response.status_code)
        print('\n')

