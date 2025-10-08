# app/routers/candidates.py
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from fastapi.templating import Jinja2Templates
import os
from ..auth_utils import get_current_user, require_candidate, require_recruiter, user_obj_to_dict
import logging

logger = logging.getLogger("jobboard.candidates")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))
router = APIRouter(prefix='/candidates', tags=['candidates'])


@router.get('/', response_model=list[schemas.UserOut])
def list_candidates_page(request: Request, db: Session = Depends(get_db), current_user = Depends(require_recruiter)):
    users = crud.list_candidates(db)
    user = user_obj_to_dict(current_user)
    return templates.TemplateResponse('candidates_list.html', {'request': request, 'users': users, 'user': user})


@router.get('/me/resume')
def my_resume_form(request: Request, db: Session = Depends(get_db), current_user = Depends(require_candidate)):
    cand = crud.get_candidate_by_user_id(db, current_user.id)
    user = user_obj_to_dict(current_user)
    return templates.TemplateResponse('resume_form.html', {'request': request, 'candidate': cand, 'user': user})


@router.post('/me/resume')
def my_resume_update(request: Request,
                     resume: str = Form(None),
                     skills: str = Form(None),
                     db: Session = Depends(get_db),
                     current_user = Depends(require_candidate)):
    try:
        cand = crud.get_candidate_by_user_id(db, current_user.id)
        if not cand:
            cand = models.Candidate(user_id=current_user.id)
            db.add(cand)
            db.commit()
            db.refresh(cand)

        data = schemas.CandidateCreate(resume=resume, skills=skills)
        crud.update_resume(db, cand.id, data)
        return RedirectResponse(url='/candidates/me/resume', status_code=303)
    except Exception as e:
        logger.exception("Failed to update resume for user %s: %s", getattr(current_user, "id", None), e)
        raise HTTPException(status_code=500, detail="Не удалось сохранить резюме")
