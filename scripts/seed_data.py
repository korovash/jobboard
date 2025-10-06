# scripts/seed_data.py
from app.database import SessionLocal, engine
from app import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
# Простейшие тестовые данные
user1 = schemas.UserCreate(email='alice@example.com', password='secret', full_name='Alice', type=schemas.UserType.candidate)
user2 = schemas.UserCreate(email='bob@company.com', password='secret', full_name='Bob', type=schemas.UserType.recruiter)

crud.create_user(db, user1)
re = crud.create_user(db, user2)
# найдём recruiter id
rec = db.query(models.Recruiter).join(models.User).filter(models.User.email==user2.email).first()

job1 = schemas.JobCreate(title='Python Developer', description='Работа с backend', category='backend', location='Helsinki')
crud.create_job(db, rec.id, job1)

print('seed done')