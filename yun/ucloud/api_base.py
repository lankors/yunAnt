#/usr/bin/python evn
#coding=utf-8
"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-6-13 11:55:57
usege:

"""
import hashlib,json,httplib
import urlparse
import urllib
import sys
import os
from ant.custom.config.ini import DictConfigParser


ini_path = os.path.join(os.path.abspath('/etc/'),'yun_config')

ini_section_key  ='ucloud'
    

class UCLOUDException(Exception):
    def __str__(self):
        return "Error"


def _verfy_ac(private_key, params):
    items = params.items()
    items.sort()

    params_data = ""
    for key, value in items:
        params_data = params_data + str(key) + str(value)

    params_data = params_data+private_key
    
    '''use sha1 to encode keys'''
    hash_new = hashlib.sha1()
    hash_new.update(params_data)
    hash_value = hash_new.hexdigest()
    return hash_value


class UConnection(object):
    def __init__(self, base_url):
        self.base_url = base_url
        o = urlparse.urlsplit(base_url)
        if o.scheme == 'https':
            self.conn = httplib.HTTPSConnection(o.netloc)
        else:
            self.conn = httplib.HTTPConnection(o.netloc)

    def __del__(self):
        self.conn.close()

    def get(self, resouse, params):
        resouse += "?" + urllib.urlencode(params)
        #print("%s%s" % (self.base_url, resouse))
        self.conn.request("GET", resouse)
        response = json.loads(self.conn.getresponse().read())
        return response


class UcloudApiClient(object):
    # 添加 设置 数据中心和  zone 参数
    def __init__(self):

        n = DictConfigParser(ini_path)
        public_key = n[ini_section_key]['id'].encode('utf-8')
        private_key = n[ini_section_key]['key'].encode('utf-8')
        base_url = n[ini_section_key]['url'].encode('utf-8')

        self.g_params = {}
        self.g_params['PublicKey'] = public_key
        self.private_key = private_key
        self.conn = UConnection(base_url)

    def get(self, uri, params):
        # print params
        _params = dict(self.g_params, **params)
        _params["Signature"] = _verfy_ac(self.private_key, _params)
        return self.conn.get(uri, _params)
