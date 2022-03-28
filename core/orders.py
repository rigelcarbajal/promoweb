from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, File, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4


class OrderSchema(BaseModel):
    id: UUID
    folio: str
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime
    client_id: str
    user_id: str
    class config:
        schema_extra = {
            "example": {

            }
        }



