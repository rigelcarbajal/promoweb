from datetime import timedelta
from fastapi import Depends, APIRouter, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from decouple import config

from .tools import verify_password
from ..database import db_user


AUTH_SECRET_KEY = config("AUTH_SECRET_KEY")


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


manager = LoginManager(
    AUTH_SECRET_KEY, 
    '/auth', 
    use_cookie=True,
    cookie_name="access-token",
    default_expiry=timedelta(hours=12)
    )


@manager.user_loader()
async def user_exist(key: str):
    user = db_user.get(key)
    return user


@router.post('/', response_description="Login form route.", response_class=RedirectResponse)
async def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = await user_exist(username)

    if not user:
        raise InvalidCredentialsException
    elif verify_password(password, user["password"]) == False:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=user["key"])
    )


    rr = RedirectResponse("/dashboard", 302)
    rr.set_cookie(key="access-token", value=access_token, httponly=True)
    #manager.set_cookie(response, access_token)
    #return {'token': access_token}
    return rr


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("access-token", domain="localhost")
    return response

