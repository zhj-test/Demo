#coding:utf-8

SQL = {
        "INSERT_ACCOUNT_COINS": "INSERT INTO tb_duobao_account_coins (account_id, remain_coins) VALUES ('%s', %s)",
        "UPDATE_ACCOUNT_COINS": "UPDATE tb_duobao_account_coins SET remain_coins = remain_coins+%s WHERE account_id = '%s'",
        "QUERY_ORDER_BY_PAY_ORDER": "select order_id from tb_duobao_order where pay_order_id='%s'",
        "QUERY_ACCOUNT_COINS": "select * from tb_duobao_account_coins where account_id = '%s'",
        "QUERY_ON_SELL_PERIOD": "select period_id from tb_duobao_product_period where product_id = '%s' and status = '1'",
        "GET_SESSIONID": "SELECT session_id FROM TB_LOTTERY_MOBILE_SESSION WHERE account_id = '%s'",
        "QUERY_PK_ON_SELL_PERIOD_INFO": "select period_id, total_times from TB_PK_PERIOD  where product_id = '%s' and START_TIME < SYSDATE and END_TIME > SYSDATE",
        }

URL = {
        'LOGIN_URL': 'http://reg.163.com/login.jsp',
        'LOGOUT_URL': 'http://reg.163.com/Logout.jsp',
        'ADD_ORDER_PC_URL': 'http://888.163.com/bet/addOrder.html',
        'ADD_ORDER_API_URL': 'http://api.g.caipiao.163.com/bet/addOrder.html',
        'ADD_ORDER_WAP_URL': 'http://g.caipiao.163.com/t/bet/addOrder.html',
        'ADD_ORDER_PK_URL': 'http://api.g.caipiao.163.com/yyg/pk/bet/addPkOrder.html',
        'PRODUCT_DETAIL_URL': 'http://g.caipiao.163.com/t/product_detail.html',
        'PK_LIST_URL': 'http://api.g.caipiao.163.com/yyg/pk/pk_list.html',
        }
