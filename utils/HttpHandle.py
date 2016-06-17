#coding:utf-8
import requests
import mimetypes
import http.client
import os
from .Log import Log
log = Log.logger

class HttpHandle:
    def __init__(self):
#        http.client.HTTPConnection._http_vsn = 10
#        http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
        self.http = requests.session()

    def get(self, url, params=[], headers={}):
        try:
            res = self.http.get(url, params=params, headers=headers)
        except Exception as err:
            log.error(err)
        if res.status_code == 200:
            log.info('发送get请求: %s 服务器返回: %s' % (url, res.status_code))
        else:
            log.error('发送get请求: %s 服务器返回: %s\n返回内容:\n%s' % (url, res.status_code, res.text))
        return res

    def post(self, url, params=[], headers={}, files=[]):
        #files = [(file1_key, file1_path), (file2_key, file2_path), ...]
        try:
            multipleFiles = [(key, (os.path.split(path)[-1], open(path, 'rb'), mimetypes.guess_type(path)[0]))for key,path in files]
        except Exception as err:
            log.error('读取文件失败\n错误信息: %s' % err)
            assert False
        try:
            res = self.http.post(url, data=params, headers=headers, files=multipleFiles)
        except Exception as err:
            log.error(err)
            assert False
        if res.status_code == 200:
            log.info('发送post请求: %s 服务器返回: %s' % (url, res.status_code))
        else:
            log.error('发送post请求: %s 服务器返回: %s\n返回内容:\n%s' % (url, res.status_code, res.text))
            assert False
        return res
