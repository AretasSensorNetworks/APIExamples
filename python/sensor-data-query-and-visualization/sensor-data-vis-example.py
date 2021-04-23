import configparser
import sensor_data_query as sdq
import plotly.graph_objs as go


# a basic example showing how to perform a multi-type query from the API for a particular MAC
# and create a nice chart with plotly (which is a very nice charting API)
def main():

    config = configparser.ConfigParser()
    config.read("config.ini")

    mac = config['DEFAULT']['TARGET_MAC']
    # target_type = config['DEFAULT']['TARGET_TYPE']

    # get the current time in linux epoch ms from the convenience function
    end = sdq.now_ms()

    # set the start time for the query 7 days ago (again in linux epoch ms)
    start = end -(7 * 24 * 60 * 60 * 1000)

    # you can also just pass in your own MAC, target_type etc and not use the config.ini
    type_map = sdq.query_sensor_data_basic(mac, None, start, end, 1000000)

    # print(response)

    chart_data = []

    for key in type_map:

        xs = [x['timestamp'] for x in type_map[key]]
        ys = [y['data'] for y in type_map[key]]

        # extract the entity type label from the metadata in the API
        label = sdq.get_type_label(key)

        # create a trace for that type to add to the plotly chart
        trace = go.Scatter(x=xs, y=ys, mode='lines', name='Sensor: {}'.format(label))

        layout = go.Layout(title='Aretas API Sensor Data for MAC:{}'.format(mac), plot_bgcolor='rgb(230, 230,230)')

        # append the trace to the chart_data
        chart_data.append(trace)

    # create the chart object with the specified traces and layout
    fig = go.Figure(chart_data, layout=layout)

    # write to html file...nice!
    fig.write_html('sensor-data-export.html', auto_open=True)


if __name__ == "__main__":
    main()
