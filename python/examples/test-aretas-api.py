import sys
sys.path.append('C:\\Users\\aretas\\Documents\\GitHub\\APIExamples\\python\\')
print(sys.path)

from aretasapiclient.api_config import *
from aretasapiclient.sensor_data_query import *
from aretasapiclient.auth import *
from aretasapiclient.aretas_client import *
from aretasapiclient.utils import Utils as autils
from aretasapiclient.api_cache import APICache


config = APIConfig()
auth = APIAuth(config)
client = APIClient(auth)


client_location_view = client.get_client_location_view()

my_client_id = client_location_view['id']
all_macs = client_location_view['allMacs']
my_devices_and_locations = client_location_view['locationSensorViews']

# show locations with active devices
for active in [obj for obj in my_devices_and_locations if obj['lastSensorReportTime'] != -1]:
    print("Description: {0} Country: {1} State/Province: {2} City: {3} Lat: {4} Lon: {5}".format(
        active['location']['description'],
        active['location']['country'],
        active['location']['state'],
        active['location']['city'],
        active['location']['lat'],
        active['location']['lon']))

# show the most recent data from the top sensors
active_locs = [location for location in my_devices_and_locations if location['lastSensorReportTime'] != -1]
now = autils.now_ms()

print("\nActive Devices:")

active_devices = []
for loc in active_locs:
    for device in loc['sensorList']:
        if(now - device['lastReportTime']) < (24 * 60 * 60 * 1000):
            active_devices.append(device)

print("\nLocations with active devices:")
for active_device in active_devices:
    print("Description: {0} Mac: {1} Lat: {2} Lon: {3}".format(active_device['description'], active_device['mac'], active_device['lat'], active_device['lon']))

# get the latest data for all the devices
active_macs = [device['mac'] for device in active_devices]

cache = APICache(auth)

latest_data_macs = cache.get_latest_data(active_macs)

sensor_data_map = dict()

for mac in active_macs:
    b = [datum for datum in latest_data_macs if datum["mac"] == mac]
    """ 
    dict format for sensor data "hashmap"
    a = {
        18992399: {
            181: {
                "data": 400.0,
                "timestamp": 1668403620062
            },
            248: {
                "data": 23.0
                "timestamp": 1668403620062
            }
        },
        1097280238:{
            181: {
                "data": 431.0,
                "timestamp: 1668403620062
            }
        }
    }
    """
    for datum in b:
        if mac not in sensor_data_map:
            sensor_data_map[mac] = dict()

        sensor_type = datum['type']

        if sensor_type not in sensor_data_map[mac]:
            sensor_data_map[mac][sensor_type] = dict()

        sensor_data_map[mac][sensor_type] = {
            "data": datum['data'],
            "timestmap": datum['timestamp']
        }

print(sensor_data_map)






