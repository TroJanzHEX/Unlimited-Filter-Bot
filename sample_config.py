import os

class Config(object):

    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

    APP_ID = int(os.environ.get("APP_ID", 12345))

    API_HASH = os.environ.get("API_HASH", "")
    
    DATABASE_URI = os.environ.get("DATABASE_URI", "")

    DATABASE_NAME = str(os.environ.get("DATABASE_NAME", "Cluster0"))

    AUTH_USERS = set(str(x) for x in os.environ.get("AUTH_USERS", "").split())
