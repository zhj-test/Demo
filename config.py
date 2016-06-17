#coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    APP_MAIL_SUBJECT_PREFIX = '[SnailApp]'
    APP_MAIL_SENDER = 'App Admin <pythontest2014@126.com>'
    APP_ADMIN = 'Snail'
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'pythontest2014@126.com'
    MAIL_PASSWORD = '20010237'
    #about log
    LOG_LEVEL = 0
    LOG_FILE_PATH = os.path.join(basedir, 'log', 'Snail.log')
    LOG_MAX_SIZE = 10*1024*1024
    LOG_BACKUP_COUNT = 5
    FILE_LOG_LEVEL = 10
    STREAM_LOG_LEVEL = 30
    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    @classmethod
    def init_app(cls, app):
        #处理代理服务器首部
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'product': ProductionConfig,
        'default': ProductionConfig,
        }

DBConnectConstants = {
        'OracleDuoBao': {
            'TYPE': 'Oracle',
            'DBINFO': 'duobao_app/duobao_appd3M8@10.120.240.252:9538/oratest',
            },
        'OraclePK': {
            'TYPE': 'Oracle',
            'DBINFO': 'duobao_pk/duobaopkd3M8@10.120.240.252:9538/oratest',
            },

        'MySQLMQ': {
            'TYPE': 'mysql',
            'DBINFO':{
                'host': '10.120.240.252',
                'port': 3309,
                'user': 'lott_mq',
                'password': 'dsd##8&!',
                'db': 'lott_mq',
                'charset': 'utf8',
                },
            }
        }
RedisInfo = {
        'host': '10.120.241.15',
        'password': '1qaz2wsx!~',
        }
