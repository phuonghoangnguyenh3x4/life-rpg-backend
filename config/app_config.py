from dotenv import load_dotenv
import os
import base64

load_dotenv()

class AppConfig:
    DB_URL = os.getenv("DB_URL")
    SECRET_KEY = base64.b64decode(os.getenv("SECRET_KEY"))
    JWT_EXPIRATION_HOURS = 720
    COOKIE_SECURE = True
    COOKIE_HTTPONLY = True
    COOKIE_SAMESITE = 'none'