# app/routers/jobs.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from fastapi.templating import Jinja2Templates
import os
from ..auth_utils import get_current_user, require_recruiter, user_obj_to_dict

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))
router = APIRouter(prefix='/jobs', tags=['jobs'])

@router.get('/', response_model=list[schemas.JobOut])
def get_jobs(request: Request, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    jobs = crud.list_jobs(db, skip, limit)
    # рендер html или возвращаем json если запрос API (для простоты рендерим HTML)
    return templates.TemplateResponse('jobs_list.html', {'request': request, 'jobs': jobs, 'user': None})

@router.get('/new')
def new_job_form(request: Request, current_user = Depends(require_recruiter)):
    # показать форму создания вакансии
    user = user_obj_to_dict(current_user)
    return templates.TemplateResponse('job_form.html', {'request': request, 'user': user})

@router.post('/new')
def create_job_form(request: Request,
                    title: str = Form(...),
                    description: str = Form(None),
                    category: str = Form(None),
                    location: str = Form(None),
                    db: Session = Depends(get_db),
                    current_user = Depends(require_recruiter)):
    job_in = schemas.JobCreate(title=title, description=description, category=category, location=location)
    # recruiter_id: нужно взять id работодателя (recruiter table)
    # В простом варианте используем recruiter.user_id mapping: найдём Recruiter by user_id
    recruiter = db.query(crud.models.Recruiter).filter(crud.models.Recruiter.user_id == current_user.id).first()
    if not recruiter:
        # В реале — создать профиль рекрутера, но для краткости:
        raise Exception("Recruiter profile not found")
    job = crud.create_job(db, recruiter.id, job_in)
    return RedirectResponse(url='/jobs', status_code=303)
