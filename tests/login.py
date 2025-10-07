import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_login():
    with httpx.Client(follow_redirects=True) as client:
        # регистрация
        register_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "type": "candidate"
        }
        r = client.post(f"{BASE_URL}/auth/register-form", data=register_data)
        print("Register:", r.status_code, r.url)

        # логин
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        r = client.post(f"{BASE_URL}/auth/login-form", data=login_data)
        print("Login:", r.status_code, r.url)
        print("Cookies:", client.cookies)

        # доступ к главной странице
        r = client.get(f"{BASE_URL}/")
        print("Main page:", r.status_code)
        print(r.text[:500])

# Вызов функции теста
if __name__ == "__main__":
    test_login()
