# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db, user)

@router.post('/login')
def login(data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, data.email)
    if not db_user or not pwd_context.verify(data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    return {"msg": "ok", "user_id": db_user.id}