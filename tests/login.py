# tests/login.py
import httpx
from itsdangerous import URLSafeSerializer

BASE_URL = "http://127.0.0.1:8000"
SECRET_KEY = "CHANGE_THIS_TO_RANDOM_STRING"  # Должен совпадать с тем, что в auth_utils.py
COOKIE_NAME = "jobboard_session"

def run_test():
    register_data = {
        "email": "testuser01@example.com",
        "password": "testpassword",
        "full_name": "Test User",
        "type": "candidate"   # обязательно, т.к. форма требует type
    }
    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }

    with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
        r = client.post("/auth/register-form", data=register_data)
        print("Register:", r.status_code, r.url)

        r = client.post("/auth/login-form", data=login_data)
        print("Login:", r.status_code, r.url)
        print("Client cookies after login:", client.cookies)

        # проверим, есть ли cookie
        if COOKIE_NAME in client.cookies:
            print("Session cookie present.")
            s = URLSafeSerializer(SECRET_KEY, salt="cookie-session")
            try:
                data = s.loads(client.cookies[COOKIE_NAME])
                print("Decoded cookie data:", data)
            except Exception as e:
                print("Failed to decode cookie:", e)
        else:
            print("Session cookie NOT present.")

        # Получим главную
        r = client.get("/")
        print("Main page:", r.status_code)
        print(r.text[:400])

if __name__ == "__main__":
    run_test()
