import configparser
import time_series_aggregation as tsa


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    mac = config['DEFAULT']['TARGET_MAC']
    target_type = config['DEFAULT']['TARGET_TYPE']

    end = tsa.now_ms()
    start = end - (7 * 24 * 60 * 60 * 1000)

    response = tsa.get_hourly_aggregation(mac, target_type, start, end, False)

    print(response)

    pass


if __name__ == "__main__":
    main()
