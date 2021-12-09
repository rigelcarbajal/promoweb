from enum import Enum
from uuid import uuid4

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field, UUID4
from decouple import config
from starlette.routing import Router

from .database import db_user


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# User Model - Enum - Areas
class UserArea(str, Enum):
    administration = 'Administración'
    adviser = 'Asesor Externo'
    sales = 'Ventas'
    production = 'Producción'
    accounting = 'Contabilidad'
    systems = 'TI'
    management = 'Gerencia'
    rrhh = 'Recursos Humanos'
    admin = 'admin'

# User Model - Enum - Type
class UserType(str, Enum):
    fullTime = 'Tiempo Completo'
    midTime = 'Medio Tiempo'
    intership = 'Pasantía'
    byFee = 'Por honorarios'

# Model of User
class UserSchema(BaseModel):
    key: str 
    name: str = Field(...)
    password: str = Field(...)
    area: UserArea
    type: UserType
    phone: str
    email: EmailStr
    curp: str = Field(...)
    rfc: str

    class Config:
        schema_extra = {
            "example": {
                "key": "GUCR900305",
                "name": "Rigel David Gutiérrez Carbajal",
                "password": "qwerty123",
                "area": "TI",
                "type": "Tiempo Completo",
                "phone": "4521072166",
                "email": "rigel.gc@icloud.com",
                "curp": "GUCR900305HMNTRG01",
                "rfc": "GUCR900305UT1"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error, 
        "code": code,
        "message": message
        }

# -------> CRUD OPERATIONS

async def user_exist(key: str) -> bool:
    user =  db_user.fetch({"key": key})
    print(user[0]) # error here
    if user: 
        return True 
    else: 
        return False


@router.post("/users", response_description="Create new user")
async def add_user(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user["key"] = user["curp"][:10]
    print(user["key"])
    exist = await user_exist(user["key"])
    if exist:
        return ErrorResponseModel("Error", 301, "User already exist.")
    else:
        db_user.insert(user)
        
    return ResponseModel(user, "User created")


@router.get("/users/{key}", response_description="Get especific user")
async def get_user(key: str):
    user = await db_user.get(key)
    if user:
        return user
    return {"An error occurred.": "404 User not found"}


