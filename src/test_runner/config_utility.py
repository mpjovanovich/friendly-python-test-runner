import os
from dotenv import load_dotenv

load_dotenv()


class ConfigUtility:

    @staticmethod
    def get_setting(key, default=None):
        ## We're assuming settings are set in the environment
        value = os.environ.get(key, default)
        if value is None:
            raise ValueError(
                f"Required environment variable '{key}' is not set")
        return value
