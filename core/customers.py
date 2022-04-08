from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from decouple import config

from .database import db_user
from .security.tools import get_password_hash
from .security.auth import manager


# Customer Model
class CustomerSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    




