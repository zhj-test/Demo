#coding:utf-8
from flask import Blueprint

duobaoTools = Blueprint('duobaoTools', __name__)

from . import views, errors
