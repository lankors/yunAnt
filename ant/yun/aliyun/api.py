#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import json
from threading import  Thread


from api_base import describe_instances
from slb import DescribeLoadBalancers



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

        hosts = describe_instances(idc)

        for i in hosts:

            try:
                inner_ip = i['InnerIpAddress']['IpAddress'][0]
            except:

                inner_ip = i['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]

            try:
                pubic_ip = i['PublicIpAddress']['IpAddress'][0]
            except:
                # from  pprint import  pprint
                # pprint(i)
                # break
                pubic_ip = i['EipAddress']['IpAddress']

            param={}
            param['outer_ip']  = pubic_ip
            param['hostname']  = i['HostName']
            param['wxsn']      = i['InstanceId']
            param['inner_ip']  = inner_ip
            param['purchase_date'] =i['CreationTime'].replace('T',' ').replace('Z','')
            param['is_del']    = 0 if i['Status']=='Running'  else 1

            self.result.append(param)
                
        return self.result
        
    
    def get_idcs(self):
        '''
        获取idc信息
        '''
        param ={}
        param['action'] ='DescribeRegions'
        temp = describe_instances(param)
        
        
        for  i in  temp['Regions']['Region']:
            param ={}

            param['name']  = u'aliyun' + '['+i['LocalName']+']'
            param['prefix']= i['RegionId']
            
            self.result.append(param)
            
        return self.result
            
    def get_balancers(self,**idc_dict):

        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        
        result = DescribeLoadBalancers(idc)
       

        for i in result:
            #保存代理服务器与后端服务器关系
            children = []

            for child in  i['BackendServers']['BackendServer']:
                children.append(child['ServerId'])

            param={}
            param['outer_ip'] = i['Address']
            param['hostname']  = i['LoadBalancerName']
            param['wxsn']      = i['LoadBalancerId']
            param['children']  = ','.join(children)

            self.result.append(param)
        return self.result
                
    def get_result(self):
        
        return self.result


