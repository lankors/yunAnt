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
from api_base import get_amazon_regions



     
    

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

        try:
            hosts = get_amazon_regions(region=idc).get_only_instances()
        except:
            return []

        if hosts == None:
            return []
        
        for i in hosts:
            
            param={}
            param['outer_ip'] = i.ip_address
            param['hostname'] = i.tags['Name']
            param['wxsn'] =i.id
            param['inner_ip'] = i.private_ip_address
            param['purchase_date'] =i.launch_time.replace('T',' ').replace('Z','')
            param['is_del']    = 0 if i.state=='running'  else 1
            
            self.result.append(param)
            
        return self.result   
        

    def get_idcs(self):
        '''
        获取idc信息
        '''
        regions = get_amazon_regions()
        
        for i in regions:
            param ={}

            param['name'] = u'amazon' + '['+i.name+']'
            param['prefix']= i.name
           
            self.result.append(param)
      
        return self.result
            
    def get_balancers(self,**idc_dict):

        '''
        获取用于负载均衡的机器信息
        '''
        idc =  idc_dict['prefix']
        
        balances  = get_amazon_regions(region=idc,type='ebl').get_all_load_balancers()
        
        for i in balances:
            children = []
            for instance_info in i.instances:
                children.append(instance_info.id)
            
            #亚马逊给的是域名，需要转成ip
            myaddr = socket.getaddrinfo(i.dns_name,'http')[0][4][0]
            public_ip = socket.gethostbyaddr(myaddr)[2][0]
  
            param={}
            param['outer_ip'] = public_ip
            param['hostname'] = i.name
            param['wxsn'] = i.canonical_hosted_zone_name
            param['children']  = ','.join(children)
            
            self.result.append(param)
        return self.result
                
    def get_result(self):
        
        return self.result

