#coding:utf-8
from ... import HttpHandle, log
from .Constant import URL

class WapBaseAction:
    def __init__(self):
        self.http = HttpHandle()

    def login(self, username, password):
        log.info('用户%s正在登录' % username)
        params = [
                ('username', username),
                ('password', password),
                ]
        res = self.http.get(URL['LOGIN_URL'], params)
        assert '正在登录，请稍等' in res.text, '登录失败'
        log.info('用户%s登录成功' % username)

    def logout(self, username):
        log.info('用户%s退出登录' % username)
        params = [
                ('username', username),
                ]
        res = self.http.get(URL['LOGOUT_URL'], params)

    def addressList(self):
        log.info('调用wap-address_list接口')
        res = self.http.get(URL['WAP_ADDRESS_LIST_URL'])
        try:
            return res.json()
        except Exception as err:
            log.error('调用wap-address_list接口失败，错误信息:\n%s' % err)
            assert False

    def homepageHeader(self):
        log.info('调用wap-homepage_header接口')
        res = self.http.get(URL['WAP_HOMEPAGE_HEADER_URL'])
        try:
            return res.json()
        except Exception as err:
            log.error('调用wap-homepage_header接口失败, 错误信息:\n%s' % err)
            assert False

    def homepageGoods(self, pageNo=1, pageSize=20, goodsType=''):
        log.info('调用wap-homepage_goods接口')
        params = [
                ('pageNo', pageNo),
                ('pageSize', pageSize),
                ('goodsType', goodsType),
                ]
        res = self.http.get(URL['WAP_HOMEPAGE_GOODS_URL'], params)
        try:
            return res.json()
        except Exception as err:
            log.error('调用wap-homepage_goods接口失败, 错误信息:\n%s' % err)
            assert False
