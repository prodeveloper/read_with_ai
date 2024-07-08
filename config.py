import configparser
import os
from collections import namedtuple

class ConfigLoader:
    @property
    def configs(self):
        Config = namedtuple('Config', ['GEMINI_API_KEY', 'FIREBASE_SERVICE_ACCOUNT', 'LOCAL_PASSWORD', 'GOOGLE_APPLICATION_CREDENTIALS'])
        # Prioritize environment variables set in Cloud Run
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        FIREBASE_SERVICE_ACCOUNT = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        LOCAL_PASSWORD = os.environ.get('LOCAL_PASSWORD')
        
        # Fallback to config file if environment variables are not set
        if not all([GEMINI_API_KEY, FIREBASE_SERVICE_ACCOUNT, LOCAL_PASSWORD]):
            config = configparser.ConfigParser()
            config.read('config.ini') 
            
            GEMINI_API_KEY = GEMINI_API_KEY or config.get('GEMINI', 'GEMINI_API_KEY', fallback=None)
            FIREBASE_SERVICE_ACCOUNT = FIREBASE_SERVICE_ACCOUNT or config.get('GEMINI', 'FIREBASE_SERVICE_ACCOUNT', fallback=None)
            LOCAL_PASSWORD = LOCAL_PASSWORD or config.get('LOCAL', 'PASSWORD', fallback=None)
        GOOGLE_APPLICATION_CREDENTIALS = FIREBASE_SERVICE_ACCOUNT
        return Config(GEMINI_API_KEY, FIREBASE_SERVICE_ACCOUNT, LOCAL_PASSWORD, GOOGLE_APPLICATION_CREDENTIALS)