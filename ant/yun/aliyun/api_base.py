#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import sys,os
import urllib, urllib2
import urllib3
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
from ant.custom.config.ini import DictConfigParser


ini_path = os.path.join(os.path.abspath('/etc/'),'yun_config')

ini_section_key  ='aliyun'



def percent_encode(str):
    res = None
    try:
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    except:
        pass
	res = str

    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    
    n = DictConfigParser(ini_path)
    access_key_id = n[ini_section_key]['id'].encode('utf-8')
    access_key_secret = n[ini_section_key]['key'].encode('utf-8')
    ecs_server_address = n[ini_section_key]['url'].encode('utf-8')
    
    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-05-26', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = ecs_server_address + "/?" + urllib.urlencode(parameters)
    return url

def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    request = urllib2.Request(url)
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
    except urllib2.HTTPError, e:
        #print(e.read().strip())
        raise SystemExit(e)
    try:
        obj = json.loads(response)
        return  obj
    except ValueError, e:
        raise SystemExit(e)


def get_host(regionid,page=1):

    user_params = {}
    user_params['Action'] = 'DescribeInstances'
    user_params['RegionId'] = regionid
    user_params['PageSize'] = '100'
    user_params['PageNumber']= str(page)

    return  user_params

def get_hosts(tmp, regionid,page):

    user_params = get_host(regionid, page=page)
    #print(user_params)
    obj = make_request(user_params, quiet=True)
    #print(obj)
    if obj['Instances']['Instance'] != []:

        for zone in obj['Instances']['Instance']:

            tmp.append(zone)
        get_hosts(tmp, regionid, page + 1)

    return  tmp


def describe_instances(regionid):

    if isinstance(regionid,dict):

        return make_request(regionid,quiet=True)

    page =1
    tmp = []
    get_hosts(tmp, regionid, page)

    return tmp



def DescribeLoadBalancers(regionid):
    user_params = {}
    user_params['Action'] = 'DescribeLoadBalancers'
    user_params['RegionId'] = regionid
    obj = make_request(user_params, quiet=True)
    

    zones = []

    for balancer in obj['LoadBalancers']['LoadBalancer']:
        user_params = {}
        user_params['Action'] = 'DescribeLoadBalancerAttribute'
        user_params['LoadBalancerId'] = balancer['LoadBalancerId']

        instances = make_request(user_params, quiet=True)
        if len(instances) > 0:
            zones.append(instances)
                
    return zones