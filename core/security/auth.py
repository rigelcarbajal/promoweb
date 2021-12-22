from fastapi_login import LoginManager
from decouple import config


AUTH_SECRET_KEY = config("AUTH_SCRET_KEY")

manager = LoginManager(AUTH_SECRET_KEY, '/')




