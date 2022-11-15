# Sensor and Time Series Data Classification #

Going forward, I'll be using Jupyter Notebooks in discrete repos to demonstrate AI classification tasks 
with data from the API or other functionality present in the API

I've posted several repos to date including:

## Time Series Image Field ##

Several examples of using time series image fields (Gramian etc.) to classify sensor data using Neural Networks
Most (if not all) of the Neural Network models achieve state-of-the-art accuracy compared with other methods, with the 
added benefits of less data processing overhead, transfer learning and model architecture reuse. 

### Time Series Image Field Example ###

An introduction to image fields, and a neural network example using synthetic sensor events:

https://github.com/AretasSensorNetworks/TSImageFieldExample

### Gun Point Example ###

We import the gunpoint data and achieve 98% classification accuracy on previously unseen data.

https://github.com/AretasSensorNetworks/GunPointImageFieldExample

### ECG200 ###

This is a challenging dataset that contains ECG waveforms for normal heartbeat and heartbeats indicating myocardial infarction.
We achieved up to 90% accuracy on the training/validation split and 83% on previously unseen data.

https://github.com/AretasSensorNetworks/ECG200ImageFieldExample

## Spectrograms ##

Several examples of using spectrograms and CNN to classify sound data

### Word Recgognition ###

We use ResNet34 to recognize spectrograms of words we recorded locally. We then test on a previously unseen
dataset containing numerous confounders words and achieve 100% test accuracy.

https://github.com/AretasSensorNetworks/SpectrogramTesting

### Gunshot Sound Classification ###
A very challenging dataset containing 6500 recordings of 18 different firearms. We achieve 85% accuracy on the best model.

https://github.com/AretasSensorNetworks/GunShotSoundClassification

## Multivariate Time Series Data ##

Examples of classification tasks using "tabular sensor data"

### Occupancy Detection ###

This dataset contains different sensor data readings (CO2, Temperature, Relative Humidity, Light) and Occupancy. 

We use RandomForest to determine variables of significance, then train a Neural Network to achieve 93% accuracy.

https://github.com/AretasSensorNetworks/SensorDataOccupancyClassification