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
    ecs_server_address = n[ini_section_key]['slburl'].encode('utf-8')
    
    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2013-02-21', \
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
        print(e.read().strip())
        raise SystemExit(e)

    #make json output pretty, this code is copied from json.tool
    try:
        obj = json.loads(response)
        if quiet:
            return obj
    except ValueError, e:
        raise SystemExit(e)
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write('\n')

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
