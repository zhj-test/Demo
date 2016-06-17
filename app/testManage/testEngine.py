#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import unittest, os, time, importlib
import HTMLTestRunner
from .. import db

class TestEngine:
    def __init__(self, datas):
        self.datas = datas
        self.testCases = list({data.testCase for data in self.datas})
        self.modules = list({testCase.module for testCase in self.testCases})

    def getBasePath(self):
        basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return basePath

    def testSuiteFactory(self, module):
        folderName = module.project.folderName
        fileName = module.fileName
        className = module.className
        testModule = importlib.import_module('tests.projects.%s.%s' % (folderName, fileName))
        Class = eval('testModule.%s' % className)
        def caseFactory(method, data):
            def func(self):
                '''%s-%s''' % (method.__doc__, data.dataName)
                args = str(data.values).split('|')
                if args == ['']:
                    args = []
                print('args: %s' % args)
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print('startTime: %s\n##############################' % startTime)
                method(self.module, *args)
                endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print('##############################\nendTime: %s' % endTime)
            return func
        class TestCase(unittest.TestCase):
            '''%s'''%module.moduleName
            pass
        TestCase.__name__ = module.moduleName
        TestCase.__doc__ = module.moduleName
        @classmethod
        def setUpClass(cls):
            cls.module = Class()
        @classmethod
        def tearDownClass(cls):
            pass
        n = 0
        for testCase in [testCase for testCase in module.testCases if testCase in self.testCases]:
            method = eval('testModule.%s.%s'%(className, testCase.funcName))
            method.__doc__ = testCase.caseName
            for data in [data for data in testCase.datas if data in self.datas]:
                setattr(TestCase, 'test_%03.f'%n, caseFactory(method, data))
                eval('TestCase.test_%03.f'%n).__doc__ = '%s-%s'%(testCase.caseName, data.dataName)
                n += 1
        setattr(TestCase, 'setUpClass', setUpClass)
        setattr(TestCase, 'tearDownClass', tearDownClass)
        return TestCase

    def executeTest(self, temp=False):
        if not temp:
            now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        else:
            no = 'tmp'
        fileName = os.path.join(self.getBasePath(), 'tests', 'report', 'report_%s.html'%now)
        fp = open(fileName, 'wb')
        allSuite = unittest.TestSuite()
        for module in self.modules:
            suite = unittest.TestLoader().loadTestsFromTestCase(self.testSuiteFactory(module))
            allSuite.addTest(suite)
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='TestReport', description='用例执行情况:')
        r = runner.run(allSuite)
        fp.close()
        return ('report_%s.html'%now, runner.getReportAttributes(r))
