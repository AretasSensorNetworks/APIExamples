# Sensor Middleware Example

With only a few lines of code, you can bridge almost any device and bring it online into the Aretas IoT Platform. Once you do, you can open up your device to an entire IoT Platform featuring Alerts, mobile app, Analytics, Live Data and more. 

In this example you are shown how to connect directly to the SG111A CO2 sensor with a low cost FTDI adapter and bring the data from the sensor straight into the platform. However, the principles demonstrated would work with any type of sensor or device. 

## Overall Steps
1. Create a standard (mock) device in your Aretas IoT Cloud Account (take note of the MAC address)
2. Hookup the sensor (more below)
3. Configure the script
4. Run the script

## Device Hookup

To learn how to hookup the FTDI device and the SG111A, review the tutorial here: [https://www2.aretas.ca/knowledge-base/sg111a-co2-sensor-and-python/](https://www2.aretas.ca/knowledge-base/sg111a-co2-sensor-and-python/)
To recap briefly: 
1. Purchase a SparkFun FTDI adapter (or Adafruit or any of the other multitude of FTDI Adapters out there)
2. Purchase an SG111A or SG112A or SG112B sensor
3. Hookup the sensor according to the diagram and plug in the FTDI adapter
4. Find out the enumerated serial port in the device manager
![FTDI to SG111A](https://www2.aretas.ca/wp-content/uploads/2019/11/FTDI-SG111A-Hookup.png)

After correctly connecting the SG111A and FTDI Adapter, find the FTI Serial Port:
![FTDI Serial port](https://www2.aretas.ca/wp-content/uploads/2019/11/windows-device-manager-usb-port.jpg)

## Configuring and Running the Example

### Dependencies
The script depends on a few Python modules
pyserial and request
If you don't already have them installed:

    $ pip install pyserial
and

    $ pip install requests

### Configuration
Edit the following lines in the script to suit your configuration:

    # change these values to use your account
    USERNAME="username"
    PASSWORD="password"
    ...
    # change this value to use your FTDI COM port
    ser.port =  "COM15"
    ...
    # change this mac address to the device address you created in the device manager
    m =  1234567890
Once everything is configured, just run:

    $ python sg111A-iot.py
On the console, you should see basic debugging output showing the script is receiving valid sensor data and sending data to the API:

    ppm: 674
    API Response:200

If all goes well, you'll see something like this in the Aretas IoT user interface (the SG111A middleware is the top chart in this case):
![enter image description here](http://www2.aretas.ca/wp-content/uploads/2019/11/SG111A-Python-Live-Data.png)





