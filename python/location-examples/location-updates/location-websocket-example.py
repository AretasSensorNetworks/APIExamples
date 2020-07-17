# example to demonstrate how to connect to the Aretas API and get live location tag data from a device in your account

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

import matplotlib.pyplot as plt
import matplotlib.animation as animation

config = configparser.ConfigParser()
config.read("config.ini")

API_URL = config['DEFAULT']['API_URL']
API_LOCATION_EVENTS_URL = config['DEFAULT']['API_LOCATION_EVENTS_URL']

USERNAME = config['DEFAULT']['API_USERNAME']
PASSWORD = config['DEFAULT']['API_PASSWORD']

TARGET_MAP_ID = config['DEFAULT']['TARGET_MAP_ID']
TARGET_TAG_IDS = config['DEFAULT']['TARGET_TAG_IDS']

# map of tag_positions
tag_positions = {}

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# placeholder for the plot data
xs = []
ys = []


# websocket-connection-example callback
def on_message(ws, message):

    global xs
    global ys

    # print(message)
    data = json.loads(message)

    # check if it is an array, list, etc.
    if isinstance(data, collections.Sequence):
        for datum in data:
            if 'uniqueId' in datum:

                # print("Received location data message:")
                tag_positions[datum['uniqueId']] = {'x': datum['centerPoint']['x'], 'y': datum['centerPoint']['y']}

                # for debugging
                print(tag_positions)

                # detect a "collision" event:
                if datum['isColliding'] is True:
                    print("COLLIDED!!")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("WEBSOCKET CLOSED")


def on_open(ws):
    # the aretas location websocket-connection-example requires one message to kick things off,
    # a comma separated list of target tag IDs prefixed by the building map ID
    req_str = "{},{}".format(TARGET_MAP_ID, TARGET_TAG_IDS)

    print(req_str)

    ws.send(req_str)

    # example of threaded run method (for keepalive or what have you if the socket needs it)
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


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    xs.clear()
    ys.clear()

    global tag_positions

    for key in tag_positions:
        xs.append(tag_positions[key]['x'])
        ys.append(tag_positions[key]['y'])

    # Draw x and y lists
    ax.clear()
    ax.scatter(xs, ys)


def main():

    global xs, ys

    # get an authorization token from the API
    API_TOKEN = gettoken()

    if API_TOKEN is None:
        print("Could not get access token!")
        exit()
    else:

        # enable this for really verbose trace from the websocket client
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp(API_LOCATION_EVENTS_URL + API_TOKEN,
                                    on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open

        # run it async so we don't block other processing
        def run(*args):
            ws.run_forever()
            print("run forever thread terminating")

        thread.start_new_thread(run, ())

        print("Main thread is still running")

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
        plt.show()

        while True:
            try:
                # listen for exit events or do other processing
                time.sleep(10)
            except KeyboardInterrupt:
                print("Exiting, thank you bye")
                sys.exit()


if __name__ == "__main__":
    main()
