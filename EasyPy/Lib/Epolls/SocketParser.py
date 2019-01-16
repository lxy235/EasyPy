# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Epoll SocketParser.

import socket, struct, json
import Log

class SocketParser():
    
    #信息头的长度(字节数)
    #信息头包括（命令号）和（正文长度）两部分组成，分别为两个无符号短整型数据
    __header_len = 4
    #命令号的长度(字节数)
    __cmd_len = 2
    
    def __init__(self):
        pass
        
    #客户端请求
    #body是一个参数字典，如：{"sql":""}
    def send(self, socket_obj, command=0, body={}):
        #"命令号"转网络字节序
        command = socket.htons(command)
        #字典编码JSON字符串，在python3中pack必须转换成bytes类型
        content = json.dumps(body).encode(encoding='utf-8')
        send_len = len(content)
        #"正文长度"转网络字节序
        body_len = socket.htons(send_len)
        send_data = struct.pack('HH'+str(send_len)+'s', command, body_len, content)
        try:
            return socket_obj.send(send_data)
        except:
            Log.error()
            return False

    #获取请求头
    def getHeader(self, socket_obj):
        recv_cmd = 0 #命令号
        body_len = 0 #内容长度
        header = {'cmd':recv_cmd, 'body_len':body_len}
        try:
            #获取头信息
            header_msg = socket_obj.recv(self.__header_len)
            #判断头的长度是否合法
            if len(header_msg) == self.__header_len:
                recv_cmd, body_len = struct.unpack('HH',header_msg)
                header['cmd'] = socket.ntohs(recv_cmd)
                header['body_len'] = socket.ntohs(body_len)
        except:
            Log.error()
        return header

    #获取请求内容
    def getBody(self, socket_obj, body_len=0):
        if body_len <= 0:
            return ''
        body_contents = ''
        try:
            while len(body_contents) < body_len:
                #python3中要将(字节)对象转换成(字符)后，才能执行连接操作
                temp = socket_obj.recv(body_len - len(body_contents)).decode(encoding='utf-8')
                body_contents += temp
        except:
            Log.error()
            return ''
        #内容解析
        blen = len(body_contents)
        if blen != body_len or blen == 0:
            return ''
        return json.loads(body_contents)


