# Location Data History Querying #

This example demonstrates querying and displaying the 3D location data from the 
locationreporthistory/byrange API endpoint

The REST endpoint is described in location_data_query.py

Running the example will result in a 3D scatterplot of location data history:

![3D Scatter Plot](http://www2.aretas.ca/wp-content/uploads/2020/07/location_api_scatter_plot.png)

## Configuration / running the example ##
Either rename config.ini.sample to config.ini or create a config.ini file in the same folder
where you're running the code. Ensure the following config options are present (fill in your information):
    
    [DEFAULT]
    API_URL = https://iot.aretas.ca/rest/
    
    API_USERNAME = username
    API_PASSWORD = password
    
In location-history-query-example.py, change the tag_id to one in your account: 

    tag_id = your_tag_id
    
Adjust the options and run the example (will query 8 hours of recent tag history):

    python3 location-history-query-example.py

## Building Your Own Queries ##

Import the utility functions for the REST query

    import location_data_query as ldq
    
The API requires time in linux epoch milliseconds, there is a utility function in 
location_data_query to get the current time in milliseconds:

    end_time = ldq.now_ms()
    
Call the function:

    ldq.get_location_data_history(tag_id, ....)
    
### API Options ###
    
    # the "end time" for the query in epoch milliseconds. 
    end = ldq.now_ms()
    
    # the "start time" for the query (should be before the end time)
    # 8 hours * 60 minutes * 60 seconds * 1000 millieconds = 8 hours of milliseconds
    # so this will give us 8 hours of data
    start = end - (8 * 60 * 60 * 1000)
    
    # the tag id / mac of the entity
    tag_id = 123456

    # apply a moving average window to each axis then sum the each averaged axis back into one point
    # default is False
    moving_average = False

    # the window size of the moving average. larger windows result in smoother lines but larger lag and less granularity
    # default is 1
    moving_average_window = 10

    # apply an interquartile range filter to the query. the IQR filter is run BEFORE the moving average filter
    # default is False
    outlier_filter = False

    # the iqr multiple to use, adjust to suit
    # default is 1.5
    iqr_multi_range = 1.5

    # whether or not to offset the query span from the last time the sensor reported
    # this is useful if you have an entity that has not reported in some time
    # and you don't know when it last reported
    offset_data = False

### Errata ###

The example as configured will output a 3D scatterplot of each recorded "blink". The number of
blinks returned by the software will depend on several things. 

1) If you are using middleware, you may have a "persistence interval" that is different than the blink interval of 
your device. For example, your device might blink every 100ms but the persistence interval is set to 5000ms 
(meaning you only permanently store one position update every 5 seconds)

2) The current moving average algorithm is a *cumulative moving average* and will *reduce* the number of datapoints
in the output 
