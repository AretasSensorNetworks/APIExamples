# Aretas Nanotron Middleware MQ Client

The Aretas Nanotron Middleware allows you to connect to a nanoLES instance and get conditioned location data from the nanoLES instance. You can use the middleware in different ways:
1. REST API Update mode (Batch or Serial) for Edge or Cloud based applications - you can use the Aretas IoT Stack or implement your own endpoints
2. CSV Datalogging output - highspeed / flush on write or std write options for CSV logging
3. ZeroMQ Socket Mode - You can benefit from the various filters in the middleware and a slightly more lean connectivity protocol using zeromq implementation.

** Note that the ZeroMQ Socket Mode is only available in AretasNanotronBridge-0.1.9 or greater.

## ZMQ Info
ZeroMQ is a hyper efficient networking library / concurrency framwework that makes network connectivity and messaging a breeze. ZeroMQ easily scales beyond 10K msg/sec and has been tested in many implementations to *millions* of messages per second. If you haven't used or heard of ZeroMQ before check out the ZeroMQ web page: http://zguide.zeromq.org/

ZeroMQ has many platform implementations for C, C++, Java, Python, C#, Perl, NodeJS and more.

You can configure the TCP endpoints for the middleware in the AretasNanotronBridge config (.properties file). The default endpoints launched in the middleware include:

### Location Data Endpoint
Typically found at tcp://*:8111

This endpoint provides streaming conditioned location data packets in JSON format. 

e.g.:
`{"tagId":51020,"timestamp":1576378212240,"x":7.765174808619754,"y":3.612147359804452,"z":2.0,"blinkRateInterval":244}`

### Sensor Data Endpoint
Typically found at tcp://*:8110

This endpoint provides streaming sensor data packets in JSON format. The MAC/ID will match the tagId

e.g.:
`{"mac":51166,"timestamp":1576380255682,"type":245,"data":9.0}`

*Note that Aretas Sensor Data Packets are deserialized from the FNIN payload, which may contain stale data. Developers implementing injection of Aretas packets with FNIN should be aware that the contents of the FNIN buffer are **not** rewritten between blinks.*

## Middleware Configuration
To configure the AretasNanotronBridge middleware to enable ZMQ output (which will disable all other outputs) set the API mode to 3 in the .properties file of AretasNanotronBridge

`aretas.api.updatemode = 3`

Follow the Aretas Nanotron Middleware Guide for further configuration / optimization steps:

https://www2.aretas.ca/knowledge-base/aretas-nanotron-middleware-configuration-guide/

## Python demo
This Python demo shows you how to connect to the middleware layer with only a few lines of code. The middleware provides a discrete socket for each BO type. The message format for each socket endpoint is JSON you can deserialize the JSON message data in Python 

### Python Setup
First, download and install pyzmq if you haven't already done so:
`pip install pyzmq`

### Example code:
````Python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
# just change the endpoint to receive sensordata messages instead
socket.connect("tcp://localhost:8111")
socket.subscribe("")
while True:

    message = socket.recv()
    # do something with the received location data packet
    locationDatum = json.loads(message)
    print("%s" % locationDatum)
````
Sample output:
````json
{'tagId': 5116632, 'timestamp': 1576382077291, 'x': 8.302858543667623, 'y': 15.793891240347047, 'z': 2.0, 'blinkRateInterval': 211}
{'tagId': 5102545, 'timestamp': 1576382077403, 'x': 4.560454596386625, 'y': 16.679619082546353, 'z': 2.0, 'blinkRateInterval': 395}
{'tagId': 5102078, 'timestamp': 1576382077462, 'x': 7.102846035814868, 'y': 5.716295307070267, 'z': 2.0, 'blinkRateInterval': 200}
{'tagId': 5116632, 'timestamp': 1576382077515, 'x': 8.309447147836812, 'y': 15.802068555346956, 'z': 2.0, 'blinkRateInterval': 211}
{'tagId': 5102078, 'timestamp': 1576382077649, 'x': 7.117411065033274, 'y': 5.701537865206717, 'z': 2.0, 'blinkRateInterval': 204}
{'tagId': 5116632, 'timestamp': 1576382077723, 'x': 8.322285195564742, 'y': 15.813940658874932, 'z': 2.0, 'blinkRateInterval': 211}
{'tagId': 5102545, 'timestamp': 1576382077780, 'x': 4.561976633681092, 'y': 16.6836583335605, 'z': 2.0, 'blinkRateInterval': 397}
{'tagId': 5102078, 'timestamp': 1576382077780, 'x': 7.127957766320192, 'y': 5.706976010596711, 'z': 2.0, 'blinkRateInterval': 199}
{'tagId': 5116632, 'timestamp': 1576382077905, 'x': 8.342057280931218, 'y': 15.804198334214501, 'z': 2.0, 'blinkRateInterval': 210}
{'tagId': 5102545, 'timestamp': 1576382077985, 'x': 4.5687437849326935, 'y': 16.68127661780779, 'z': 2.0, 'blinkRateInterval': 394}
{'tagId': 5102078, 'timestamp': 1576382078045, 'x': 7.12488023488691, 'y': 5.694924748258292, 'z': 2.0, 'blinkRateInterval': 200}
````
