import numpy
import requests
import time
import json
import configparser
from matplotlib import pyplot

config = configparser.ConfigParser()
config.read("config.ini")

API_URL = config['DEFAULT']['API_URL']

USERNAME = config['DEFAULT']['API_USERNAME']
PASSWORD = config['DEFAULT']['API_PASSWORD']

API_TOKEN = None


# basic function to get an access token
def gettoken():
    api_response = requests.get(API_URL + "authentication/g?username=" + USERNAME + "&password=" + PASSWORD)
    if api_response.status_code >= 200:
        return api_response.content.decode()
    else:
        return None


def now_ms():
    return int(time.time() * 1000)


def get_probability(histo, X):
    # get the probability of X occurring within this distribution
    for b in histo['frequencyBins']:
        if X > b['min'] and X <= b['max']:
            return b['probability']

    return 0

# get an authorization token from the API
API_TOKEN = gettoken()

if API_TOKEN is None:
    print("Could not get access token!")
    exit()
else:

    url = API_URL + "probability/univariatehistogram"
    # now
    end = int(round(time.time() * 1000))
    # 7 days of data
    start = end - (30 * 24 * 60 * 60 * 1000)

    # the "devices" we're profiling
    macs = config['DEFAULT']['TARGET_MACS']

    macsToK = [int(x.strip()) for x in macs.split(",")]

    strMacs = ""
    for mac in macsToK:
        strMacs = strMacs + "&macs=" + str(mac)

    # get the histogram for some temperature sensors (type 246) with 100 bins
    queryUrl = url + "?type=246&startTime=" + str(start) + "&endTime=" + str(end) + "&nBins=100" + strMacs + "&recordLimit=1000000"

    print(queryUrl)
    startTime = now_ms()

    response = requests.get(queryUrl, headers={"Authorization": "Bearer " + API_TOKEN, "X-AIR-Token": str(mac)})

    endTime = now_ms()

    print("Time taken for query and data: {0} ms".format(endTime - startTime))

    if response.status_code == 200:

        histogram = json.loads(response.content.decode())
        print(histogram)

        histogram['frequencyBins'].sort(key=lambda x: x['density'])

        densities = [x['density'] for x in histogram['frequencyBins']]
        probabilities = [x['probability'] for x in histogram['frequencyBins']]

        binLabels = ['{0:.2f}'.format(x['min']) + "-" + '{0:.2f}'.format(x['max']) for x in histogram['frequencyBins']]
        count = sum([x['count'] for x in histogram['frequencyBins']])

        # probabilities.sort()
        # densities.sort()

        print("Number of observations:{0}".format(count))
        print("5th percentile:{0}".format(numpy.percentile(probabilities, 5.0)))
        print("90th percentile:{0}".format(numpy.percentile(probabilities, 90.0)))
        print("Probability of {0} is: {1}".format(20.0, get_probability(histogram, 20.0)))

        fig, axes = pyplot.subplots(2, 1)

        from matplotlib.ticker import LinearLocator
        axes[0].plot(densities)
        axes[0].set_title("Histogram")
        axes[0].set_ylabel("Densities")
        axes[0].set_xlabel("Bin")
        axes[0].set_xticks(range(0, len(binLabels)))
        axes[0].set_xticklabels(binLabels, rotation=90)
        axes[0].get_xaxis().set_major_locator(LinearLocator(numticks=20))

        axes[1].set_title("Histogram")
        axes[1].plot(probabilities)
        axes[1].set_ylabel("Probabilities")
        axes[1].set_xlabel("Bin")
        axes[1].set_xticks(range(0, len(binLabels)))
        axes[1].set_xticklabels(binLabels, rotation=90)
        axes[1].get_xaxis().set_major_locator(LinearLocator(numticks=20))

        fig.tight_layout()

        fileName = '{}.png'.format(startTime)

        pyplot.savefig(fileName)

        pyplot.show()

    else:
        print("Invalid response code:")
        print(response.status_code)
        print('\n')

