import os


class ConfigEnvironmentVariableNotFound(Exception):
    pass


class Config:
    def __init__(
        self,
        user_id: str = None,
        homeserver: str = None,
        device_id: str = None,
        access_token: str = None,
    ):
        self._config = dict(
            user_id=user_id,
            homeserver=homeserver,
            device_id=device_id,
            access_token=access_token
        )

    @classmethod
    def from_environment(cls):
        try:
            user_id = os.environ["SUGAROID_MX_USERID"]
            homeserver = os.environ["SUGAROID_MX_HOMESERVER"]
            device_id = os.environ["SUGAROID_MX_DEVICEID"]
            access_token = os.environ["SUGAROID_MX_ACCESSTOKEN"]
        except KeyError as e:
            raise ConfigEnvironmentVariableNotFound(f"{e}")
        return Config(
            user_id=user_id,
            homeserver=homeserver,
            device_id=device_id,
            access_token=access_token
        )
    
    @classmethod
    def from_json(cls, filepath):
        with open(filepath) as fp:
            _data = json.load(fp)
        return Config(**_data)

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return None

