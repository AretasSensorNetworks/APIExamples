import requests
import serial
import time

API_URL = "https://iot.aretas.ca/rest/"

# change these values to use your account
USERNAME="username"
PASSWORD="password"

API_TOKEN = None

ser = serial.Serial()
# change this value to use your FTDI COM port
ser.port = "COM15"
ser.baudrate = 9600
ser.parity = serial.PARITY_NONE
ser.bytesize = serial.EIGHTBITS
ser.stopbits = 1

# get an authorization token to use in the Request Header of subsequent requests
def gettoken():
    global USERNAME, PASSWORD, API_URL
    response = requests.get(API_URL + "authentication/g?username=" + USERNAME + "&password=" + PASSWORD);
    if response.status_code >= 200 :
        return response.content.decode()
    else:
        return None

# send a data point to the Aretas API
def sendToAPI(mac, timestamp, dataType, dataValue):
    global API_TOKEN, API_URL
    response = requests.get(API_URL + "ingest/secured/std/get" + "?t=" + str(timestamp) + "&m=" + str(mac) + "&st=" + str(dataType) + "&d=" + str(dataValue), headers={"Authorization": "Bearer " + API_TOKEN})
    print("API Response:" + str(response.status_code))
    return response.status_code

# generic send data function to help create a new API_TOKEN if it expired
# return with the response code
def senddata(dataType, dataValue):

    global API_TOKEN

    # change this mac address to the device address you created in the device manager
    m = 1234567890
    now = int(round(time.time() * 1000))
    resp_code =  sendToAPI(m, now, dataType, dataValue)

    if resp_code == 401:
        API_TOKEN = gettoken()
        if API_TOKEN is None:
            return -1
        else:
            resp_code = sendToAPI(m, now, dataType, dataValue)

    return resp_code

# open the serial port and read in the CO2 values from the SG111A sensor
def getco2():
    ser.open()
    buffer = ser.read(8)

    for b in buffer:
        print(hex(b))

    print(buffer)

    ppm = (buffer[5] * 256) + buffer[4]

    print("ppm: " + str(ppm))
    ser.close()
    return ppm

# get an authorization token from the API
API_TOKEN = gettoken()

if API_TOKEN is None:
    print("Could not get access token!")
    exit()

# send sensor data every 30 seconds to the API
try:
    while True:
        ppm = getco2()
        if 5000 > ppm >= 300:
            
            # note that 181 is the data type for CO2
            senddata(181, ppm)
        else:
            print("Invalid CO2 value")

        time.sleep(30)

except KeyboardInterrupt:
    exit()