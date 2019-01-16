# !/usr/bin/python
# coding=utf-8
# 
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Redis Library.

import redis, Log, sys, json
from Config import Config
from Cache import Cache

class Redis(Cache):
    config = None
    def __init__(self, options={}):
        self.config = Config()
        if "redis" not in sys.modules:
            Log.error(L('_NO_MODULE_')+":redis")
        if len(options) == 0:
            options = {
                "host":self.config.get("redis.host") if self.config.get("redis.host") else "127.0.0.1",
                "port":self.config.get("redis.port") if self.config.get("redis.port") else "6397"
            }
        self.options = options
        self.handler = redis.Redis(**options)
        #set prefix
        if 'prefix' in options:
            self.options['prefix'] = options['prefix']
        else:
            self.options['prefix'] = self.config.get("redis.prefix")
    
    ##
     # 读取缓存
     # @access public
     # @param string $name 缓存变量名
     # @return mixed None
     ##
    def get(self, name=""):
        value = self.handler.get(self.options['prefix']+name)
        value = value.decode('UTF-8')
        try:
            jsonData = json.loads(value)
        except:
            jsonData = value
        return jsonData

    ##
     # 写入缓存
     # @access public
     # @param string $name 缓存变量名
     # @param mixed $value  存储数据
     # @param integer $expire  有效时间（秒）
     # @return boolean
     ##
    def set(self, name="", value="", expire=0):
        name = self.options['prefix']+name
        if isinstance(value, (dict,tuple,list)):
            value = json.dumps(value)
        if isinstance(expire, int) and expire>0:
            result = self.handler.setex(name, value, expire)
        else:
            result = self.handler.set(name, value)
        return result
    
    ##
     # 删除缓存
     # @access public
     # @param string $name 缓存变量名
     # @return boolean
     ##
    def rm(self, name=""):
        self.handler.delete(self.options['prefix']+name)

    ##
     # 清除缓存
     # @access public
     # @return boolean
     ##
    def clear(self):
        return self.handler.flushdb()

if __name__ == "__main__":
    r = Redis()
    r.set("list", {"a":1,"b":2,"c":(3,4)})
    #r.set("list", "ddd")
    data = r.get("list")
    print(data)
    for i in data:
        print(i)