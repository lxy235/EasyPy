# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Util

import sys, os, traceback
from Utils.Log import Log
from Const import *
from Config import Config

#日志对象
l = Log()

def log(msg="", log_type=LOG_SYSTEM, log_level=ERROR, log_file=""):
    config = Config()
    if config.get("log_record") == "False":
        return False
    if msg == "":
        #捕获异常信息
        msg = traceback.format_exc().splitlines()
    #写日志
    l.write(msg, log_file, log_type, log_level)
    
#调试信息
def debug(msg=""):
    log(msg, log_level=DEBUG, log_file="info.log")
    
#错误信息
def error(msg=""):
    log(msg, log_file="error.log")
    exit()
    
#访问信息
def access(msg=""):
    log(msg, log_level=INFO, log_file="access.log")

#记录日志，并且过滤未设置的级别
def record(msg=""):
    l.record(msg, type=LOG_SYSTEM, level=DEBUG, record=False)
    
#日志保存
def save():
    l.save(level=DEBUG)
    
if __name__=='__main__':
    error((1, "ddddddd"))
    
