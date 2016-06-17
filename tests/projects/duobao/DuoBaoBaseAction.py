#coding:utf-8
from ... import DBHandle, log
from .Constant import SQL

class DuoBaoBaseAction:
    def __init__(self):
        self.duobao = DBHandle('OracleDuoBao')

    def queryWapQuickNavigation(self):
        '''查询wap版首页快捷入口配置'''
        result = self.duobao.query(SQL['QUERY_WAP_QUICK_NAVIGATION'])
        log.debug(result)
        return result

    def queryWapAdInfos(self):
        '''查询wap版首页广告轮播图配置'''
        result = self.duobao.query(SQL['QUERY_WAP_ADINFOS'])
        log.debug(result)
        return result
