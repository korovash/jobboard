# app/auth_utils.py
from itsdangerous import URLSafeSerializer
from fastapi import Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models
from .database import get_db
from typing import Optional

SECRET_KEY = "CHANGE_THIS_TO_RANDOM_STRING"
serializer = URLSafeSerializer(SECRET_KEY, salt="cookie-session")
COOKIE_NAME = "jobboard_session"

def create_session_cookie(response: Response, user_id: int):
    data = serializer.dumps({"user_id": user_id})
    response.set_cookie(COOKIE_NAME, data, httponly=True, max_age=3600*24, samesite="lax")

def get_current_user_obj(request: Request, db: Session) -> Optional[models.User]:
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return None
    try:
        data = serializer.loads(cookie)
        user_id = data.get("user_id")
        return crud.get_user(db, user_id)
    except Exception:
        return None

def user_obj_to_dict(user_obj: models.User) -> dict:
    if not user_obj:
        return None
    return {
        "authenticated": True,
        "id": user_obj.id,
        "full_name": user_obj.full_name,
        "email": user_obj.email,
        "type": user_obj.type.value if hasattr(user_obj.type, "value") else str(user_obj.type)
    }

# Dependency for endpoints (raises 401 if no user)
def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    user = get_current_user_obj(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Role-check dependencies
def require_candidate(current_user: models.User = Depends(get_current_user)):
    if (current_user.type.value if hasattr(current_user.type, "value") else str(current_user.type)) != "candidate":
        raise HTTPException(status_code=403, detail="Requires candidate role")
    return current_user

def require_recruiter(current_user: models.User = Depends(get_current_user)):
    if (current_user.type.value if hasattr(current_user.type, "value") else str(current_user.type)) != "recruiter":
        raise HTTPException(status_code=403, detail="Requires recruiter role")
    return current_user

def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
