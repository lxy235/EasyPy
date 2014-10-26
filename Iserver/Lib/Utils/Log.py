# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Log

import logging, os, types
import datetime, math
from Const import *
from Config import Config

class Log():

    #日志类型
    __type  = {1:"SYSTEM",2:"QUEUE"}
    #日志级别
    __level = {50:"CRITICAL",40:"ERROR",30:"WARNING",20:"INFO",10:"DEBUG"}
    #日志信息
    __log = []
    #日期格式
    __format = "%Y-%m-%d %H:%M:%S"
    #配置对象
    __config = ""
    #日志目录
    __log_path = ""
    
    def __init__(self):
        #获取当前目录
        _cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        _log_path = _cur_path+"/../../../App/Data/Log"
        if not os.path.isdir(_log_path):
            os.makedirs(_log_path)
        #创建解析器
        self.__config = Config()
        self.__log_path = _log_path
     
    #记录日志，并且过滤未设置的级别
    def record(self, msg="", type=LOG_SYSTEM, level=ERROR, record=False):
        if isinstance(msg, (list,tuple)):
            s = [str(i) for i in msg]
            msg = " | ".join(s)
        type = self.__type[type]
        level = self.__level[level]
        log_level = self.__config.get("log_level").split(",")
        if record or (level in log_level):
            now = datetime.datetime.now().strftime(self.__format)
            self.__log.append("%s %s: %s" % (now, type, msg))
            
    #日志保存
    #destination 写入目标
    def save(self, destination='', level=ERROR):
        if destination == "":
            now = datetime.datetime.now().strftime("%Y_%m_%d")
            destination = self.__log_path+"/"+now+".log"
        else:
            destination = self.__log_path+"/"+destination
        #检测日志文件大小，超过配置大小则备份日志文件重新生成
        is_file = os.path.isfile(destination) #判断文件，是否存在
        if is_file == True:
            file_size = os.path.getsize(destination) #获取文件尺寸，以字节为单位
            log_file_size = math.floor(int(self.__config.get("log_file_size")))
            if log_file_size <= file_size:
                cur_time = datetime.datetime.now()
                os.rename(destination, os.path.dirname(destination)+'/'+str(cur_time)+'-'+os.path.basename(destination))
        #写日志
        msg = "\r\n".join(self.__log)
        logging.basicConfig(filename=destination, level=level)
        logging.log(level, msg)
        #保存后清空日志缓存
        self.__log = []
        
    #写日志
    def write(self, msg="", destination="", type=LOG_SYSTEM, level=ERROR):
        if isinstance(msg, (list,tuple)):
            s = [str(i) for i in msg]
            msg = " | ".join(s)
        if destination == "":
            now = datetime.datetime.now().strftime("%Y_%m_%d")
            destination = self.__log_path+"/"+now+".log"
        else:
            destination = self.__log_path+"/"+destination
        #检测日志文件大小，超过配置大小则备份日志文件重新生成
        is_file = os.path.isfile(destination) #判断文件，是否存在
        if is_file == True:
            file_size = os.path.getsize(destination) #获取文件尺寸，以字节为单位
            log_file_size = math.floor(int(self.__config.get("log_file_size")))
            if log_file_size <= file_size:
                cur_time = datetime.datetime.now()
                os.rename(destination, os.path.dirname(destination)+'/'+str(cur_time)+'-'+os.path.basename(destination))
        #写日志
        now = datetime.datetime.now().strftime(self.__format)
        type = self.__type[type]
        msg = "%s %s: %s" % (now, type, msg)
        logging.basicConfig(filename=destination, level=level)
        logging.log(level, msg)


