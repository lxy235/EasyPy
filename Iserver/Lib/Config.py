# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Config.

import sys
from Configs.ParseConfig import ParseConfig

class Config():

    #配置字典
    __config_dict = {}

    #创建解析器
    def __init__(self, app_name=""):
        #惯例配置
        c = ParseConfig()
        default_dict = c.getValues()
        #读取应用配置
        app_dict = {}
        if app_name != "":
            c = ParseConfig(app_name)
            app_dict = c.getValues()
        #合并配置
        self.__config_dict = dict(default_dict, **app_dict)
        
    #读取配置
    def get(self, param_name=""):
        temp = param_name.split(".")
        if len(temp) == 2:
            node  = temp[0]
            field = temp[1]
        else:
            node = "default"
            field = temp[0]
        value = self.__config_dict[node][field]
        return value
    
if __name__=='__main__':
    config = Config()
    print(config.get("db.hostname"))
    
