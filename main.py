from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.security import auth
from core import core
from core import users


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(core.router)
app.include_router(users.router)
app.include_router(auth.router)

