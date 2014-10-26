# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-11-06
# @Info: Queue Server.

import Epoll
from Config import Config
from App.Queue.CircularQueue import CircularQueue

#获取队列服务配置
_config = Config("Queue")

#初始参数
_port = _config.get("queue.port") #服务端口
_app = CircularQueue()
#_allow_ip = ['192.168.1.100'] #白名单IP列表

#开始服务
s = Epoll.createServer(_app)
#s.setAllowIp(_allow_ip)
s.listen(_port)


