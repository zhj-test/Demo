#coding:utf-8
from . import db
import datetime

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(64), unique=True, index=True)
    folderName = db.Column(db.String(64), unique=True)
    remark = db.Column(db.Text())

    modules = db.relationship('Module', backref='project')

    def __repr__(self):
        return '<Project %r>' % self.projectName

class Module(db.Model):
    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True)
    moduleName = db.Column(db.String(64), index=True)
    fileName = db.Column(db.String(64))
    className = db.Column(db.String(64))
    remark = db.Column(db.Text())

    projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
    testCases = db.relationship('TestCase', backref='module')

    def __repr__(self):
        return '<Module %r>' % self.moduleName

class TestCase(db.Model):
    __tablename__ = 'testCase'
    id = db.Column(db.Integer, primary_key=True)
    caseName = db.Column(db.String(64), index=True)
    funcName = db.Column(db.String(64))
    params = db.Column(db.Text())
    remark = db.Column(db.Text())

    moduleId = db.Column(db.Integer, db.ForeignKey('module.id'))
    datas = db.relationship('Data', backref='testCase')

    def __repr__(self):
        return '<testCase %r>' % self.caseName

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    dataName = db.Column(db.String(64))
    values = db.Column(db.Text())
    tags = db.Column(db.Text())
    remark = db.Column(db.Text())

    testCaseId = db.Column(db.Integer, db.ForeignKey('testCase.id'))

suiteData = db.Table('suiteData',
        db.Column('suiteId', db.Integer, db.ForeignKey('suite.id')),
        db.Column('dataId', db.Integer, db.ForeignKey('data.id')),)

class Suite(db.Model):
    __tablename__ = 'suite'
    id = db.Column(db.Integer, primary_key=True)
    suiteName = db.Column(db.String(64), unique=True, index=True)
    remark = db.Column(db.Text())

    testReports = db.relationship('TestReport', backref='suite')
    datas = db.relationship('Data', secondary=suiteData,
            backref=db.backref('suites', lazy='dynamic'),
            lazy='dynamic')

    def __repr__(self):
        return '<Suite %r>' % self.suiteName

class TestReport(db.Model):
    __tablename__ = 'testReport'
    id = db.Column(db.Integer, primary_key=True)
    reportFile = db.Column(db.String(64))
    passNum = db.Column(db.Integer)
    failedNum = db.Column(db.Integer)
    errorNum = db.Column(db.Integer)
    remark = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    suiteId = db.Column(db.Integer, db.ForeignKey('suite.id'))

    def __repr__(self):
        return '<TestReport %r>' % self.id
