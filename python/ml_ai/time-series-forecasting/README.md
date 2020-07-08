## Time Series Forecasting Examples ##
#### Vanilla LSTM ####
This example is a single step forecasting utility, probably useful for forecasting next day min/max or averages.
Or, if you train it on particular intervals or bins, it might be useful for predicting the next bin.

You'll want to adjust the sensor types, query length and other parameters in the actual API query. The current version is designed to profile and predict temperature. 
Until I parameterize the functions in aretas_data_query.py, you'll want to adjust the query params yourself

#### Multi-step LSTM ####

This example (at the time of this writing) trains the LSTM on 50 samples and 20 output timesteps. It needs a lot of data (I initially trained on 20 days)

At the standard reporting interval for sensor data, 20 output steps gives you ~40 mins of predictive value. 

##### Notes #####
Ultimately, these examples will be more useful when we bin the data (1hr maximums for example) and train / predict on hourly or daily timesteps. These models can then 
be used to forecast filter changes, maintenance intervals, failures, etc.