#coding:utf-8
from flask.ext.wtf import Form
from wtforms import SubmitField, StringField, ValidationError, TextAreaField
from wtforms.validators import Required
from ..models import Project, Suite

class ModifyProjectForm(Form):
    projectName = StringField('项目名称', validators=[Required()])
    folderName = StringField('项目文件夹', validators=[Required()])
    remark = TextAreaField('备注')
    submit = SubmitField('提交')

class AddProjectForm(ModifyProjectForm):
    def validate_projectName(self, field):
        if Project.query.filter_by(projectName=field.data).first():
            raise ValidationError('已有相同的项目名')

    def validate_folderName(self, field):
        if Project.query.filter_by(folderName=field.data).first():
            raise ValidationError('已有相同的项目文件夹')

class ModifyModuleForm(Form):
    moduleName = StringField('模块名称', validators=[Required()])
    fileName = StringField('文件名称', validators=[Required()])
    className = StringField('类名', validators=[Required()])
    remark = TextAreaField('备注')
    submit = SubmitField('提交')

class AddModuleForm(ModifyModuleForm):
    def __init__(self, moduleNameList, fileNameList):
        super(AddModuleForm, self).__init__()
        self.moduleNameList = moduleNameList
        self.fileNameList = fileNameList

    def validate_moduleName(self, field):
        if field.data in self.moduleNameList:
            raise ValidationError('该项目下已有相同的模块名')

    def validate_fileName(self, field):
        if field.data in self.fileNameList:
            raise ValidationError('该项目下已有相同的文件名')

class ModifyTestCaseForm(Form):
    caseName = StringField('用例名称', validators=[Required()])
    funcName = StringField('方法名称', validators=[Required()])
    params = StringField('参数(以|分隔)')
    remark = TextAreaField('备注')
    submit = SubmitField('提交')

class AddTestCaseForm(ModifyTestCaseForm):
    def __init__(self, caseNameList, funcNameList):
        super(AddTestCaseForm, self).__init__()
        self.caseNameList = caseNameList
        self.funcNameList = funcNameList
    def validate_caseName(self, field):
        if field.data in self.caseNameList:
            raise ValidationError('该模块下已有相同的用例名')
    def validata_funcName(self, field):
        if field.data in self.funcNameList:
            raise ValidationError('该模块下已有相同的方法名')

class ModifyDataForm(Form):
    dataName = StringField('数据名称', validators=[Required()])
    values = StringField('传入值(以|分隔)')
    tags = StringField('标签')
    remark = TextAreaField('备注')
    submit = SubmitField('提交')

class AddDataForm(ModifyDataForm):
    def __init__(self, dataNameList):
        super(AddDataForm, self).__init__()
        self.dataNameList = dataNameList

    def validate_dataName(self, field):
        if field.data in self.dataNameList:
            raise ValidationError('该用例下已有相同的测试数据名')

class suiteForm(Form):
    suiteName = StringField('测试集名称', validators=[Required()])
    remark = TextAreaField('备注')
