# tests/login_debug.py
import httpx
from itsdangerous import URLSafeSerializer

BASE_URL = "http://127.0.0.1:8000"
COOKIE_NAME = "jobboard_session"
SECRET_KEY = "CHANGE_THIS_TO_RANDOM_STRING"  # тот же, что в auth_utils.py

def run_debug():
    register_data = {
        "email": "testuser01@example.com",
        "password": "testpassword",
        "full_name": "Test User",
        "type": "candidate"
    }
    login_data = {"email": register_data["email"], "password": register_data["password"]}

    with httpx.Client(base_url=BASE_URL) as client:
        r = client.post("/auth/register-form", data=register_data, follow_redirects=False)
        print("Register:", r.status_code, "headers:", dict(r.headers))
        # попробуем логин без follow_redirects чтобы увидеть 303 и Set-Cookie
        r = client.post("/auth/login-form", data=login_data, follow_redirects=False)
        print("Login (no-follow):", r.status_code)
        print("Login headers:", dict(r.headers))
        if "set-cookie" in r.headers:
            print("Set-Cookie present in login response")
        else:
            print("Set-Cookie NOT present in login response")

        # покажем cookies, даже если без редиректа
        print("Client cookies after no-follow login:", client.cookies)

        # теперь вручную follow редирект: если есть Location — GET туда, сохраняя client
        location = r.headers.get("location")
        if location:
            print("Following location:", location)
            r2 = client.get(location)
            print("Followed GET status:", r2.status_code)
            print("Client cookies after following:", client.cookies)

        # если cookie есть — попробуем декодировать
        if COOKIE_NAME in client.cookies:
            s = URLSafeSerializer(SECRET_KEY, salt="cookie-session")
            try:
                data = s.loads(client.cookies[COOKIE_NAME])
                print("Decoded cookie payload:", data)
            except Exception as e:
                print("Failed to decode cookie:", e)
        else:
            print("No session cookie in client.cookies")

if __name__ == "__main__":
    run_debug()
