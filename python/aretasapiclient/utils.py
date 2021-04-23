import time
from . import *


class Utils:
    def __init__(self):
        pass

    # utility function to get the time in milliseconds
    @staticmethod
    def now_ms():
        return int(time.time() * 1000)
