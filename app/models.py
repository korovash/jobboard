# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import enum
import datetime


class UserType(enum.Enum):
    candidate = 'candidate'
    recruiter = 'recruiter'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    type = Column(Enum(UserType), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


candidate = relationship('Candidate', uselist=False, back_populates='user')
recruiter = relationship('Recruiter', uselist=False, back_populates='user')


class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    resume = Column(Text)
    skills = Column(String)
    user = relationship('User', back_populates='candidate')


class Recruiter(Base):
    __tablename__ = 'recruiters'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    company = Column(String)
    user = relationship('User', back_populates='recruiter')


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    location = Column(String)
    posted_by = Column(Integer, ForeignKey('recruiters.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    recruiter = relationship('Recruiter')