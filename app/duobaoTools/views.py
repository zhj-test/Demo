#coding:utf-8
from . import duobaoTools
from .DuobaoBaseAction import DuobaoBaseAction
from flask import render_template, flash, redirect, url_for, request
import os
from utils.Encrypt import Encrypt
from utils.Log import Log

log = Log.logger

####################
# 1元购测试工具首页
####################
@duobaoTools.route('/duobaoTools/')
def index():
    return render_template('/duobaoTools/index.html')

@duobaoTools.route('/duobaoTools/addOrder/')
def addOrder():
    pk = DuobaoBaseAction()
    pkList = []
    pkListMaxPage = pk.pkList()['maxPage']
    for pageNo in range(1, int(pkListMaxPage)+1):
        params = {
                'pageNo': pageNo,
                'pageSize': '20',
                }
        pkListInfo = pk.pkList(**params)['productInfosList']
        for info in pkListInfo:
            periodId = info['periodId']
            productName = info['productName']
            productId = info['productId']
            pkList.append((productId, productName, periodId))
    return render_template('/duobaoTools/addOrder.html', pkList=pkList)

@duobaoTools.route('/duobaoTools/addDuobaoOrder/', methods=['POST'])
def addDuobaoOrder():
    username = request.form.get('username')
    password = request.form.get('password')
    productID = request.form.get('productID')
    pay_coins = int(request.form.get('pay_coins'))
    total_time = request.form.get('total_time')
    totalCoins = int(pay_coins)*int(total_time)
    source = request.form.get('source')
    duobao = DuobaoBaseAction()
    duobao.login(username, password)
    duobao.addCoins(username, totalCoins)
    orderList = []
    if source == 'pc':
        addOrder = duobao.addOrderPC
    elif source == 'api':
        addOrder = duobao.addOrderAPI
    elif source == 'wap':
        addOrder = duobao.addOrderWAP

    for i in range(int(total_time)):
        try:
            info = duobao.productDetail(productID)
            remainTimes = info['product']['remainTimes']
            period = duobao.queryOnSellPeriodId(productID)
            if pay_coins > remainTimes:
                coins = remainTimes
            else:
                coins = pay_coins
            params = {'productId': productID, 'periodId': period, 'payCoins': coins, 'totalAmount': coins, 'accountId': username}
            payInfo = addOrder(**params)
            log.info('下单返回值: %s' % payInfo)
            orderId = duobao.queryOrderIdByPayOrderId(payInfo['duoBaoOrderId'])
            orderList.append(orderId)
        except Exception as err:
            return "下单出错，请检查输入数据正确性。\n%s" % err

    resultStr = "下单orderId为: <br />"
    resultStr += "<br />".join(orderList)
    return resultStr

@duobaoTools.route('/duobaoTools/addPkOrder/', methods=['POST'])
def addPkOrder():
    try:
        pk = DuobaoBaseAction()
        username = request.form.get('username')
        productId = request.form.get('productID')
        betOption = request.form.get('betOption')
        buyTimes = request.form.get('buyTimes')
        info = pk.queryPkOnSellPeriodInfo(productId)
        periodId = info[0]
        payCoins = int(info[1]/2)*int(buyTimes)
        pk.addCoins(username, payCoins)
        params = {'accountId': username, 'periodId': periodId, 'productId': productId, 'payCoins': payCoins, 'betOption': betOption, 'buyTimes': buyTimes}
        result = pk.addOrderPK(**params)
        resultStr = "下单返回值为:<br />%s" % result
        return resultStr
    except Exception as err:
        return "下单出错, 请检查输入数据正确性。<br />%s" % err
