import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_login():
    with httpx.Client(follow_redirects=True) as client:
        # 1. Попробуем регистрацию (если есть форма регистрации)
        register_data = {
            "email": "testuser1@example.com",
            "password": "testpassword"
        }
        r = client.post(f"{BASE_URL}/auth/register-form", data=register_data)
        print("Register:", r.status_code, r.url)

        # 2. Логин
        login_data = {
            "email": "testuser1@example.com",
            "password": "testpassword"
        }
        r = client.post(f"{BASE_URL}/auth/login-form", data=login_data)
        print("Login:", r.status_code, r.url)
        print("Cookies:", client.cookies)

        # 3. Доступ к главной странице
        r = client.get(f"{BASE_URL}/")
        print("Main page:", r.status_code)
        print(r.text[:500])  # первые 500 символов HTML
