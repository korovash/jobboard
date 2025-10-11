#app/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import engine, Base, get_db
from .routers import auth, jobs, candidates
from .auth_utils import get_current_user_obj, user_obj_to_dict
from sqlalchemy.orm import Session
import os
from .logging_config import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Jobboard')

app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name='static')
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    user_obj = get_current_user_obj(request, db)
    user = None
    if user_obj:
        user = user_obj_to_dict(user_obj)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
