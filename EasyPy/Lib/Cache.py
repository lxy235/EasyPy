# !/usr/bin/python
# coding=utf-8
# 
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Cache Library.

from Config import Config
import Log
from Function import *

class Cache():
    # 是否连接
    connected = False
    # 操作句柄
    handler = None
    # 缓存连接参数
    options = {}
    # 配置对象
    config = None
    # 缓存对象
    cache = None
    # __instance
    __instance = None
    
    def __init__(self):
        self.config = Config()

    def connect(self, type=""):
        if '' == type:
            type = self.config.get("cache.data_cache_type")
        module_type = type.title()
        module = "Caches."+module_type
        m = getattr(__import__(module), module_type)
        #print(m)
        className = getattr(m,module_type)
        #print(className)
        try:
            cache = className(self.options)
        except:
            Log.error(L('_CACHE_TYPE_INVALID_')+':'+type)
        return cache

    def setOptions(self, name="", value=""):
        self.options[name] = value

    def getOptions(self, name=""):
        return self.options[name]

    #取得缓存类实例
    @classmethod
    def getinstance(cls, type=""):
        if(cls.__instance == None):
            cls.__instance = Cache()
        return cls.__instance

if __name__=='__main__':
    c = Cache.getinstance()
    c.setOptions("host", "127.0.0.1")
    c.setOptions("post", "6357")
    
    cache = c.connect()
    cache.get()
