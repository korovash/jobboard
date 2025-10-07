# app/routers/auth.py  (добавить в текущий файл)
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from fastapi.templating import Jinja2Templates
import os
from passlib.context import CryptContext

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))
router = APIRouter(prefix='/auth', tags=['auth'])

# render pages
@router.get('/register')
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request, 'user': {'authenticated': False}})

@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request, 'user': {'authenticated': False}})

# form handlers (POST)
@router.post('/register-form')
def register_form(request: Request, email: str = Form(...), password: str = Form(...),
                  full_name: str = Form(None), type: str = Form(...), db: Session = Depends(get_db)):
    # сопоставление типа
    try:
        user_type = schemas.UserType(type)
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid user type')

    user_in = schemas.UserCreate(email=email, password=password, full_name=full_name, type=user_type)
    # обработка ошибок регистрации
    if crud.get_user_by_email(db, email):
        return templates.TemplateResponse('register.html', {'request': request, 'error': 'Email уже занят', 'user': {'authenticated': False}})

    user = crud.create_user(db, user_in)
    # После регистрации: можно редиректить на страницу логина
    return RedirectResponse(url='/auth/login', status_code=303)

@router.post('/login-form')
def login_form(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Используем простой check — в реале ставим сессии/JWT
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Неверные учетные данные', 'user': {'authenticated': False}})
    from passlib.context import CryptContext
    pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto"
    )

    if not pwd_context.verify(password, db_user.hashed_password):
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Неверные учетные данные', 'user': {'authenticated': False}})

    # TODO: поставить сессионную cookie или JWT. Пока — редиректим и передаём query param для демо
    redirect_url = '/?login=1&type=' + (db_user.type.value if hasattr(db_user.type, 'value') else str(db_user.type))
    return RedirectResponse(url=redirect_url, status_code=303)
