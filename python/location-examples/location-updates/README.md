# Location Websocket connection to the Aretas API #

This is a very basic example that connects to the Aretas API and streams real-time location data messages from one or many tags

Shows the resulting tag positions on a plot (not very exciting)

The example demonstrates:
1. Logging in to the API and generating an access token
2. How to authenticate with a websocket endpoint
3. Async handling for long lived websocket connections (without blocking __main__)
4. Sending the map entity and tag id requests for one or many sensors (read config.ini.sample)
5. Detecting collision / proximity events
6. Keeping track of tag positions
7. Updating a "plot" with the tag positions


