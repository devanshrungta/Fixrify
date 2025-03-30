import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Admin
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@fixrify.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'

    # CORS Settings
    CORS_ORIGINS = ['*']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials']
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ['Content-Range', 'X-Content-Range']

    # Redis settings
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300

    # Celery settings
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://172.17.0.1:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://172.17.0.1:6379/0'

    # Email settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or '172.17.0.1'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 1025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@fixrify.com'

    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}

    # Google Chat Webhook settings
    GOOGLE_CHAT_WEBHOOK_URL = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL') 