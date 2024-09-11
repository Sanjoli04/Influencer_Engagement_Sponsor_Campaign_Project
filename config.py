class Config:
    DEBUG = False
    TESTING = False

class DevelopementConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///IESCP2.sqlite3'
    SECRET_KEY = "mysecret"
    SECURITY_PASSWORD_SALT = "saltistasty"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authenticated-Token"
    UPLOAD_FOLDER = 'static/uploads'
    SECURITY_LOGIN_URL  = '/user-login'
    SECURITY_LOGIN_USER_TEMPLATE = "signup_or_login.html"
    # CACHE_TYPE = 'simple'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = "spheresponsor@gmail.com"
    # MAIL_PASSWORD = "wyzx wsjn wyfp hadh"
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
# secret key is for the session and flask_security is build on flask_login and flask_login uses the session.