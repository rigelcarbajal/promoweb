from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from dependencies import templates
from .database import db_user

from .security.auth import manager

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user = Depends(manager)):
    return templates.TemplateResponse("/pages/dashboard.html", {"request": request, "user": user, "dbusers": db_user})

@router.get("/products", response_class=HTMLResponse)
async def products(request: Request, user = Depends(manager)):
    return templates.TemplateResponse("/pages/products.html", {"request": request, "user": user})


@router.get("/customers", response_class=HTMLResponse)
async def customers(request: Request, user = Depends(manager)):
    return templates.TemplateResponse("/pages/customers.html", {"request": request, "user": user})



