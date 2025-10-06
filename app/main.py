# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import engine, Base
from .routers import auth, jobs, candidates
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Jobboard')

# Static files
app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name='static')

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})