#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import os
import qingcloud.iaas
from ant.custom.config.ini import DictConfigParser
import datetime

ini_path = os.path.join(os.path.abspath('/etc/'),'yun_config')


ini_section_key  ='qingcloud'


class QingCloudApiBase(object):
    
    def __init__(self,zone = None):
        n = DictConfigParser(ini_path)
        self.access_key_id = n[ini_section_key]['id'].encode('utf-8')
        self.access_key_secret = n[ini_section_key]['key'].encode('utf-8')
        self.zone = zone

    def get_regions(self):

        #conn = self.create_conn()
        conn = qingcloud.iaas.connect_to_zone('pek1', self.access_key_id, self.access_key_secret)
        return  conn.describe_zones()

    def get_describe(self,type = 'instances',balancerId = ''):
        
        try:
            conn = self.create_conn()

            if type == "instances":
                data = conn.describe_instances(status=['running','stopped'])['instance_set']
                
            elif type == 'loadbalancers':
                data = conn.describe_loadbalancers(status = ['active','stopped'])['loadbalancer_set']
            
            elif type == 'loadbalancer_listeners':
                if not balancerId:
                    data = []
                else:
                    data = conn.describe_loadbalancer_listeners(loadbalancer = balancerId,verbose = 1)['loadbalancer_listener_set']
        except:
            print "describe_instances error"
        else:
            
            return data
        
    def create_conn(self):
        try:
            conn = qingcloud.iaas.connect_to_zone(self.zone,self.access_key_id,self.access_key_secret)
            return conn
        except:
            print "create conn error"

    def close_conn(self):
        pass

