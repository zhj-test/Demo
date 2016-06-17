#coding:utf-8
from flask import Blueprint

testManage = Blueprint('testManage', __name__)

from . import views, errors
