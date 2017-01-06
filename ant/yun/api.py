#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wqc2008@gmail.com
createtime:2014-7-9上午11:26:08
usege:

"""

import types
import json

from ant.custom.auto_load import auto_load


class api():
    '''
    本模块自动加载yun中的不同的模块类型，并运行，与实际业务无关，放置在yun包中
    '''
    def __init__(self,package_name,func_name,param ={}):
        
        self.package_name = package_name
        self.func_name    = func_name
        self.param        = param
        self.mod          = None
            
    def get_mod(self):
        
        #自动加载模块
        auto = auto_load('ant.yun.%s.api'%self.package_name)   
        self.mod = auto.get_mod() 
        
    def get_result(self): 
        
        self.get_mod()

        #实例化 运行
        object = None
        
        if self.param == {}:
            
            object = getattr(self.mod, 'API')(self.func_name)
        else:
            
            object = getattr(self.mod, 'API')(self.func_name,**self.param)
            
        object.start()
        object.join()
        
        return object.get_result()
