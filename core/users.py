from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from decouple import config
from pydantic.types import UUID1

from .database import db_user
from .security.tools import get_password_hash
from .security.auth import manager

router = APIRouter(
    prefix="/user",
    tags=["user"],
    #user = Depends(manager)
)

# User Model - Enum - Areas
class UserArea(str, Enum):
    admin       = 'TI'
    adviser     = 'Asesor Externo'
    sales       = 'Ventas'
    management  = 'Gerencia'
    production  = 'Produccion'

# User Model - Enum - Type
class UserType(str, Enum):
    fullTime    = 'Tiempo Completo'
    midTime     = 'Medio Tiempo'
    intership   = 'Pasantia'
    byFee       = 'Honorarios'

# Model of Create User
class UserSchema(BaseModel):
    id: UUID                = Field(default_factory=uuid4)
    key: Optional[str]
    firstName: str          = Field(...)
    lastName: str           = Field(...)
    password: str           = Field(...)
    area: UserArea
    type: UserType
    phone: str
    email: EmailStr
    curp: str               = Field(...)
    rfc: str
    nss: int
    emergencyContact: str   = Field(...)
    emergencyPhone: str     = Field(...)
    is_active: bool         = Field(default_factory=True)
    updated_at: datetime    = Field(default_factory=datetime.utcnow)
    created_at: datetime    = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "firstName" : "Rigel David",
                "lastName"  : "Gutiérrez Carbajal",
                "password"  : "qwerty321",
                "area"      : "TI",
                "type"      : "Tiempo Completo",
                "phone"     : "4521072166",
                "email"     : "rigel.gc@outlook.com",
                "curp"      : "GUCR900305HMNTRG01",
                "rfc"       : "GUCR900305UT1",
                "nss"       : 2549865484,
                "emergencyContact": "Maria de la Luz",
                "emergencyPhone"  : "4521225158",
                "is_active" : True
            }
        }

# Model of Update User
class UpdateUserSchema(BaseModel):
    key: Optional[str] 
    firstName: str
    lastName: str
    password: str
    area: UserArea
    type: UserType
    phone: str
    email: EmailStr
    curp: str
    rfc: str
    nss: int
    emergencyContact: str
    emergencyPhone: str
    is_active: bool
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "firstName" : "Rigel David",
                "lastName"  : "Gutiérrez Carbajal",
                "password"  : "qwerty321",
                "area"      : "TI",
                "type"      : "Medio Tiempo",
                "phone"     : "4521072166",
                "email"     : "rigel.gc@outlook.com",
                "curp"      : "GUCR900305HMNTRG01",
                "rfc"       : "GUCR900305UT1",
                "nss"       : 2549865484,
                "emergencyContact": "Maria de la Luz",
                "emergencyPhone"  : "4521225158",
                "is_active" : False
            }
        }

# -------> CRUD OPERATIONS

async def user_exist(key: str):
    user = db_user.get(key)
    return user



@router.post("/", response_description="Create new user")
async def add_user(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user["curp"] = user["curp"].upper()
    user["key"] = user["curp"][:10]
    user["password"] = get_password_hash(user["password"])
    exist = await user_exist(user["key"])
    if exist:
        return HTTPException(status_code=403, detail="User already exist.")
    else:
        db_user.insert(user)
    return HTTPException(status_code=201, detail="User created.")



@router.put("/{key}", response_description="Update user.")
async def update_user(key: str, req: UpdateUserSchema = Body(...)):
    req = { k: v for k, v in req.dict().items() if v is not None }
    if len(req) < 1:
        return HTTPException(status_code=401, detail="Data doesn't exist.")
    user = await user_exist(key)
    if user:
        req["key"] = req["curp"][:10]
        req["password"] = get_password_hash(req["password"])
        req= jsonable_encoder(req)
        updated_user = db_user.put(req)
    if updated_user:
        return HTTPException(status_code=204, detail="User was updated.")
    return HTTPException(status_code=500, detail="Error updating user information.")



@router.get("/{key}", response_description="Get especific user.")
async def get_user(key: str):
    user = db_user.get(key)
    if user:
        return user
    return HTTPException(status_code=401, detail="User doesn't exist.")



@router.get("/", response_description="Get all users.")
async def get_all_users():
    users = db_user.fetch()
    if users:
        return users.items
    return HTTPException(status_code=201, detail="There aren't users yet.")



@router.delete("/{key}", response_description="Delete user.")
async def delete_user(key: str):
    user = get_user(key)
    if user:
        db_user.delete(key)
        return HTTPException(status_code=204, detail="User deleted successfully.")

