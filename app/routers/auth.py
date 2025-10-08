#app/routers/auth.py
from fastapi import APIRouter, Depends, Request, Form, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from fastapi.templating import Jinja2Templates
import os
from passlib.context import CryptContext
from ..auth_utils import create_session_cookie, logout

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))
router = APIRouter(prefix='/auth', tags=['auth'])

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

# render pages
@router.get('/register')
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request, 'user': {'authenticated': False}})

@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request, 'user': {'authenticated': False}})

# form handlers
@router.post('/register-form')
def register_form(request: Request,
                  email: str = Form(...),
                  password: str = Form(...),
                  full_name: str = Form(None),
                  type: str = Form(...),
                  db: Session = Depends(get_db)):
    try:
        user_type = schemas.UserType(type)
    except Exception:
        return templates.TemplateResponse('register.html', {'request': request, 'error': 'Неверный тип пользователя', 'user': {'authenticated': False}})

    if crud.get_user_by_email(db, email):
        return templates.TemplateResponse('register.html', {'request': request, 'error': 'Email уже занят', 'user': {'authenticated': False}})

    user_in = schemas.UserCreate(email=email, password=password, full_name=full_name, type=user_type)
    crud.create_user(db, user_in)
    # После регистрации редиректим на страницу логина
    return RedirectResponse(url='/auth/login', status_code=303)


@router.post('/login-form')
def login_form(request: Request,
               email: str = Form(...),
               password: str = Form(...),
               db: Session = Depends(get_db)):
    """
    Обратите внимание: мы создаём RedirectResponse, **ставим cookie на этот объект**
    и возвращаем его. Это гарантирует, что Set-Cookie попадёт в клиент.
    """
    db_user = crud.get_user_by_email(db, email)
    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Неверные учетные данные', 'user': {'authenticated': False}})

    redirect = RedirectResponse(url='/', status_code=303)
    create_session_cookie(redirect, db_user.id)
    return redirect


@router.get("/logout")
def logout_user():
    redirect = RedirectResponse("/", status_code=303)
    logout(redirect)
    return redirect