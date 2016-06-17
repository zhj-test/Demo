#coding:utf-8
from utils.HttpHandle import HttpHandle
from utils.DBHandle import DBHandle
from utils.Encrypt import Encrypt
from .Constant import URL, SQL
import time

class DuobaoBaseAction:

    def __init__(self):
        self.http = HttpHandle()
        self.duobaoDB = DBHandle('OracleDuoBao')
        self.pkDB = DBHandle('OraclePK')

    def login(self, username, password):
        params = [
                ('username', username),
                ('password', password),
                ]
        res = self.http.get(URL['LOGIN_URL'], params)
        assert '正在登录，请稍等' in res.text, '登录失败'

    def addOrderPC(self, **kw):
        '''pc版下单'''
        params = [
                ('orderType', kw.get('orderType', '1')),
                ('source', kw.get('source', '4')),
                ('productId', kw['productId']),
                ('periodId', kw['periodId']),
                ('payType', kw.get('payType', '2')),
                ('couponId', kw.get('couponId', '')),
                ('couponAmount', kw.get('couponAmount', '')),
                ('payCoins', kw.get('payCoins', '1')),
                ('payAmount', kw.get('payAmount', '0')),
                ('totalAmount', kw.get('totalAmount', '1')),
                #('isPartNewPeriod', kw.get('isPartNewPeriod', 1)),
                ]
        res = self.http.post(URL['ADD_ORDER_PC_URL'], params)
        assert res.json()['result'] == 100, res.json()
        return res.json()

    def addOrderPK(self, **kw):
        '''pk场下单'''
        db = DBHandle('MySQLMQ')
        username = kw['accountId']
        sessionId = db.query(SQL['GET_SESSIONID'] % username)[0][0]
        params = [
                ('accountId', kw['accountId']),
                ('sessionId', sessionId),
                ('payType', kw.get('payType', '1')),
                ('orderType', kw.get('orderType', '1')),
                ('periodId', kw['periodId']),
                ('productId', kw['productId']),
                ('couponId', kw.get('couponId', '')),
                ('payCoins', kw['payCoins']),
                ('couponAmount', kw.get('couponAmount', '')),
                ('buyTimes', kw['buyTimes']),
                ('totalAmount', kw.get('totalAmount', kw['payCoins'])),
                ('payAmount', kw.get('payAmount', '0')),
                ('betOption', kw.get('betOption', '0')),
                ('source', kw.get('source', '1')),
                ('mobileType', kw.get('mobileType', 'iphone')),
                ('alipaySDKPreferred', kw.get('alipaySDKPreferred', '0')),
                ('isPartNewPeriod', kw.get('isPartNewPeriod', '1')),
                ]
        e = Encrypt()
        stamp = str(int(time.time()*1000))
        data = e.Encrypt(params, stamp)
        D = [
                ('data', data),
                ('stamp', stamp),
                ('product', kw.get('product', 'android_cp_hyg')),
                ('mobileType', kw.get('mobileType', 'android')),
                ]
        res = self.http.post(URL['ADD_ORDER_PK_URL'], D)
        assert res.json()['result'] == 100, res.json()
        return res.json()

    def addOrderAPI(self, **kw):
        '''客户端下单'''
        db = DBHandle('MySQLMQ')
        username = kw['accountId']
        sessionId = db.query(SQL['GET_SESSIONID'] % username)[0][0]
        params = [
                ('accountId', kw['accountId']),
                ('sessionId', sessionId),
                ('orderType', kw.get('orderType', '1')),
                ('productId', kw['productId']),
                ('periodId', kw['periodId']),
                ('source', kw.get('source', '1')),
                ('productType', kw.get('productType', '乐得版')),
                ('mobileType', kw.get('mobileType', 'iphone')),
                ('payType', kw.get('payType', '1')),
                ('couponId', kw.get('couponId', '')),
                ('couponAmount', kw.get('couponAmount', '')),
                ('payCoins', kw.get('payCoins', '1')),
                ('payAmount', kw.get('payAmount', '0')),
                ('totalAmount', kw.get('totalAmount', '1')),
                ('isPartNewPeriod', kw.get('isPartNewPeriod', ''))
                ]
        e = Encrypt()
        stamp = str(int(time.time()*1000))
        data = e.Encrypt(params, stamp)
        D = [
                ('data', data),
                ('stamp', stamp),
                ]
        res = self.http.post(URL['ADD_ORDER_API_URL'], D)
        assert res.json()['result'] == 100, res.json()
        return res.json()

    def addOrderWAP(self, **kw):
        '''触屏版下单'''
        params = [
                ('orderType', kw.get('orderType', '1')),
                ('source', kw.get('source', '2')),
                ('productId', kw['productId']),
                ('periodId', kw['periodId']),
                ('payType', kw.get('payType', '2')),
                ('couponId', kw.get('couponId', '')),
                ('couponAmount', kw.get('couponAmount', '')),
                ('payCoins', kw.get('payCoins', '1')),
                ('payAmount', kw.get('payAmount', '0')),
                ('totalAmount', kw.get('totalAmount', '1')),
                ]
        res = self.http.post(URL['ADD_ORDER_WAP_URL'], params)
        assert res.json()['result'] == 100, res.json()
        return res.json()

    def pkList(self, **kw):
        '''pk场列表'''
        params = [
                ('pageNo', kw.get('pageNo', '')),
                ('pageSize', kw.get('pageSize', '')),
                ]
        res = self.http.get(URL['PK_LIST_URL'], params)
        assert res.json()['result'] == 100, res.json()
        return res.json()

    def productDetail(self, productId):
        '''奖品详情'''
        res = self.http.get(URL['PRODUCT_DETAIL_URL'], params=[('productId', productId)])
        assert res.json()['result'] == 100, res.json()
        return res.json()

    def addCoins(self, accountId, coins):
        '''给指定账户增加欢乐豆'''
        if len(self.duobaoDB.query(SQL['QUERY_ACCOUNT_COINS']%accountId)) == 0:
            self.duobaoDB.execute(SQL['INSERT_ACCOUNT_COINS']%(accountId, coins))
        else:
            self.duobaoDB.execute(SQL['UPDATE_ACCOUNT_COINS']%(coins, accountId))

    def queryOrderIdByPayOrderId(self, payOrderId):
        '''通过payOrderId查询orderId'''
        orderId = self.duobaoDB.query(SQL['QUERY_ORDER_BY_PAY_ORDER']%payOrderId)[0][0]
        return orderId

    def queryOnSellPeriodId(self, productId):
        '''通过payOrderId查询orderId'''
        periodId = self.duobaoDB.query(SQL['QUERY_ON_SELL_PERIOD']%productId)[0][0]
        return periodId

    def queryPkOnSellPeriodInfo(self, productId):
        '''通过productId查询pk场在售期次信息'''
        info = self.pkDB.query(SQL['QUERY_PK_ON_SELL_PERIOD_INFO'] % productId)[0]
        return info
