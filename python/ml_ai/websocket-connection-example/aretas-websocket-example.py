# example to demonstrate how to connect to the Aretas API and get live sensor data from a device in your account

import configparser
import requests
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

API_TOKEN = None

TARGET_LOCATION_ID = config['DEFAULT']['TARGET_LOCATION_ID']
TARGET_MACS = config['DEFAULT']['TARGET_MACS']


# websocket-connection-example callback
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


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("WEBSOCKET CLOSED")


def on_open(ws):
    # the aretas sensordataevents websocket-connection-example requires the first message to be the location entity ID and the list of
    # entity (device) IDs you want to monitor
    # send the request for the location ID and associated entity addresses
    req_str = "{},{}".format(TARGET_LOCATION_ID, TARGET_MACS)
    ws.send(req_str)

    # example of threaded run method (for keepalive or what have you)
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
    #         ws.send("PING")
    #     time.sleep(1)
    #     # ws.close()
    #     print("thread terminating")
    # thread.start_new_thread(run, ())


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
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.1.11:8080/sensordataevents/" + API_TOKEN,
                                on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    # run it async so we don't block other processing
    def run(*args):
        ws.run_forever()
        print("run forever thread terminating")

    thread.start_new_thread(run, ())

    print("Main thread is still running")

    while True:
        try:
            # listen for exit events or do other processing
            time.sleep(10)
        except KeyboardInterrupt:
            print("Exiting, thank you bye")
            sys.exit()
