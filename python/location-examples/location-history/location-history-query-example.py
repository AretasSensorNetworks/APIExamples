import matplotlib.pyplot as plt
import location_data_query as ldq


def main():

    end = ldq.now_ms()
    start = end - (8 * 60 * 60 * 1000)
    tag_id = 20001

    # apply a moving average window to each axis then sum the each averaged axis back into one point
    moving_average = False

    # the window size of the moving average. larger windows result in smoother lines but larger lag and less granularity
    moving_average_window = 10

    # apply an interquartile range filter to the query. the IQR filter is run BEFORE the moving average filter
    outlier_filter = False

    # the iqr multiple to use, adjust to suit
    iqr_multi_range = 1.5

    # whether or not to offset the query span from the last time the sensor reported
    offset_data = False

    location_data = ldq.get_location_data_history(tag_id, start, end, record_limit=100000,
                                         iqr_filter=outlier_filter, iqr_multi=iqr_multi_range,
                                         moving_average=moving_average, mv_window_size=moving_average_window,
                                         offset_data=offset_data)

    if location_data is None:
        print("The query returned no data!")

    else:
        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        xs = [x['x'] for x in location_data]
        ys = [x['y'] for x in location_data]
        zs = [x['z'] for x in location_data]

        # for a line version
        # ax.plot3D(xs, ys, zs, 'gray')

        ax.scatter3D(xs, ys, zs)

        plt.show()

        print(location_data)


if __name__ == "__main__":
    main()

