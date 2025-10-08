# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Users
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed, full_name=user.full_name, type=user.type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if user.type == schemas.UserType.candidate:
        cand = models.Candidate(user_id=db_user.id)
        db.add(cand)
        db.commit()
    else:
        rec = models.Recruiter(user_id=db_user.id)
        db.add(rec)
        db.commit()
    return db_user

# Jobs
def create_job(db: Session, recruiter_id: int, job: schemas.JobCreate):
    db_job = models.Job(title=job.title, description=job.description, category=job.category, location=job.location, posted_by=recruiter_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def list_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()

# Candidate resume
def update_resume(db: Session, candidate_id: int, data: schemas.CandidateCreate):
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        return None
    if data.resume is not None:
        cand.resume = data.resume
    if data.skills is not None:
        cand.skills = data.skills
    db.add(cand)
    db.commit()
    db.refresh(cand)
    return cand

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def list_candidates(db: Session, skip: int = 0, limit: int = 50):
    # возвращаем User ORM-объекты соискателей
    return db.query(models.User).filter(models.User.type == models.UserType.candidate).offset(skip).limit(limit).all()

def get_candidate_by_user_id(db: Session, user_id: int):
    return db.query(models.Candidate).filter(models.Candidate.user_id == user_id).first()