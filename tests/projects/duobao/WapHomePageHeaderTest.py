#coding:utf-8
from .WapBaseAction import WapBaseAction
from .DuoBaoBaseAction import DuoBaoBaseAction

class WapHomePageHeaderTest:

    def __init__(self):
        self.wap = WapBaseAction()
        self.db = DuoBaoBaseAction()

    def normalTest(self):
        result = self.wap.homepageHeader()
        assert result['result'] == 100, 'result字段验证失败，result:%s' % result['result']
        print('result字段,验证成功')
        assert result['resultDesc'] == '成功', 'resultDesc字段验证失败，resultDesc:%s' % result['resultDesc']
        print('resultDesc字段,验证成功')
        quickNavigationList = result['quickNavigation']
        adInfosList = result['adInfos']
        assert len(quickNavigationList) <= 4, '快捷入口个数验证失败, 快捷入口个数为%s'%len(quickNavigationList)
        print('快捷入口个数小于等于4个,验证成功')
        assert len(adInfosList) <= 5, '广告轮播图个数验证失败，广告轮播图个数为%s'%len(adInfosList)
        print('广告轮播图个数小于等于5个,验证成功')

        quickNavigationListInDB = self.db.queryWapQuickNavigation()
        weightList = []
        for n, m in enumerate(quickNavigationList):
            q = [i for i in quickNavigationListInDB if i[0]==m['navName'] and i[2]==m['picture']]
            assert len(q)>=1, '第%s个快捷入口配置信息未在数据库中查到'%(n+1)
            print('第%s个快捷入口在数据库中存在, 验证成功'%(n+1))
            if q[0][1] == 'http://g.caipiao.163.com/gotoLatestPublish.html':
                assert m['clickUrl']=='http://g.caipiao.163.com/t/gotoLatestPublish.html', '第%s个快捷入口clickUrl字段验证失败'%(n+1)
                print('第%s个快捷入口clickUrl字段, 验证成功'%(n+1))
            elif q[0][1] == 'ntescaipiao://circlePostList?boardId=145':
                assert m['clickUrl']=='http://caipiao.163.com/nfop/hlg-shaidan/index.htm?auto=start', '第%s个快捷入口clickUrl字段验证失败'%(n+1)
                print('第%s个快捷入口clickUrl字段, 验证成功'%(n+1))
            else:
                assert m['clickUrl']==q[0][1], '第%s个快捷入口clickUrl字段验证失败'%(n+1)
                print('第%s个快捷入口clickUrl字段, 验证成功'%(n+1))
            weightList.append(q[0][3])

        assert sorted(weightList, reverse=True)==weightList, '快捷入口按权重排序验证失败'
        print('快捷入口按权重排序, 验证成功')

        adInfosListInDB = self.db.queryWapAdInfos()
        weightList = []
        for n, m in enumerate(adInfosList):
            a = [i for i in adInfosListInDB if i[0]==m['clickUrl'] and i[1]==m['picture']]
            assert len(q)>=1, '第%s个图片轮播配置信息未在数据库中查到'%(n+1)
            print('第%s个图片轮播在数据库中存在, 验证成功'%(n+1))
            weightList.append(a[0][2])

        assert sorted(weightList, reverse=True)==weightList, '图片轮播按权重排序验证失败'
        print('图片轮播按权重排序, 验证成功')
