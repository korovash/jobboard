# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
import enum
import datetime

class UserType(str, enum.Enum):
    candidate = 'candidate'
    recruiter = 'recruiter'

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]
    type: UserType

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    type: UserType
    class Config:
        orm_mode = True

class CandidateCreate(BaseModel):
    resume: Optional[str]
    skills: Optional[str]

class JobCreate(BaseModel):
    title: str
    description: Optional[str]
    category: Optional[str]
    location: Optional[str]

class JobOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    location: Optional[str]
    posted_by: Optional[int]
    created_at: datetime.datetime
    class Config:
        orm_mode = True