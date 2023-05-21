from dotenv import load_dotenv
import os

load_dotenv()

def _env_getter(secret_key):
    return os.environ.get(secret_key)

def env_get_open_ai_api_key():
    return _env_getter('OPEN_AI_API_KEY')

def env_get_serper_api_key():
    return _env_getter('SERPER_API_KEY')
