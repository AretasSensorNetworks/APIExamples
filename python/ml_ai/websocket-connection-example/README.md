# Websocket connection to the Aretas API
This example connects to the Aretas API and streams real-time sensor messages from one or many sensors

The example demonstrates:
1. Logging in to the API and generating an access token
2. How to authenticate with a websocket endpoint
3. Async handling for long lived websocket connections (without blocking __main__)
4. Sending the location entity and mac requests for one or many sensors (read config.ini.sample)


