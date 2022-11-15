from .auth import APIAuth
import requests
import json


class APIClient:
    """Various methods for Client BO stuff"""
    def __init__(self, api_auth: APIAuth):
        self.api_auth = api_auth

    def get_client_location_view(self):
        """Get a list of all the locations, sensorlocations, buildingmaps and macs for this account
        :return:
        """
        headers = {"Authorization": "Bearer " + self.api_auth.get_token()}
        url = self.api_auth.api_config.get_api_url() + "client/locationview"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_content = json.loads(response.content.decode())
            return response_content
        else:
            print("Bad response code: " + str(response.status_code))
            return None
