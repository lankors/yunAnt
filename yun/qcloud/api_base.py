#!/usr/bin/python
#coding=utf-8


"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import sys,os
import commands,subprocess
from ant.custom.config.ini import DictConfigParser

import urllib, urllib2
import random
import base64
import hmac
import hashlib
from hashlib import sha1
import uuid
import json
from urllib2 import  URLError

import requests
import binascii
import copy
import time


ini_path = os.path.join(os.path.abspath('/etc/'),'yun_config')

ini_section_key  ='qcloud'



class Sign:
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def make(self, requestHost, requestUri, params, method = 'GET'):
        srcStr = method.upper() + requestHost + requestUri + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]





class Request:
    timeout = 10
    version = 'SDK_PYTHON_1.1'
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def generateUrl(self, requestHost, requestUri, params, method = 'GET'):
        params['RequestClient'] = Request.version
        sign = Sign(self.secretId, self.secretKey)
        params['Signature'] = sign.make(requestHost, requestUri, params, method)
        params = urllib.urlencode(params)

        url = 'https://%s%s' % (requestHost, requestUri)
        if (method.upper() == 'GET'):
            url += '?' + params

        return url

    def send(self, requestHost, requestUri, params, files = {}, method = 'GET', debug = 0):
        params['RequestClient'] = Request.version
        sign = Sign(self.secretId, self.secretKey)
        params['Signature'] = sign.make(requestHost, requestUri, params, method)

        url = 'https://%s%s' % (requestHost, requestUri)

        if (method.upper() == 'GET'):
            req = requests.get(url, params=params, timeout=Request.timeout)
            if (debug):
                print 'url:', req.url, '\n'
        else:
            req = requests.post(url, data=params, files=files, timeout=Request.timeout)
            if (debug):
                print 'url:', req.url, '\n'

        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        return req.text

    


class Base:
    debug = 0
    requestHost = ''
    requestUri = '/v2/index.php'
    _params = {}

    def __init__(self, config):

        n = DictConfigParser(ini_path)
        config['secretId'] = n[ini_section_key]['id'].encode('utf-8')
        config['secretKey'] = n[ini_section_key]['key'].encode('utf-8')


        self.secretId = config['secretId']
        self.secretKey = config['secretKey']
        self.defaultRegion = config['Region']
        self.method = config['method']

    def _checkParams(self, action, params):
        self._params = copy.deepcopy(params)
        self._params['Action'] = action[0].upper() + action[1:]

        if (self._params.has_key('Region') != True):
            self._params['Region'] = self.defaultRegion

        if (self._params.has_key('SecretId') != True):
            self._params['SecretId'] = self.secretId

        if (self._params.has_key('Nonce') != True):
            self._params['Nonce'] = random.randint(1, sys.maxint)

        if (self._params.has_key('Timestamp') != True):
            self._params['Timestamp'] = int(time.time())

        return self._params

    def generateUrl(self, action, params):
        self._checkParams(action, params)
        request = Request(self.secretId, self.secretKey)
        return request.generateUrl(self.requestHost, self.requestUri, self._params, self.method)

    def call(self, action, params, files = {}):
        self._checkParams(action, params)
        request = Request(self.secretId, self.secretKey)
        callback = request.send(self.requestHost, self.requestUri, self._params, files, self.method, self.debug)
        return json.loads(callback)



class Base2:
    debug = 0
    requestHost = ''
    requestUri = '/v2/index.php'
    _params = {}

    def __init__(self, config):

        n = DictConfigParser(ini_path)
        config['secretId'] = n[ini_section_key]['id'].encode('utf-8')
        config['secretKey'] = n[ini_section_key]['key'].encode('utf-8')


        self.secretId = config['secretId']
        self.secretKey = config['secretKey']
        self.defaultRegion = config['instanceType']
        self.method = config['method']

    def _checkParams(self, action, params):
        self._params = copy.deepcopy(params)
        self._params['Action'] = action[0].upper() + action[1:]

        if (self._params.has_key('instanceType') != True):
            self._params['instanceType'] = self.defaultRegion

        if (self._params.has_key('SecretId') != True):
            self._params['SecretId'] = self.secretId

        if (self._params.has_key('Nonce') != True):
            self._params['Nonce'] = random.randint(1, sys.maxint)

        if (self._params.has_key('Timestamp') != True):
            self._params['Timestamp'] = int(time.time())

        return self._params

    def generateUrl(self, action, params):
        self._checkParams(action, params)
        request = Request(self.secretId, self.secretKey)
        return request.generateUrl(self.requestHost, self.requestUri, self._params, self.method)

    def call(self, action, params, files = {}):
        self._checkParams(action, params)
        request = Request(self.secretId, self.secretKey)

        callback = request.send(self.requestHost, self.requestUri, self._params, files, self.method, self.debug)
        return json.loads(callback)

class Cvm(Base):
    requestHost = 'cvm.api.qcloud.com'
 

class Region(Base2):
    requestHost = 'trade.api.qcloud.com'


class Lb(Base):
    requestHost = 'lb.api.qcloud.com'

