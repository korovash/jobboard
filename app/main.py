from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import engine, Base, get_db
from .routers import auth, jobs, candidates
from .auth_utils import get_current_user
from sqlalchemy.orm import Session
import os
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Jobboard')

# Static files
app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name='static')

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    user_obj = get_current_user(request, db)
    user = None
    if user_obj:
        user = {
            "authenticated": True,
            "id": user_obj.id,
            "full_name": user_obj.full_name,
            "type": user_obj.type.value if hasattr(user_obj.type, "value") else str(user_obj.type)
        }
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
