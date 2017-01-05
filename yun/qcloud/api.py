#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import json,socket
from threading import  Thread


from api_base import *




__ALL__ =['API']

class API(Thread):
    '''
    
    '''

    def __init__(self,func,**param):
        super(API,self).__init__()
        self.func = func
        self.param = param
        self.result = []
        
    def  run(self):
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
        
        idc =  idc_dict['prefix']
        del idc_dict['prefix']

        action = 'DescribeInstances'
        config = {
            'Region': '%s' % idc,
            'method': 'get'
        }
        params = {}
        service = Cvm(config)
        result =  service.call(action, params)      
 


        if result.get('totalCount')>0:

            for i in result['instanceSet']:
                
                param={}
                param['outer_ip'] = i['wanIpSet'][0]
                param['hostname']  = i['instanceName']
                param['wxsn']      = i['instanceId']
                param['inner_ip']  = i['lanIp']
                param['purchase_date'] = i['createTime']      

                self.result.append(param)
                
        return self.result
        
    
    def get_idcs(self):
        '''
        获取idc信息
        '''

        temp = []
        action = 'DescribeProductRegionList'
        config = {
            'Region': ' ' ,
            'instanceType': '1',
            'method': 'get'
        }
        params = {}
        service = Region(config)
        result =  service.call(action, params)

        for key in result['availableRegion']:


            dict = {'prefix':key,'name':result['availableRegion'][key]}
            temp.append(dict)

        return temp
  
    def get_balancers(self,**idc_dict):

        idc =  idc_dict['prefix']
        del idc_dict['prefix']

        action = 'DescribeLoadBalancersByInstances'
        config = {
            'Region': '%s'% idc,
            'method': 'get'
        }
        params = {}
        service = Lb(config)
        result =  service.call(action, params)

        if result['loadBalancerSet']>0:
#             print result
            for i in result['loadBalancerSet']:
                
                param={}
                param['outer_ip'] =  i['backendLanIp'] if i['loadBalancerVips']==[] else  i['loadBalancerVips'][0]
                param['hostname']  = i['loadBalancerName']
                param['wxsn']      = i['instanceId']
                param['inner_ip']  = i['backendLanIp']
                param['purchase_date'] = i['createTime']
                param['is_del']    = 0 if i['status']=='1' else 1
                param['children']  = i['backendWanIpSet']
                self.result.append(param)
                
        return self.result


                
    def get_result(self):
        
        return self.result


