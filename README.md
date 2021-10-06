# Aretas API Documentation and Examples
Various Examples for the Aretas IoT API

## Companion Documentation
The Aretas Knowledge Base will contain companion documentation (Tutorials, Introductions, etc.). You can access that here: http://www2.aretas.ca/knowledge-base/

## REST API
Most of the Aretas IoT REST API methods are documented through the automatic WADL generator. You can find those here:
https://aretassensornetworks.github.io/APIExamples/swadl/wadl.html

The WADL generator does not pick up on Websockets and some of the Event and/or ML microservice methods are excluded for now. We'll document those separately. The WADL may be out of date as I do not update it with every commit. If you need up to the minute docs, please ping me.

## Python
The Python entries are the most updated, there are lots of examples in there in including several ML examples. The Python entries are here: https://github.com/AretasSensorNetworks/APIExamples/tree/master/python

Please review the README, there are several major sections:
* Sensor / Entity Data Query and Visualization
* Machine Learning / AI
* Timeseries Aggregation
* Sensor Middleware
* Location / RTLS Examples

## Javascript
The Javascript entries will generally be basic .html files that execute the method (using jquery) and return results for viewing, nothing fancy.
