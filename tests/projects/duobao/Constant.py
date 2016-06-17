#coding:utf-8

SQL = {
        'QUERY_WAP_QUICK_NAVIGATION': "select t.title, t.link_url, t.pic_url, t.WEIGHT from DUOBAO.TB_DUOBAO_LINK_CONFIG t where t.LINK_TYPE = '2' and t.START_TIME < sysdate and t.END_TIME > sysdate and t.PLATFORM = 'other' order by t.weight desc",
        'QUERY_WAP_ADINFOS': "select t.link_url, t.pic_url, t.WEIGHT from DUOBAO.TB_DUOBAO_LINK_CONFIG t where t.LINK_TYPE = '1' and t.START_TIME < sysdate and t.END_TIME > sysdate and t.PLATFORM like '%wap%' order by t.weight desc",
        }

URL = {
        'LOGIN_URL': 'http://reg.163.com/login.jsp',
        'LOGOUT_URL': 'http://reg.163.com/Logout.jsp',
        'WAP_HOMEPAGE_HEADER_URL': 'http://g.caipiao.163.com/t/homepage_header.html',
        'WAP_HOMEPAGE_GOODS_URL': 'http://g.caipiao.163.com/t/homepage_goods.html',
        'WAP_ADDRESS_LIST_URL': 'http://g.caipiao.163.com/t/address/address_list.html',
        }
