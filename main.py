from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.security import auth
from core.security.auth import NotAuthenticatedException
from core import core
from core import users


app = FastAPI()


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/')


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(core.router)
app.include_router(users.router)
app.include_router(auth.router)

