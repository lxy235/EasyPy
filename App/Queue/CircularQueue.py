# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2014-06-06
# @Info: 循环队列

import Log
from Config import Config

class CircularQueue():

    #配置对象
    __config = ""

    #假设队列最大长度
    __maxsize = 1000000

    #队列数据结构
    __sq = {"data":[],"front":0,"rear":0}

    #i    
    __i=0
    
    #初始化
    def __init__(self):
        self.__config = Config()

    #入队列
    def handler_8001(self, p):
        sql = p.get("sql","")
        self.__i = self.__i + 1
        sql = sql % self.__i
        print(sql)
        q=self.__sq
        print("rear = %d" % q['rear'])
        try:
            if ((q['rear']+1)%self.__maxsize == q['front']):
                return [0,{"msg":"error"}]
            q['data'].append(sql)
            q['rear']=(q['rear']+1)%self.__maxsize
        except:
            Log.error()
            return [0,{"msg":"error"}]
        return [8001,{"msg":"success"}]

    #出队列
    def handler_8002(self, p):
        q=self.__sq
        try:
            if q['front'] == q['rear']:
                return [0,{"msg":"error"}]
            e = q['data'][q['front']]
            q['front']=(q['front']+1)%self.__maxsize
        except:
            Log.error()
            return [0,{"msg":"error"}]
        return [8002,e]

    #队列长度
    def handler_8003(self, p):
        q=self.__sq
        try:
            temp = (q['rear']-q['front']+self.__maxsize)%self.__maxsize
        except:
            Log.error()
            return [0,{"msg":"error"}]
        return [8003,temp]

if __name__ == "__main__":
    cq = CircularQueue()

    #入队列，向队列里添加10条sql
    for i in range(10):
        cq.handler_8001({"sql":"select "+str(i)+" from table"})
    
    #获取队列长度
    print(cq.handler_8003())

    #出队列，从队列里取出10条sql
    for i in range(10):
        print(cq.handler_8002())

    #获取队列长度
    print(cq.handler_8003())
    
    
