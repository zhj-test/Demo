#coding:utf-8
from ...base.HttpHandle import HttpHandle

class TestDemo:
    def testCaseDemo(self):
        h = HttpHandle()
        r = h.get('http://api.g.caipiao.163.com/pk/pk_lis.html?pageNo=1&pageSize=20')
        print(r.json())
