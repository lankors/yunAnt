#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-6-13 11:55:57
usege:

"""
import time
from pprint import pprint
from threading import  Thread
from multiprocessing import Process
from api_base import UcloudApiClient

__ALL__ =['API']

class API(Thread):
    
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
    
    def get_idcs(self): 
        '''
        ucloud没有提供此接口
        '''

        param ={}
        param['name'] = '北京BGP-A'
        param['prefix']= 'cn-north-01'      

        self.result.append(param)

        param ={}
        param['name'] = '北京BGP-B'
        param['prefix']= 'cn-north-02'     

        self.result.append(param)

        param ={}
        param['name'] = '北京BGP-C'     
        param['prefix']= 'cn-north-03'      

        self.result.append(param)

        param ={}
        param['name'] = '华东双线'       
        param['prefix']= 'cn-east-01'          

        self.result.append(param)

        param ={}
        param['name'] = '华南双线'       
        param['prefix']= 'cn-south-01'         

        self.result.append(param)

        param ={}
        param['name'] = '亚太'           
        param['prefix']= 'hk-01'   

        self.result.append(param)

        param ={}
        param['name'] = '北美'           
        param['prefix']= 'us-west-01'  

        self.result.append(param)
           
        return self.result
    
      
    def get_hosts(self,**idc_dict):
        '''
        获取主机内容 
        '''
        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        

        ApiClient = UcloudApiClient()
        Parameters={
                "Action":"DescribeUHostInstance",
                "Region":"%s"%idc,
               }
        result = ApiClient.get("/", Parameters);


        #这里会有一个区域权限不可用的问题
        if result.get('UHostSet'):
            pass
        else:
            return  []


        for host in result['UHostSet']:
           
            outer_ip = ''
            inner_ip = ''

            for ips in host['IPSet']:

                if ips.get('Type') == u'Private':
                    inner_ip = ips['IP']

                if ips.get('Type')  == u'Bgp':
                    outer_ip = ips['IP']


            param={}
            param['outer_ip']  = outer_ip
            param['hostname']   = host['Name']
            param['wxsn']       = host['UHostId']
            param['inner_ip']   = inner_ip
            param['purchase_date'] = time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(host['CreateTime']))
            param['is_del']    = 0 if host['State']=='Running' else 1
            
            self.result.append(param)
            
        return self.result



    def get_balancers(self,**idc_dict):
        
        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        
        ApiClient = UcloudApiClient(region_id =idc)
        result = ApiClient.get('/ulb/vserver', offset=0, max_count=10);
      
        
        if result['ret_code']==0 and result.get('data',None)!=None:
            
            for balancer in result['data']:
                
                
                public_ip = ''
                inner_ip = ''
                
                if balancer.get('public_ips'):
                    public_ip = balancer['public_ips'][0]['ip']
                #保存代理服务器与后端服务器关系    
                children = []
                #pprint(balancer['vserver_infos'][0]['server_infos'])
                for child in  balancer['vserver_infos'][0]['server_infos']:
                    children.append(child['object_id'])
                    
                #print count
                param={}
                param['public_ip'] = public_ip
                param['hostname']  = balancer['vip_name']
                param['wxsn']      = balancer['vip_id']
                param['children']  = ','.join(children)
                
                self.result.append(param)
        
        return self.result        


    def get_result(self):
        
        return self.result
 
