#coding:utf-8
from . import main
from flask import render_template
from .. import db

@main.route('/')
def index():
    return render_template('index.html')
