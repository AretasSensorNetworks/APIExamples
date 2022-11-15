# Probability service endpoint examples

There will be several examples here for testing the Probability / Anomaly detection service in Python

1) Univariate
2) Multivariate
3) Temporal Univariate
4) KDE with auto parameter tuning / solving
5) Setting up an anomaly monitor
6) Subscribing to the anomaly service websocket

The two examples so far:

### aretas-probability-service-test-histogram

This example connects to the API and profiles a group of sensors to determine the probability distribution of
the sensor data. A Histogram is returned from the API that can be used to determine the probability of a new sensor reading.
In this way, we can perform anomaly detection based on the quantile of the returned probability.

### aretas-probability-service-test-probability

This example demonstrates how we can send a list of X values (sensor data readings) to the API and get back
a similarly dimensioned array of probabilities for the X values. 

Further:
## Univariate

The univariate API endpoint allows you to:

- Get a histogram of one or many data sources of a specific type (for example, CO2 from several monitors) - the histogram contains metadata for the counts, intervals, probabilities and densities for each bin
- Get the probability or density of X occurring based on that list of data sources
- Determine the profile time span, number of bins, etc.

Calling the endpoint in Python is very simple, just construct a URL with the following parameters:

**macs** (a list of entity IDs to query)

**startTime** (the start time for the profiling)

**endTime** (the end time for the profiling)

type (the entity type. e.g. 181 for CO2, 248 for RH, etc)

**recordLimit** (set this very high - it determines the maximum number of records to fetch from the time series data store)


