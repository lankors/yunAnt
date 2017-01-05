# 项目代号：Ant
============
###项目介绍：
* 项目代号取自蚂蚁搬家之意，主要是用来收集和管理各家云服务器，方便做CMDB。

###支持python版本
    python2.7
    python3.5

###安装方式
    依赖 qingcloud-sdk 、boto
    pip2.7 install yunAnt

###用法参考

```
#/usr/bin/python evn
#coding=utf-8


import os
from  ant.yun.api import api
from pprint import  pprint

def run(yun_name):

    #查询云的Region
    strat = api(yun_name,'get_idcs')
    idcs = strat.get_result()


    #查询Region中服务器信息
    for idc in idcs:
        print(idc)
        t = api(yun_name,'get_hosts',idc)
        data =  t.get_result()
        #直接打印个数
        pprint(len(data))
        #pprint(data)

    print("="*50)
    # 查询Region中负载信息
    for idc in idcs:

        print(idc)
        t = api(yun_name,'get_balancers',idc)
        data =  t.get_result()
        # 直接打印个数
        pprint(len(data))
        # pprint(data)




if __name__ == '__main__':

    #,'amazon','qcloud','ucloud','qingcloud'
    yun_list = ['aliyun']
    for yun in yun_list:

        run(yun)
```





