from deta import Deta
from decouple import config


DETA_PROJECT_KEY   = config("DETA_PROJECT_KEY")
DETA_DB_NAME  = config("DETA_DB_NAME")
DETA_DB_USERS = config("DETA_DB_USERS")
DETA_DB_CUSTOMERS = config("DETA_DB_CUSTOMERS")
DETA_DB_PRODUCTS = config("DETA_DB_PRODUCTS")
DETA_DB_ORDERS = config("DETA_DB_ORDERS")


deta = Deta(DETA_PROJECT_KEY)
deta.Base(DETA_DB_NAME)

db_user = deta.Base(DETA_DB_USERS)
db_customer = deta.Base(DETA_DB_CUSTOMERS)
db_product = deta.Base(DETA_DB_PRODUCTS)
db_order = deta.Base(DETA_DB_ORDERS)

