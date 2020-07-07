# Probability service endpoint examples

There will be several examples here for testing the Probability / Anomaly detection service in Python

1) Univariate
2) Multivariate
3) Temporal Univariate
4) KDE with auto parameter tuning / solving
5) Setting up an anomaly monitor
6) Subscribing to the anomaly service websocket



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

Example (querying for a Histogram):

http://localhost:8080/rest/probability/univariatehistogram?type=248&startTime=1593210799254&endTime=1593815599254&nBins=100&macs=33333333&macs=222222222&macs=11111111&recordLimit=1000000

Using the sample code (aretas-probability-service-test-histogram.py) will produce output similar to the following:

![](https://www2.aretas.ca/wp-content/uploads/2020/07/1593816805711.png)

More coming soon...

