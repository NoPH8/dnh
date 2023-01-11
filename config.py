import pathlib

from decouple import config
from flask_security import uia_username_mapper

BASE_DIR = pathlib.Path(__file__).parent


def str_to_list(value):
    return [d for d in [s.strip() for s in value.split(' ')] if d]


class AppConfig:
    # Common settings
    APP_NAME = config('APP_NAME', default='DNH')
    DNS_SERVERS = config('DNS_SERVERS', cast=str_to_list, default='')
    DNS_UPDATE_INTERVAL = config('DNS_UPDATE_INTERVAL', cast=int, default=15)  # in minutes

    # Database settings
    DB_NAME = config('DB_NAME', default='database.sqlite')
    DB_PATH = pathlib.Path.joinpath(BASE_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask admin settings
    FLASK_ADMIN_SWATCH = 'cerulean'

    # Flask security settings
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = '/admin/change-password/'
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_LOGIN_URL = '/admin/login/'
    SECURITY_LOGOUT_URL = '/admin/logout/'
    SECURITY_POST_LOGIN_VIEW = '/admin/'
    SECURITY_POST_LOGOUT_VIEW = '/admin/'
    SECURITY_REGISTERABLE = False
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {'username': {'mapper': uia_username_mapper, 'case_insensitive': True}},
    ]

    # Generate a nice key using 'make generate-secret-key'
    SECRET_KEY = config('SECRET_KEY')
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a nice key using 'make generate-secret-salt'
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT')


class AppConfigTesting(AppConfig):
    DB_NAME = 'database.sqlite.test'
    DB_PATH = pathlib.Path.joinpath(BASE_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

    SECURITY_PASSWORD_HASH = 'plaintext'

    TESTING = True
