import configparser


class APIConfig:

    def __init__(self, config_path=None):

        # cur_dir = os.path.dirname(__file__)
        # ymmv
        # config.read(cur_dir + "\\config.ini")
        self.___config = configparser.ConfigParser()
        if config_path is None:
            self.___config.read("config.ini")
        else:
            self.___config.read(config_path)

        self._API_URL = self.___config['DEFAULT']['API_URL']
        self._API_USERNAME = self.___config['DEFAULT']['API_USERNAME']
        self._API_PASSWORD = self.___config['DEFAULT']['API_PASSWORD']

    def get_api_url(self):
        return self._API_URL

    def get_api_username(self):
        return self._API_USERNAME

    def get_api_password(self):
        return self._API_PASSWORD
