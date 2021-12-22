from deta import Deta
from decouple import config


DETA_PROJECT_KEY   = config("DETA_PROJECT_KEY")
DETA_DB_NAME  = config("DETA_DB_NAME")
DETA_DB_USERS = config("DETA_DB_USERS")


deta = Deta(DETA_PROJECT_KEY)
deta.Base(DETA_DB_NAME)

db_user = deta.Base(DETA_DB_USERS)

