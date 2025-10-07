import httpx

BASE_URL = "http://127.0.0.1:8000"

# Данные для тестового пользователя
LOGIN_DATA = {
    "username": "testuser",
    "password": "testpassword"
}

with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
    # Шаг 1: Попробуем зарегистрировать пользователя (если ещё не зарегистрирован)
    register_data = {
        "username": LOGIN_DATA["username"],
        "email": "test@example.com",
        "password": LOGIN_DATA["password"]
    }
    resp = client.post("/auth/register-form", data=register_data)
    print("Register:", resp.status_code, resp.url)

    # Шаг 2: Логинимся
    resp = client.post("/auth/login-form", data=LOGIN_DATA)
    print("Login:", resp.status_code, resp.url)

    # Шаг 3: Проверяем доступ к защищённой странице
    resp = client.get("/")
    print("Main page:", resp.status_code)
    print("Cookies:", client.cookies)

    # Если сервер возвращает HTML, можно вывести первые 300 символов
    print(resp.text[:300])
