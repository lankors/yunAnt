# 项目代号：yunAnt
============
###项目介绍：
* 项目代号取自蚂蚁搬家之意，主要是用来收集和管理各家云服务器，方便做CMDB。

###支持python版本
    python2.7
    python3.5

###安装方式
    依赖 qingcloud-sdk 、boto
    pip2.7 install yunAnt

###配置项 /etc/yun_config

    [aliyun]
    url = https://ecs.aliyuncs.com
    id  = xxxxxx
    key = xxxxxx
    slburl = https://slb.aliyuncs.com

    [ucloud]
    url = http://api.ucloud.cn
    id  = xxxxxx
    key = xxxxxx

    [amazon]
    url = http://api.ucloud.cn
    id  = xxxxxx
    key = xxxxxx

    [qcloud]
    url = api.qcloud.com
    id  = xxxxxx
    key = xxxxxx

    [qingcloud]
    id = xxxxxx
    key = xxxxxx



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


### 输出格式
    区域格式:
    {'prefix': u'pek1', 'name': u'pek1'}

    服务器格式:
     [
      {'hostname': 'codis_test1',
      'inner_ip': '10.10.10.76',
      'is_del': 0,
      'os': 'centos65x64d',
      'outer_ip': '114.114.114.114',
      'purchase_date': '2016-10-11 07:14:55',
      'wxsn': 'i-ipzzr9sr'},
      {'hostname': 'codis_test1',
      'inner_ip': '10.10.10.76',
      'is_del': 0,
      'os': 'centos65x64d',
      'outer_ip': '114.114.114.114',
      'purchase_date': '2016-10-11 07:14:55',
      'wxsn': 'i-ipzzr9sr'}
      ]

    负载格式:

    [
     {'children': u'i-tw6ksevg,i-z76mpmku',
      'hostname': 'xxx_lb',
      'outer_ip': '114.114.114.114',
      'wxsn': 'lb-ypysddsm'},
     {'children': u'i-uqylknbc,i-1wtbms18',
      'hostname': 'xxx_lb',
      'outer_ip': '114.114.114.115',
      'wxsn': 'lb-thvj2bhc'}
      ]


###Ant项目代码:

* https://github.com/djshell/yunAnt