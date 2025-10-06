# app/routers/candidates.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
import models

router = APIRouter(prefix='/candidates', tags=['candidates'])

@router.put('/{candidate_id}/resume')
def update_resume(candidate_id: int, data: schemas.CandidateCreate, db: Session = Depends(get_db)):
    cand = crud.update_resume(db, candidate_id, data)
    if not cand:
        raise HTTPException(status_code=404, detail='Candidate not found')
    return cand

@router.get('/', response_model=list[schemas.UserOut])
def list_candidates(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.type==models.UserType.candidate).offset(skip).limit(limit).all()
    return users