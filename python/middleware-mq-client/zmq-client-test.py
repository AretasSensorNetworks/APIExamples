import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:8111")
socket.subscribe("")
while True:

    message = socket.recv()
    # do something with the received location data packet
    locationDatum = json.loads(message)
    print("%s" % locationDatum)
