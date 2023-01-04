import pathlib

from decouple import config

from app.utils import uia_username_mapper

BASE_DIR = pathlib.Path(__file__).parent


class AppConfig:
    # Common settings
    APP_NAME = config('APP_NAME', default='DNH')

    # Database settings
    DB_NAME = config('DB_NAME', default='database.sqlite')
    DB_PATH = pathlib.Path.joinpath(BASE_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Development settings
    DEBUG = config('DEBUG', cast=bool, default=False)

    # Flask admin settings
    FLASK_ADMIN_SWATCH = 'cerulean'

    # Flask security settings
    SECURITY_LOGIN_URL = '/admin/login/'
    SECURITY_LOGOUT_URL = '/admin/logout/'
    SECURITY_POST_LOGIN_VIEW = '/admin/'
    SECURITY_POST_LOGOUT_VIEW = '/admin/'
    SECURITY_REGISTERABLE = False
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {'username': {'mapper': uia_username_mapper, 'case_insensitive': True}},
    ]

    # TODO: Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = config('SECRET_KEY')
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # TODO: Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT')
