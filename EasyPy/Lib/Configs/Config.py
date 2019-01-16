# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Server Library.

import os, sys
from optparse import OptionParser
from configparser import ConfigParser

class Config():

    #配置对象
    __config = ""
    #配置文件
    __config_file = "Config.ini"
    
    #初始化文件
    def __init__(self, app_name=""):
        #获取当前目录
        cur_path  = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config_path = cur_path+"/../../Conf/"+self.__config_file
        if app_name != "":
            config_path = cur_path+"/../../../App/"+app_name+"/Conf/"+self.__config_file
        #设置配置文件
        self.parser(config_path)
        
    #解析INI文件
    def parser(self, file_name=""):
        if not os.path.isfile(file_name):
            print("you input ini file not is file")
            sys.exit()
        self.__config = ConfigParser()
        self.__config.readfp(open(file_name))
        
    #读取配置
    def get(self, param_name=""):
        temp = param_name.split(".")
        if len(temp) == 2:
            node  = temp[0]
            field = temp[1]
        else:
            node = "default"
            field = temp[0]
        #print(dir(self.__config))
        #print(self.__config.items("db"))
        value = self.__config.get(node, field)
        return value
    
    #读取节点配置信息
    def getSection(self, name="default"):
        return self.__config.items(name)

if __name__ == "__main__":
    c = Config()
    print(c.get("db.deploy_type"))

