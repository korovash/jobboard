#app/auth_utils.py
from itsdangerous import URLSafeSerializer
from fastapi import Request, Response
from . import crud, models

SECRET_KEY = "CHANGE_THIS_TO_RANDOM_STRING"  # замени на что-то секретное
serializer = URLSafeSerializer(SECRET_KEY, salt="cookie-session")

COOKIE_NAME = "jobboard_session"

def create_session_cookie(response: Response, user_id: int):
    data = serializer.dumps({"user_id": user_id})
    response.set_cookie(
        COOKIE_NAME,
        data,
        httponly=True,
        max_age=3600*24,  # 1 день
        samesite="lax"
    )

def get_current_user(request: Request, db) -> models.User | None:
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return None
    try:
        data = serializer.loads(cookie)
        user_id = data.get("user_id")
        user = crud.get_user(db, user_id)
        return user
    except Exception:
        return None

def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
