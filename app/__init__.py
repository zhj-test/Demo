#coding:utf-8
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
import os
#from .Log import Log

#log = Log.getLogger()
bootstrap = Bootstrap()
db = SQLAlchemy()

def GetBasePath():
    basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return basePath

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .testManage import testManage as testManage_blueprint
    app.register_blueprint(testManage_blueprint)
    from .duobaoTools import duobaoTools as duobaoTools_blueprint
    app.register_blueprint(duobaoTools_blueprint)
    return app
