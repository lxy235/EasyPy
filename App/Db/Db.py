# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Queue

import Config, Util
from collections import deque

class Queue():
    
    #配置对象
    __config = ""
    #队列字典
    __sqs = {}
    
    #初始化
    def __init__(self):
        self.__config = Config.create()
        #初始化队列
        queue_type_list = str(self.__config.get("queue.queue_type_list"))
        for queue_type in queue_type_list.split(","):
            self.__sqs[queue_type] = deque([])
        
    #进队列
    def handler_8001(self, p):
        i = p.get('i',0)
        queue_type = p.get('queue_type',"")
        if queue_type not in self.__sqs:
            return [4001,{"msg":"queue type error"}]
        try:
            del p['queue_type']
            self.__sqs[queue_type].append(p)
        except:
            Util.error()
        return [8001,{"msg":"success"+str(i)}]
        
    #出队列
    def handler_8002(self, p):
        queue_type = p.get('queue_type',"")
        if queue_type not in self.__sqs:
            return [4001,{"msg":"queue type error"}]
        try:
            temp = self.__sqs[queue_type].popleft()
            if temp == -1:
                return [4002,{"msg":"queue is empty"}]
        except:
            Util.error()
        return [8002,temp]
    
    #队列长度
    def handler_8003(self, p):
        queue_type = p.get('queue_type',"")
        if queue_type not in self.__sqs:
            return [4001,{"msg":"queue type error"}]
        try:
            temp = len(self.__sqs[queue_type])
        except:
            Util.error()
        return [8003,temp]
        
if __name__ == "__main__":
    q = Queue()
    queue_type = "sql"
    
    #入队列，向队列里添加10条sql
    for i in range(10):
        q.handler_8001({"queue_type":queue_type,"sql":"select "+str(i)+" from table"})
    #获取队列长度
    print(q.handler_8003({"queue_type":queue_type}))
    
    #出队列，从队列里取出10条sql
    for i in range(10):
        print(q.handler_8002({"queue_type":queue_type}))
    #获取队列长度
    print(q.handler_8003({"queue_type":queue_type}))
    
    
    
    
