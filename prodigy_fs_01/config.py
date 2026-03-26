import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # simple SQLite for now
    SQLALCHEMY_TRACK_MODIFICATIONS = False