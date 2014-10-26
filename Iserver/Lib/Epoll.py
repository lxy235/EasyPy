# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Epoll Server.

from Epolls.Server import Server
from Epolls.SocketParser import SocketParser

#当前状态码
_STATUS_CODES = 200

#创建服务端
def createServer(app=""):
    return Server(app)

#发送请求
def send(socket_obj, command, body):
    s = SocketParser()
    s.send(socket_obj, command, body)

#获取内容
def getBody(socket_obj):
    s = SocketParser()
    header = s.getHeader(socket_obj)
    if header['cmd'] == 0:
        return False
    body = s.getBody(socket_obj, header['body_len'])
    return body

#获取请求头
def getHeader(socket_obj):
    s = SocketParser()
    header = s.getHeader(socket_obj)
    if header['cmd'] == 0:
        return False
    return header
    
if __name__=='__main__':
    createServer()
