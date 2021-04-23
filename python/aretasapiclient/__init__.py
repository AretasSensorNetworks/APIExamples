import configparser
# import os

config = configparser.ConfigParser()

# cur_dir = os.path.dirname(__file__)
# ymmv
# config.read(cur_dir + "\\config.ini")

config.read("config.ini")

ARETAS_API_URL = config['DEFAULT']['API_URL']

ARETAS_USERNAME = config['DEFAULT']['API_USERNAME']
ARETAS_PASSWORD = config['DEFAULT']['API_PASSWORD']

API_TOKEN = None

