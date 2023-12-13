import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root@localhost/dss')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1234567890qwertyuiopasdfghkl'