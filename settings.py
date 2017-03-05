import os

def get_env(name):
  return os.environ[name]
  
REDIS_URL = get_env("REDIS_URL")
SECRET_KEY = get_env("SECRET_KEY")
GOOGLE_CLIENT_ID = get_env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_env("GOOGLE_CLIENT_SECRET")
