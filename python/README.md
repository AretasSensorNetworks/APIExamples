# Aretas API Python Examples
You may wish to start with the APIExamples/python/api-data-query.py example. It contains a full fledged API backed data mining application to chart a monitor over a defined time period.  And as of this writing, it's the ***only*** example!

## api-data-query Example
The supplied Python example demonstrates:

 1. How to login to the API and aquire a Token for Token based Authentication
 2. How to acquire the sensor type metadata 
 3. How to perform a basic historical data query
 4. How to chart the resulting data

### Required Python modules:
To run the api-data-query example, you need to install:

Plotly (for charting):

    $ pip install plotly
Requests (for http requests):

    $ pip install requests
   Pandas (for dataframe)
   

    $ pip install pandas
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
Querying data can be done a number of ways and the data query endpoints contain many options (decimation, moving average, smoothing, outlier filtering, indexes, etc). To get started with a basic data query though, use the following example (note the access token header):

    # define the API url for data queries
    url = "https://iot.aretas.ca/rest/sensordata/byrange"
    # now
    end =  int(round(time.time() *  1000))
    # 8 hours of data
    start = end - (8  *  60  *  60  *  1000)
    # the device ID / mac of one of the devices in the account
    mac: int  =  00001
    response = requests.get(url +  "?mac="  +  str(mac) +  "&begin="  +  str(start) +  "&end="  +  str(end) +  "&limit=10000000", headers={"Authorization" : "Bearer "  + API_TOKEN, "X-AIR-Token" : str(mac)})
    if response.status_code ==  200:
        json_response = json.loads(response.content.decode())
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