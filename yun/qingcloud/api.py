#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import json
import socket
from pprint import pprint
from threading import  Thread
from api_base import QingCloudApiBase
import time


__ALL__ =['API']

class API(Thread):
    '''
    
    '''

    def __init__(self,func,**param):
        super(API,self).__init__()
        self.func = func
        self.param = param
        self.result = []
        
    def run(self):
        '''
        任务调度，根据不函数名不同进行任务作业
        '''
        if callable(getattr(self ,self.func)):
            if isinstance(self.param,dict) and self.param !={}:
                self.result = getattr(self, self.func)(**self.param)
            else:
                self.result = getattr(self, self.func)()
        

    def get_hosts(self,**idc_dict):
        '''
        获取主机内容 
        '''
        zone =  idc_dict['prefix']
        
        api = QingCloudApiBase(zone)
        hosts = api.get_describe('instances')
         
        if hosts == None:
            return []

        for info in hosts:
            param = {}
            
            param['outer_ip'] = info['eip']['eip_addr'].encode('utf8') if info.has_key('eip') else ''
            param['inner_ip'] = info['vxnets'][0]['private_ip'].encode('utf8')
            param['hostname'] = info['instance_name'].encode('utf8')
            
            purchase_date = time.mktime(time.strptime(info['create_time'].encode('utf8'),"%Y-%m-%dT%H:%M:%SZ"))
            param['purchase_date'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(purchase_date))

            param['wxsn'] = info['instance_id'].encode('utf8')
            param['os'] = info['image']['image_id'].encode('utf8')
            
            param['is_del'] = 0 if info['status']=='running' else 1


            self.result.append(param)
            
        return self.result   
        

    def get_idcs(self):
        '''
        获取idc信息
        '''



        api = QingCloudApiBase()
        result = balances  = api.get_regions()

        idcs = []
        for idc in result['zone_set']:

            idcs.append({'name':idc["zone_id"],'prefix':idc["zone_id"]})

        return  idcs


            
    def get_balancers(self,**idc_dict):

        '''
        获取用于负载均衡的机器信息
        '''
        zone =  idc_dict['prefix']
        api = QingCloudApiBase(zone)
        balances  = api.get_describe('loadbalancers')
        
        if balances == None:
            return []
        
        for info in balances:
            children = []
            child_data = api.get_describe('loadbalancer_listeners',info['loadbalancer_id'])[0]
            for instance_info in child_data['backends']:
                children.append(instance_info['resource_id'])
            
            param = {}
            param['outer_ip'] = info['eips'][0]['eip_addr'].encode('utf8') if info.has_key('eips') else ''
            param['hostname'] = info['loadbalancer_name'].encode('utf8')
            param['wxsn'] = info['loadbalancer_id'].encode('utf8')

            param['children']  = ','.join(children)
            
            self.result.append(param)
            
        return self.result
            
    def get_result(self):
        
        return self.result

