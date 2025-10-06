# копировать проект
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# настроить DATABASE_URL в env
# запустить
uvicorn app.main:app --reload