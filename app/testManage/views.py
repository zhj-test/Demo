#coding:utf-8
from . import testManage
from flask import render_template, flash, redirect, url_for, request
from ..models import Project, Module, TestCase, Data, Suite, TestReport
from .forms import AddProjectForm, ModifyProjectForm, AddModuleForm, ModifyModuleForm, AddTestCaseForm, ModifyTestCaseForm, AddDataForm, ModifyDataForm, suiteForm
from .. import db
from .testEngine import TestEngine
import os

####################
# 测试管理平台首页
####################
@testManage.route('/testManage/')
def index():
    return render_template('/testManage/index.html')

####################
# 测试项目相关
####################
@testManage.route('/testManage/addProject/', methods=['GET', 'POST'])
def addProject():
    form = AddProjectForm()
    if form.validate_on_submit():
        project = Project(projectName=form.projectName.data, folderName=form.folderName.data, remark=form.remark.data)
        db.session.add(project)
        db.session.commit()
        flash('项目添加成功')
        return redirect(url_for('testManage.projectInfo', projectId=project.id))
    return render_template('/testManage/addProject.html', form=form)

@testManage.route('/testManage/modifyProject/<int:projectId>', methods=['GET', 'POST'])
def modifyProject(projectId):
    project = Project.query.get_or_404(projectId)
    projects = Project.query.all()
    projects.remove(project)
    form = ModifyProjectForm()
    form.projectName.data = project.projectName
    form.folderName.data = project.folderName
    form.remark.data = project.remark
    if form.validate_on_submit():
        if request.form.get('projectName') in [p.projectName for p in projects]:
            flash('已存在相同项目名')
            return redirect(url_for('testManage.modifyProject', projectId=projectId))
        if request.form.get('folderName') in [p.folderName for p in projects]:
            flash('已存在相同目录名')
            return redirect(url_for('testManage.modifyProject', projectId=projectId))
        project.projectName = request.form.get('projectName')
        project.folderName = request.form.get('folderName')
        project.remark = request.form.get('remark')
        db.session.add(project)
        flash('项目信息修改成功')
        return redirect(url_for('testManage.projectInfo', projectId=projectId))
    return render_template('/testManage/modifyProject.html', form=form, projectId=projectId)

@testManage.route('/testManage/projectInfo/<int:projectId>')
def projectInfo(projectId):
    project = Project.query.get_or_404(projectId)
    return render_template('/testManage/projectInfo.html', project=project)

@testManage.route('/testManage/projectList/')
def projectList():
    projects = Project.query.all()
    return render_template('/testManage/projectList.html', projects=projects)

@testManage.route('/testManage/deleteProject/<int:projectId>')
def deleteProject(projectId):
    project = Project.query.get_or_404(projectId)
    for module in project.modules:
        for testCase in module.testCases:
            for data in testCase.datas:
                for suite in Suite.query.all():
                    if data in suite.datas:
                        suite.datas.remove(data)
                    db.session.add(suite)
                db.session.delete(data)
            db.session.delete(testCase)
        db.session.delete(module)
    db.session.delete(project)
    try:
        db.session.commit()
        flash('项目信息及其包含的测试模块/用例/测试数据已删除完毕')
    except Exception as err:
        db.session.rollback()
        flash('删除失败')
        return redirect(url_for('testManage.projectInfo', projectId=projectId))
    return redirect(url_for('testManage.projectList'))
####################
# 模块相关
####################
@testManage.route('/testManage/project_<int:projectId>/addModule/', methods=['GET', 'POST'])
def addModule(projectId):
    project = Project.query.get_or_404(projectId)
    modules = project.modules
    moduleNameList = [module.moduleName for module in modules]
    fileNameList = [module.fileName for module in modules]
    form = AddModuleForm(moduleNameList, fileNameList)
    if form.validate_on_submit():
        module = Module(moduleName=form.moduleName.data, fileName=form.fileName.data,
                className=form.className.data, remark=form.remark.data, projectId=projectId)
        db.session.add(module)
        db.session.commit()
        flash('模块添加成功')
        return redirect(url_for('testManage.moduleInfo', moduleId=module.id))
    return render_template('/testManage/addModule.html', form=form, project=project)

@testManage.route('/testManage/modifyModule/<int:moduleId>', methods=['GET', 'POST'])
def modifyModule(moduleId):
    module = Module.query.get_or_404(moduleId)
    project = module.project
    modules = project.modules[:]
    modules.remove(module)
    form = ModifyModuleForm()
    form.moduleName.data = module.moduleName
    form.fileName.data = module.fileName
    form.className.data = module.className
    form.remark.data = module.remark
    if form.validate_on_submit():
        if request.form.get('moduleName') in [m.moduleName for m in modules]:
            flash('该项目下已有相同的模块名')
            return redirect(url_for('testManage.modifyModule', moduleId=moduleId))
        if request.form.get('fileName') in [m.fileName for m in modules]:
            flash('该项目下已有相同的文件名')
            return redirect(url_for('testManage.modifyModule', moduleId=moduleId))
        module.moduleName = request.form.get('moduleName')
        module.fileName = request.form.get('fileName')
        module.className = request.form.get('className')
        module.remark = request.form.get('remark')
        db.session.add(module)
        flash('模块信息修改成功')
        return redirect(url_for('testManage.moduleInfo', moduleId=moduleId))
    return render_template('/testManage/modifyModule.html', form=form, moduleId=moduleId)

@testManage.route('/testManage/moduleInfo/<int:moduleId>')
def moduleInfo(moduleId):
    module = Module.query.get_or_404(moduleId)
    return render_template('/testManage/moduleInfo.html', module=module)

@testManage.route('/testManage/deleteModule/<int:moduleId>')
def deleteModule(moduleId):
    module = Module.query.get_or_404(moduleId)
    for testCase in module.testCases:
        for data in testCase.datas:
            for suite in Suite.query.all():
                if data in suite.datas:
                    suite.datas.remove(data)
                db.session.add(suite)
            db.session.delete(data)
        db.session.delete(testCase)
    db.session.delete(module)
    try:
        db.session.commit()
        flash('模块信息及其包含的用例/测试数据已删除完毕')
    except Exception as err:
        db.session.rollback()
        flash('删除失败')
        return redirect(url_for('testManage.moduleInfo', moduleId=moduleId))
    return redirect(url_for('testManage.projectInfo', projectId=module.projectId))
####################
# 用例相关
####################
@testManage.route('/testManage/module_<int:moduleId>/addTestCase/', methods=['GET', 'POST'])
def addTestCase(moduleId):
    module = Module.query.get_or_404(moduleId)
    testCases = module.testCases
    caseNameList = [testCase.caseName for testCase in testCases]
    funcNameList = [testCase.funcName for testCase in testCases]
    form = AddTestCaseForm(caseNameList, funcNameList)
    if form.validate_on_submit():
        testCase = TestCase(caseName=form.caseName.data, funcName=form.funcName.data,
                params=form.params.data, remark=form.remark.data, moduleId=moduleId)
        db.session.add(testCase)
        db.session.commit()
        flash('用例添加成功')
        return redirect(url_for('testManage.testCaseInfo', testCaseId=testCase.id))
    return render_template('/testManage/addTestCase.html', form=form, module=module)

@testManage.route('/testManage/modifyTestCase/<int:testCaseId>', methods=['GET', 'POST'])
def modifyTestCase(testCaseId):
    testCase = TestCase.query.get_or_404(testCaseId)
    module = testCase.module
    testCases = module.testCases[:]
    testCases.remove(testCase)
    form = ModifyTestCaseForm()
    form.caseName.data = testCase.caseName
    form.funcName.data = testCase.funcName
    form.params.data = testCase.params
    form.remark.data = testCase.remark
    if form.validate_on_submit():
        if request.form.get('caseName') in [t.caseName for t in testCases]:
            flash('该模块下已有相同的用例名')
            return redirect(url_for('testManage.modifyTestCase', testCaseId=testCaseId))
        if request.form.get('funcName') in [t.funcName for t in testCases]:
            flash('该模块下已有相同的方法名')
            return redirect(url_for('testManage.modifyTestCase', testCaseId=testCaseId))
        testCase.caseName = request.form.get('caseName')
        testCase.funcName = request.form.get('funcName')
        testCase.params = request.form.get('params')
        testCase.remark = request.form.get('remark')
        db.session.add(testCase)
        flash('用例信息修改成功')
        return redirect(url_for('testManage.testCaseInfo', testCaseId=testCaseId))
    return render_template('/testManage/modifyTestCase.html', form=form, testCaseId=testCaseId)

@testManage.route('/testManage/testCaseInfo/<int:testCaseId>')
def testCaseInfo(testCaseId):
    testCase = TestCase.query.get_or_404(testCaseId)
    return render_template('/testManage/testCaseInfo.html', testCase=testCase)

@testManage.route('/testManage/deleteTestCase/<int:testCaseId>')
def deleteTestCase(testCaseId):
    testCase = TestCase.query.get_or_404(testCaseId)
    for data in testCase.datas:
        for suite in Suite.query.all():
            if data in suite.datas:
                suite.datas.remove(data)
            db.session.add(suite)
        db.session.delete(data)
    db.session.delete(testCase)
    try:
        db.session.commit()
        flash('用例信息及其包含的测试数据已删除完毕')
    except Exception as err:
        db.session.rollback()
        flash('删除失败')
        return redirect(url_for('testManage.testCaseInfo', testCaseId=testCaseId))
    return redirect(url_for('testManage.moduleInfo', moduleId=testCase.moduleId))
####################
# 测试数据相关
####################
@testManage.route('/testManage/testCase_<int:testCaseId>/addData/', methods=['GET', 'POST'])
def addData(testCaseId):
    testCase = TestCase.query.get_or_404(testCaseId)
    datas = testCase.datas
    dataNameList = [data.dataName for data in datas]
    form = AddDataForm(dataNameList)
    if form.validate_on_submit():
        data = Data(dataName=form.dataName.data, values=form.values.data, tags=form.tags.data,
                remark=form.remark.data, testCaseId=testCaseId)
        db.session.add(data)
        db.session.commit()
        flash('测试数据添加成功')
        return redirect(url_for('testManage.dataInfo', dataId=data.id))
    return render_template('/testManage/addData.html', form=form, testCase=testCase)

@testManage.route('/testManage/modifyData/<int:dataId>', methods=['GET', 'POST'])
def modifyData(dataId):
    data = Data.query.get_or_404(dataId)
    testCase = data.testCase
    datas = testCase.datas[:]
    datas.remove(data)
    form = ModifyDataForm()
    form.dataName.data = data.dataName
    form.values.data = data.values
    form.tags.data = data.tags
    form.remark.data = data.remark
    if form.validate_on_submit():
        if request.form.get('dataName') in [d.dataName for d in datas]:
            flash('该用例下已有相同的测试数据名')
            return redirect(url_for('testManage.modifyData', dataId=dataId))
        data.dataName = request.form.get('dataName')
        data.values = request.form.get('values')
        data.tags = request.form.get('tags')
        data.remark = request.form.get('remark')
        db.session.add(data)
        return redirect(url_for('testManage.dataInfo', dataId=dataId))
    return render_template('/testManage/modifyData.html', form=form, dataId=dataId)

@testManage.route('/testManage/dataInfo/<int:dataId>')
def dataInfo(dataId):
    data = Data.query.get_or_404(dataId)
    return render_template('/testManage/dataInfo.html', data=data)

@testManage.route('/testManage/deleteData/<int:dataId>')
def deleteData(dataId):
    data = Data.query.get_or_404(dataId)
    for suite in Suite.query.all():
        if data in suite.datas:
            suite.datas.remove(data)
        db.session.add(suite)
    db.session.delete(data)
    try:
        db.session.commit()
        flash('测试数据已删除完毕')
    except Exception as err:
        db.session.rollback()
        flash('删除失败')
        return redirect(url_for('testManage.dataInfo', dataId=dataId))
    return redirect(url_for('testManage.testCaseInfo', testCaseId=data.testCaseId))

####################
# 测试集相关
####################
@testManage.route('/testManage/addSuite/', methods=['GET', 'POST'])
def addSuite():
    projects = Project.query.all()
    form = suiteForm()
    if request.method == 'POST':
        suiteName = request.form.get('suiteName')
        if suiteName in [suite.suiteName for suite in Suite.query.all()]:
            flash('已有相同的测试集名称')
            return redirect(url_for('testManage.addSuite'))
        datas = [Data.query.get(int(i.replace('data_', ''))) for i in request.form.keys() if i.startswith('data_')]
        suite = Suite(suiteName=suiteName, remark=request.form.get('remark'))
        suite.datas = datas
        db.session.add(suite)
        db.session.commit()
        flash('测试集添加成功')
        return redirect(url_for('testManage.suiteInfo', suiteId=suite.id))
    return render_template('/testManage/addSuite.html', form=form, projects=projects)

@testManage.route('/testManage/modifySuite/<int:suiteId>', methods=['GET', 'POST'])
def modifySuite(suiteId):
    suite = Suite.query.get_or_404(suiteId)
    datas = suite.datas
    checkList = ['data_%s'%data.id for data in datas]
    testCases = list({'testCase_%s'%data.testCaseId for data in datas})
    modules = list({'module_%s'%data.testCase.moduleId for data in datas})
    projects = list({'project_%s'%data.testCase.module.projectId for data in datas})
    checkList.extend(testCases)
    checkList.extend(modules)
    checkList.extend(projects)
    projects = Project.query.all()
    form = suiteForm()
    form.suiteName.data = suite.suiteName
    form.remark.data = suite.remark
    if request.method == 'POST':
        suiteName = request.form.get('suiteName')
        if suiteName in [s.suiteName for s in Suite.query.all() if s!=suite]:
            flash('已有相同的测试集名称')
            return redirect(url_for('testManage.modifySuite', suiteId=suiteId))
        datas = [Data.query.get(int(i.replace('data_', ''))) for i in request.form.keys() if i.startswith('data_')]
        suite.suiteName = request.form.get('suiteName')
        suite.remark = request.form.get('remark')
        suite.datas = datas
        db.session.add(suite)
        db.session.commit()
        flash('测试集信息修改成功')
        return redirect(url_for('testManage.suiteInfo', suiteId=suite.id))
    return render_template('/testManage/modifySuite.html', form=form, checkList=checkList, projects=projects)

@testManage.route('/testManage/suiteInfo/<int:suiteId>')
def suiteInfo(suiteId):
    suite = Suite.query.get_or_404(suiteId)
    datas = suite.datas
    checkList = ['data_%s'%data.id for data in datas]
    testCases = list({'testCase_%s'%data.testCaseId for data in datas})
    modules = list({'module_%s'%data.testCase.moduleId for data in datas})
    projects = list({'project_%s'%data.testCase.module.projectId for data in datas})
    checkList.extend(testCases)
    checkList.extend(modules)
    checkList.extend(projects)
    projects = Project.query.all()
    return render_template('/testManage/suiteInfo.html', checkList=checkList, projects=projects, suite=suite)

@testManage.route('/testManage/deleteSuite/<int:suiteId>')
def deleteSuite(suiteId):
    suite = Suite.query.get_or_404(suiteId)
    for testReport in suite.testReports:
        reportFile = 'tests/report/%s'%testReport.reportFile
        if os.path.exists(reportFile):
            os.remove(reportFile)
        db.session.delete(testReport)
    for data in suite.datas:
        data.suites.remove(suite)
        db.session.add(data)
    db.session.delete(suite)
    try:
        db.session.commit()
        flash('测试集已删除完毕')
    except Exception as err:
        db.session.rollback()
        flash('删除失败')
        return redirect(url_for('testManage.suiteInfo', suiteId=suiteId))
    return redirect(url_for('testManage.suiteList'))

@testManage.route('/testManage/suiteList/')
def suiteList():
    suites = Suite.query.all()
    return render_template('/testManage/suiteList.html', suites=suites)

@testManage.route('/testManage/executeSuite/<int:suiteId>')
def executeSuite(suiteId):
    suite = Suite.query.get_or_404(suiteId)
    t = TestEngine(suite.datas)
    reportPath, info = t.executeTest()
    reportInfo = dict(info)
    result = reportInfo['Status'].split(' ')
    r = dict([result[i:i+2] for i in range(0, len(result), 2)])
    passNum = r.get('Pass', 0)
    failedNum = r.get('Failure', 0)
    errorNum = r.get('Error', 0)
    r = len(suite.testReports)
    testReport = TestReport(reportFile=reportPath, passNum=int(passNum), failedNum=int(failedNum), errorNum=int(errorNum), remark='测试集: %s-->%s'%(suite.suiteName, os.path.basename(reportPath)), suiteId=suiteId)
    db.session.add(testReport)
    db.session.commit()
    return 'OK'

@testManage.route('/testManage/testReport/<int:testReportId>')
def getTestReport(testReportId):
    testReport = TestReport.query.get_or_404(testReportId)
    report = open('tests/report/%s'%testReport.reportFile).read()
    return report

@testManage.route('/testManage/deleteTestReport/<int:testReportId>')
def deleteTestReport(testReportId):
    testReport = TestReport.query.get_or_404(testReportId)
    reportFile = 'tests/report/%s'%testReport.reportFile
    suiteId = testReport.suiteId
    db.session.delete(testReport)
    try:
        db.session.commit()
        if os.path.exists(reportFile):
            os.remove(reportFile)
        flash('测试报告删除成功')
    except Exception as err:
        print(err)
        db.session.rollback()
        flash('删除失败')
    return redirect(url_for('testManage.suiteInfo', suiteId=suiteId))

