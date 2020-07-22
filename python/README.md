# Aretas API Python Examples

These are examples of interacting with the Aretas API with Python. These examples are far from complete, 
however they demonstrate a lot of the more important API endpoints.

Eventually all of these examples will coalesce into an API package we can submit to pip. For now, there is a lot of 
duplicated code to keep all of the examples self-contained with minimal external dependencies

Each folder is broadly arranged by subject and should have it's own documentation

## Sensor / Entity Data Query and Visualization
APIExamples/python/sensor-data-query-and-visualization/

Contains examples of:
- Querying the Aretas API for historical data 
- Charting resulting data using plotly 
- Charting several entity types (temperature, relative humidity, indexes, etc.)
- Applying downsampling, moving average, outlier filtering, etc.

## Machine Learning / AI
APIExamples/python/ml_ai

Contains examples of:
- Realtime Probabalistic Anomaly detection
- Using the Aretas Probability web service
    - Unviariate histogram for one or many entities / types
    - Temporal univariate 
- KDE Fitting to sensor data
- Standard Probability Fitting
- Time Series Forecasting of Sensor / Entity Data using LSTM
- Regression vs AI performance
- Live websocket sensor data

## Timeseries Aggregation
APIExamples/python/timeseries-aggregation

- Demonstrates the Aretas Timeseries Aggregation API 

## Sensor Middleware
APIExamples/python/sensor-middleware

- Demonstrates how to connect a real sensor (SG111A) to the Aretas API and stream real-time data with minimal code

## Location / RTLS Examples

Contains examples for:

- Monitoring real-time Locations of RTLS tags
- Monitoring for proximity events
- Querying historical location data

## ZMQ Middleware Example

- Demonstrates how to connect to the middleware ZMQ endpoint and stream location messages