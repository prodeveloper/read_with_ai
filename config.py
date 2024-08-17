import configparser
import os
from collections import namedtuple
import json

class ConfigLoader:
    """Loads and manages configuration settings for the application."""
    config = configparser.ConfigParser()
    database_config = namedtuple('DatabaseConfig', [
            'DB_HOST', 
            'DB_NAME', 
            'DB_USER', 
            'DB_PASSWORD',
            'DB_PORT'
        ])
    def __init__(self):
        self._get_configs()
        self._db_configs()
    @property
    def configs(self):
        config = configparser.ConfigParser()
        config.read('config.ini') 
        Config = namedtuple('Config', ['GEMINI_API_KEY', 'FIREBASE_SERVICE_ACCOUNT', 'LOCAL_PASSWORD', 'GOOGLE_APPLICATION_CREDENTIALS'])
        # Prioritize environment variables set in Cloud Run
        GEMINI_API_KEY = os.environ.get('gemini') if os.environ.get('gemini') else config.get('GEMINI', 'GEMINI_API_KEY', fallback=None)
        LOCAL_PASSWORD = os.environ.get('password') if os.environ.get('password') else config.get('LOCAL', 'PASSWORD', fallback=None)
        #Because Firebase expects a dictionary while Google application credentials expects a string
        if(os.environ.get('firebase')):
            FIREBASE_SERVICE_ACCOUNT = json.loads(os.environ.get('firebase'))
            GOOGLE_APPLICATION_CREDENTIALS = None
        else:
            FIREBASE_SERVICE_ACCOUNT = config.get('GEMINI', 'FIREBASE_SERVICE_ACCOUNT', fallback=None)
            GOOGLE_APPLICATION_CREDENTIALS = FIREBASE_SERVICE_ACCOUNT


        return Config(GEMINI_API_KEY, FIREBASE_SERVICE_ACCOUNT, LOCAL_PASSWORD, GOOGLE_APPLICATION_CREDENTIALS)
    
    def get_prompt(self):
        default_prompt = """
Use the context from this page of the book to teach me. I want to use the preq framework

Point: the main idea
Reason: why this makes sense
Example: make this one as visual as possible. Use analogies and so on
Question: leave me with something to think about


Feel free to use as many preqs as possible to illustrate the point.

The page will normally only have a sub point of  the main content. Use it as a guide but explain the full context.

Take the perspective I am preparing for an interview in system design and coding so where possible add this context 

"""
        prompt = os.environ.get('prompt') if os.environ.get('prompt') else default_prompt
        return prompt
    def _get_configs(self,*,config_string:str=None):
        if config_string:
            self.config.read_string(config_string)
        else:
            online_config = os.environ.get('read_with_ai_configs')
            if online_config:
                self.config.read_string(online_config)
            else:
                self.config.read('config.ini')

    def _load_config(self, config_type, section, convert_to_int=False):
        for field in config_type._fields:
            value = os.environ.get(field) or self.config.get(section, field, fallback=None)
            if convert_to_int and value is not None:
                try:
                    value = int(value)
                except ValueError:
                    value = 0
            setattr(config_type, field, value)

    def _db_configs(self):
        self._load_config(self.database_config, 'DATABASE')
