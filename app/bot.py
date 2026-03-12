from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask
from flask.sessions import SecureCookieSessionInterface
import requests
import time

BASE_URL = "http://localhost:3000"

def make_admin_session_cookie() -> str:
    tmp_app = Flask(__name__)
    tmp_app.secret_key = "supersecretkey_fixed"
    with tmp_app.test_request_context():
        serializer = SecureCookieSessionInterface().get_signing_serializer(tmp_app)
        return serializer.dumps({"is_admin": True})

def register_admin_cookie(session_val: str):
    resp = requests.get(
        f"{BASE_URL}/internal/set-admin-cookie",
        params={"value": session_val}
    )
    print(f"[bot] registered: {resp.text}")

def make_driver(session_val: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(options=options)
    driver.get(f"{BASE_URL}/")
    driver.add_cookie({
        "name": "session",
        "value": session_val,
        "path": "/"
    })
    return driver

def run():
    print("[bot] starting...")
    time.sleep(3)  

    session_val = make_admin_session_cookie()
    register_admin_cookie(session_val)

    driver = make_driver(session_val)
    print("[bot] ready, starting patrol...")

    while True:
        try:
            driver.get(f"{BASE_URL}/search?city=Seoul")
            print("[bot] visited /search")
        except Exception as e:
            print(f"[bot] error: {e}, restarting driver...")
            driver = make_driver(session_val)
        time.sleep(10)

if __name__ == "__main__":
    run()