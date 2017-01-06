#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import os
import boto.ec2
import boto.ec2.elb
from ant.custom.config.ini import DictConfigParser


ini_path = os.path.join(os.path.abspath('/etc/'),'yun_config')


ini_section_key  ='amazon'


def get_amazon_regions(region=None,type='ecs'):
    
    n = DictConfigParser(ini_path)
    access_key_id = n[ini_section_key]['id'].encode('utf-8')
    access_key_secret = n[ini_section_key]['key'].encode('utf-8')
    #ecs_server_address = n[ini_section_key]['url'].encode('utf-8')
    
    if region==None:
        try: 
            return  boto.ec2.regions(aws_access_key_id=access_key_id,aws_secret_access_key=access_key_secret)

        except  Exception as e:
            #print e

            return None
    else:
        if type == 'ecs':
            try:
                return boto.ec2.connect_to_region(region,aws_access_key_id=access_key_id,aws_secret_access_key=access_key_secret)
    
            except  Exception as e:
                #print e
                return None
        if type == 'ebl':
            try:
                return boto.ec2.elb.connect_to_region(region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=access_key_secret)

            except  Exception as e:
                #print e
                return None
             
        

'''
if __name__ == '__main__':
    regions = get_amazon_regions()
    
    for i in regions:
        name = i.name
        print name
'''
'''
res = conn.get_all_reservations()
for i in res:
    print i
status = conn.get_all_instance_status()
print status
'''
