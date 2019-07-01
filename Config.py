# import pymysql


class TestingConfig:
    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = 'BD88xTI0gNYkVpLY'
    SECRET_KEY = 'BD88xTI0gNYkVpLY'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = int('465') or int('994')
    MAIL_USE_TLS = 'true'.lower() in ['true', 'on', '1']
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'admin'
    PASSWORD = '7251998MySql+'
    HOST = '192.168.253.134'
    PORT = '3306'
    DATABASE = 'mes_db'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    TESTING = True

    @staticmethod
    def init_app(app):
        pass


select_config = {
    'default': TestingConfig
}
