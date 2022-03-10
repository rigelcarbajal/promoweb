from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, File, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4


class ItemSchema(BaseModel):
    id: UUID                = Field(default_factory=uuid4)
    sku: str                = Field(...)
    father_sku: str
    name: str
    category: str
    item_type: str
    brand: str
    color: str
    price: float
    description: str
    weight: float
    material: str
    measure: str
    size: str
    composition: str
    print_area: str
    print_technique: str
    capacity: str
    supplier: str
    stars: int
    tissue: str
    sex: str
    is_active: bool         = Field(default_factory=True)
    updated_at: datetime    = Field(default_factory=datetime.utcnow)
    created_at: datetime    = Field(default_factory=datetime.utcnow)

    











