import configparser
import sensor_data_query as sdq
import plotly.graph_objs as go


# an example showing the usage of varying length moving average windows on a sample
def main():

    config = configparser.ConfigParser()
    config.read("config.ini")

    mac = config['DEFAULT']['TARGET_MAC']
    target_type = config['DEFAULT']['TARGET_TYPE']

    end = sdq.now_ms()
    start = end - (7 * 24 * 60 * 60 * 1000)

    to_chart = list()

    # you can also just pass in your own MAC, target_type etc and not use the config.ini
    # no moving average (raw data)
    to_chart.append(sdq.query_sensor_data_basic(mac, target_type, start, end, 1000000))
    # moving average window of 10
    to_chart.append(sdq.query_sensor_data_basic(mac, target_type, start, end, 10000000, False, None, True, 10))
    # moving average window of 100
    to_chart.append(sdq.query_sensor_data_basic(mac, target_type, start, end, 10000000, False, None, True, 100))

    # downsamples the chart to 100 points max
    to_chart.append(sdq.query_sensor_data_basic(mac, target_type, start, end, 10000000, False, None, False, None, False, downsample=True, downsample_size=100))

    chart_data = []

    for data_set in to_chart:

        print("Number of records returned from query:{}".format(len(data_set)))

        xs = [x['timestamp'] for x in data_set]
        ys = [y['data'] for y in data_set]

        # extract the entity type label from the metadata in the API
        label = sdq.get_type_label(target_type)

        trace = go.Scatter(x=xs, y=ys, mode='lines', name='Sensor: {}'.format(label))

        layout = go.Layout(title='Aretas API Sensor Data for MAC:{}'.format(mac), plot_bgcolor='rgb(230, 230,230)')
        chart_data.append(trace)

    fig = go.Figure(chart_data, layout=layout)

    # write to html file
    fig.write_html('sensor-data-export.html', auto_open=True)


if __name__ == "__main__":
    main()
