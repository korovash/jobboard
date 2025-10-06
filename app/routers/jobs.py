# app/routers/jobs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix='/jobs', tags=['jobs'])

@router.post('/', response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, recruiter_id: int, db: Session = Depends(get_db)):
    # recruiter_id — в реале берём из токена
    return crud.create_job(db, recruiter_id, job)

@router.get('/', response_model=list[schemas.JobOut])
def get_jobs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_jobs(db, skip, limit)