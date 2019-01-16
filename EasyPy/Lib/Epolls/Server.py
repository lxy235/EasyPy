# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Server Library.

import socket, select, time, Log
from Epolls.SocketParser import SocketParser

class Server():
    
    #白名单列表, 默认允许本机连接
    __allow_ip = ["127.0.0.1"]
    #epoll对象
    __epoll = ""
    #socket链接
    __socket = ""
    #超时时间设置，客户端10秒内没有任何输入，系统会自动断开
    #从第一次有输入后的10秒开始计时，第一次输入的10秒不计时
    #__timeouts = 5 #秒数
    #监听主机IP, 默认监听
    __host = "0.0.0.0"
    #监听主机端口，默认为8888
    __port = 8888
    #等待连接队列的最大长度
    __listens = 1024
    #设置阻塞模式，1阻塞模式 0非阻塞模式, 默认非阻塞模式
    __block = 0
    #连接列表，值为：socket对象
    __client_connections = {}
    #连接IP列表
    __client_ip = {}
    #连接接受信息列表
    __client_requests = {}
    #注册的应用程序
    __app = ""
    #socket解析对象
    __socket_parser = ""
    #发送给client的数据
    __send_list = ""
    
    def __init__(self, app=""):
        self.__app = app
        self.__socket_parser = SocketParser()
        
    #设置白名单，默认运行本机IP
    def setAllowIp(self, ip_list=[]):
        if len(ip_list) > 0:
            for lv in ip_list: self.__allow_ip.append(lv)
    
    #检测IP是否在白名单里
    def __isAllowIp(self, ip):
        if len(self.__allow_ip) == 0:
            return False
        else:
            try:
                #如果存在返回True，否则抛出异常
                self.__allow_ip.index(ip)
                return True
            except:
                return False
    
    #服务监听            
    def listen(self, port=0):
        #创建socket链接
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #在绑定前让套接字允许复用（两个套接字可以绑定到同一个端口上）
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #绑定主机和端口
        if port == 0:
            port = self.__port
        self.__socket.bind((self.__host, int(port)))
        #等待连接队列的最大长度
        self.__socket.listen(self.__listens)
        #设置阻塞模式，默认为非阻塞模式
        self.__socket.setblocking(self.__block)
        #创建epoll对象
        self.__epoll = select.epoll()
        self.__epoll.register(self.__socket.fileno(), select.EPOLLIN | select.EPOLLET) #工作在ET模式
        #开始服务
        self.__loop()
        
    #开始服务
    def __loop(self):
        try:
            while True:
                events = self.__epoll.poll(-1)
                #print("polling...")
                #print(events)
                for fileno, event in events:
                    #当请求连接时（处理客户端链接）
                    #只有客户端第一次建立链接时会执行一次
                    if fileno == self.__socket.fileno():
                        try:
                            while True:
                                conn_sock, client_values = self.__socket.accept()
                                #print("accept...")
                                client_ip, client_port = client_values
                                conn_sock.setblocking(0)
                                #检测白名单
                                if not self.__isAllowIp(client_ip):
                                    conn_sock.close() #关闭链接
                                    break
                                conn_fileno = conn_sock.fileno()
                                self.__epoll.register(conn_fileno, select.EPOLLIN | select.EPOLLET) #工作在ET模式
                                #conn_sock.settimeout(self.__timeouts)
                                #当前链接进入队列
                                self.__client_connections[conn_fileno] = conn_sock
                                #当前链接IP进入队列
                                self.__client_ip[conn_fileno] = client_ip
                                #当前连接接受信息
                                self.__client_requests[conn_fileno] = b''
                                #记录访问日志
                                #Log.access("host: %s, port: %s" % (client_ip, client_port))
                        except socket.error as e:
                            #print(dir(e))
                            #errno代码为11(EAGAIN)
                            if e.errno == 11:
                                pass
                    #当客户端有输入时
                    #表示对应的文件描述符可以读（包括对端SOCKET正常关闭）
                    elif event & select.EPOLLIN:
                        self.__epollIn(fileno)
                    elif event & select.EPOLLOUT:
                        conn = self.__client_connections[fileno]
                        send_list = self.__send_list
                        #print(send_list)
                        if send_list[0] > 0:
                            self.__socket_parser.send(conn, send_list[0], send_list[1])
                        if send_list[0] <= 0:
                            self.__epoll.modify(fileno, select.EPOLLET)
                            conn.shutdown(socket.SHUT_RDWR)
                        self.__epoll.modify(fileno, select.EPOLLIN)
                    #表示对应的文件描述符被挂断
                    elif event & select.EPOLLHUP:
                        self.__epoll.unregister(fileno)
                        self.__client_connections[fileno].close()
                        del self.__client_connections[fileno]
        finally:
            self.__epoll.unregister(self.__socket.fileno())
            self.__epoll.close()
            self.__socket.close()
    
    #获取处理程序名
    #command 命令号
    def __getHandler(self, command):
        handler_name = "handler_" + str(command)
        handler_list = dir(self.__app)
        if(handler_name in handler_list):
            handler_name = "self._Server__app." + handler_name
        else:
            handler_name = ""
        return handler_name
        
    #处理输入
    #fileno 文件描述符
    def __epollIn(self, fileno):
        try:
            #取得当前链接对象
            conn = self.__client_connections[fileno]
            #取得当前内容
            requests = self.__client_requests[fileno]
            #取得头信息
            header = self.__socket_parser.getHeader(conn)
            cmd = header['cmd']
            if cmd == 0:
                self.__epoll_close(fileno)
                return False
            #获取内容长度
            body_info = self.__socket_parser.getBody(conn, header['body_len'])
            #获取处理程序
            handler_name = self.__getHandler(cmd)
            if len(handler_name) > 0:
                send_list = eval(handler_name)(body_info)
            else:
                send_list = [0,{"error":"cmd not defined"}]
            self.__send_list = send_list
            #处理程序的返回值发送回调用者，返回值格式为[标识符, {}]
            #self.__socket_parser.send(conn, send_list[0], send_list[1])
            #修改文件描述符为可读状态
            self.__epoll.modify(fileno, select.EPOLLOUT)
        except:
            Log.error()
            self.__epoll_close(fileno)
            return False
        
    #关闭连接
    def __epoll_close(self, fileno):
        try:
            self.__client_connections[fileno].shutdown(socket.SHUT_RDWR)
        except:
            pass
        finally:
            self.__epoll.unregister(fileno)
            self.__client_connections[fileno].close()
            del self.__client_connections[fileno]
            del self.__client_ip[fileno]
            del self.__client_requests[fileno]


