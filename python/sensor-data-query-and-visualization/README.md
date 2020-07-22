# Aretas Sensor Data API Query Examples
You may wish to start with  sensor-data-vis-example.py It contains a full fledged API backed data mining application to chart a monitor over a defined time period.

The second example shows how to use moving average windows and data decimation (downsampling with feature preservation) 

You must have an account and connected devices / entities (with data stored in the API) to use these examples

## API Data Query Examples
The supplied Python example demonstrates:

 1. How to login to the API and aquire a Token for Token based Authentication
 2. How to acquire the sensor type metadata 
 3. How to perform a basic historical data query
 4. How to chart the resulting data
 5. How to use moving average windows and data decimation

### config.ini

Copy config.ini.sample to config.ini 

Your file will need the following lines:

    [DEFAULT]
    API_URL = https://iot.aretas.ca/rest/
    
    API_USERNAME = username
    API_PASSWORD = password
    
    TARGET_MAC =
    TARGET_TYPE =

### Required Python modules:
To run the api-data-query example, you need to install:

Plotly (for charting):

    $ pip install plotly
Requests (for http requests):

    $ pip install requests

### API Related Code Explanation
#### Authentication
Most methods in the Aretas API require authentication per request. The API uses Token Based Authentication. You must login to a registered authentication endpoint, receive a token, then use the token in subsequent requests in your Request header. 
Example to acquire a token:

    def  gettoken():
        response = requests.get("https://iot.aretas.ca/rest/authentication/g?username="  + USERNAME +  "&password="  + PASSWORD)
        if response.status_code >=  200 :
            return response.content.decode()
        else:
            return  None
    # get an authorization token from the API
    API_TOKEN = gettoken()
#### Querying Data
Querying data can be done a number of ways and the data query endpoints contain many options (decimation, moving average, smoothing, outlier filtering, indexes, etc). To get started with a basic data query is pretty easy:
    
    import sensor_data_query as sdq
    sdq.query_sensor_data_basic(mac, None, start, end, 1000000)
    
### Running the code
Make sure you:

 1. Enter a valid username and password (or token)
 2. Enter in a valid mac/device ID from your account
 3. Adjust the query interval / duration to suit your needs

From the command prompt, just type:

    $ python api-data-query.py
    
### Results
The magic of Plotly will produce a nice HTML report page containing the chart for the query interval:
![Chart results](https://www2.aretas.ca/wp-content/uploads/2019/11/python-api-data-query-output.jpg)

#### Moving Average / Decimation Comparison

The second example (sensor-data-vis-example-mv.py) contains a comparison of a few moving average window sizes and a decimation / downsampling
 (with feature preservation)
 
    # no moving average (raw data)
    results = sdq.query_sensor_data_basic(mac, target_type, start, end, 1000000)
    
    # moving average window of 10
    results = sdq.query_sensor_data_basic(mac, target_type, start, end, 10000000, False, None, True, 10)
    
    # moving average window of 100
    results = sdq.query_sensor_data_basic(mac, target_type, start, end, 10000000, False, None, True, 100)

    # downsamples the chart to 100 points max
    results = sdq.query_sensor_data_basic(mac, target_type, start, end, 10000000, False, None, False, None, False, downsample=True, downsample_size=100)
 
 The last chart line (light purple) is the downsampled version
 ![Moving Average / Decimation](http://www2.aretas.ca/wp-content/uploads/2020/07/moving-average-decimation-comparison.jpg) 