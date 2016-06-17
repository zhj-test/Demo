#coding:utf-8
import pymysql
import sqlite3
import cx_Oracle
from .Log import Log
from config import DBConnectConstants
log = Log.logger
import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class DBHandle:

    def __init__(self, whichDB):
        self.DB = DBConnectConstants[whichDB]

    def __connect(self):
        try:
            if self.DB['TYPE'].lower() == 'mysql':
                self.conn = pymysql.connect(**self.DB['DBINFO'])
                self.cur = self.conn.cursor()
            elif self.DB['TYPE'].lower() == 'oracle':
                self.conn = cx_Oracle.connect(self.DB['DBINFO'])
                self.cur = self.conn.cursor()
            elif self.DB['TYPE'].lower() == 'sqlite':
                self.conn = sqlite3.connect(self.DB['DBINFO'])
                self.cur = self.conn.cursor()
            else:
                log.info('%s is Unsupported Type' % self.DB['TYPE'])
        except Exception as err:
            log.error('数据库接连出错, 错误信息:\n%s' % err)
            assert False

    def execute(self, sql):
        self.__connect()
        log.debug('执行SQL: %s' % sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as err:
            log.error('执行SQL出错, 错误信息:\n%s' % err)
            self.conn.rollback()
            assert False
        self.cur.close()
        self.conn.close()

    def query(self, sql, fetchOne=False):
        self.__connect()
        log.debug('查询SQL: %s' % sql)
        try:
            self.cur.execute(sql)
            if fetchOne:
                result = self.cur.fetchone()
            else:
                result = self.cur.fetchall()
            self.cur.close()
            self.conn.close()
            return result
        except Exception as err:
            log.error('查询SQL出错, 错误信息:\n%s' % err)
            self.cur.close()
            self.conn.close()
            assert False
