import requests
from . import *


class Auth:

    def __init__(self):

        global ARETAS_API_URL

        self.API_TOKEN = None
        self.API_URL = ARETAS_API_URL
        pass

    def test_token(self):

        api_response = requests.get(self.API_URL + "greetings/isloggedin",
                                    headers={"Authorization": "Bearer " + self.API_TOKEN})

        if api_response.status_code == 401 or 403:
            return False
        else:
            return True

    def refresh_token(self):

        global ARETAS_USERNAME, ARETAS_PASSWORD

        # basic function to get an access token
        api_response = requests.get(
            self.API_URL + "authentication/g?username=" + ARETAS_USERNAME + "&password=" + ARETAS_PASSWORD)

        if api_response.status_code >= 200:
            self.API_TOKEN = api_response.content.decode()

            return self.API_TOKEN
        else:
            return None

    def get_token(self):

        if self.API_TOKEN is None:
            # try and get one
            return self.refresh_token()
        else:
            if self.test_token() is False:
                return self.refresh_token()
            else:
                return self.API_TOKEN


