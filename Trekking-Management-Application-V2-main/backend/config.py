import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = "it-is-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "it-is-secret"

    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

  
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM = os.environ.get("MAIL_FROM", "noreply@trekking.local")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@trekking.com")
    GCHAT_WEBHOOK_URL = os.environ.get("GCHAT_WEBHOOK_URL")
    EXPORT_DIR = "exports"
