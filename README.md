iserver简介
iserver是一个用python编写的网络服务框架（编译版本3.4.1），使用的是epool网络模型

测试机配置
处理器 2x Genuine Intel(R) CPU T2050 @ 1.60GHz

内存 2060MB (673MB used)

nginx开启进程数
root 2413 2409 0 09:17 pts/0 00:00:00 grep -i nginx

www 2414 2411 2 09:17 ? 00:00:00 nginx: master process

www 2415 2411 0 09:17 ? 00:00:00 nginx: worker process

www 2416 2411 0 09:17 ? 00:00:00 nginx: worker process

www 2417 2411 0 09:17 ? 00:00:00 nginx: worker process

www 2418 2411 0 09:17 ? 00:00:00 nginx: worker process

www 2419 2411 0 09:17 ? 00:00:00 nginx: worker process

www 2420 2411 0 09:17 ? 00:00:00 nginx: worker process

www 2421 2411 0 09:17 ? 00:00:00 nginx: worker process
开启8个nginx进程消耗120M内存（15M * 8 = 120M）

php-cgi 开启进程数
root 2424 1 0 09:17 ? 00:00:00 php-fpm: master process

www 2425 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2426 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2427 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2428 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2429 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2430 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2431 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2432 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2433 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2434 2424 0 09:17 ? 00:00:00 php-fpm: pool www

www 2435 2424 0 09:17 ? 00:00:00 php-fpm: pool www

开启12个php-cgi进程消耗掉240M内存（20M * 12 = 240M）

测试流程
首先启动队列网络服务，php向队列服务里插入一条insert sql，例如

client.php

复制代码
 1 /**
 2  * socket client
 3  * a NULL填充字符串
 4  * n 表式无符号短整形
 5  * 无符号短整型, 总是16点，大端字节序
 6  */
 7 function insert_queue($cmd, $sql) {
 8     $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
 9     try {
10       socket_connect($s, "127.0.0.1", 8888);
11       $list = json_encode(array(
12         "sql"=>$sql
13       ));
14       $len = strlen($list);
15       $param = pack("nna{$len}",$cmd, $len, $list);
16       socket_write($s, $param, strlen($param));
17       socket_recv($s, $head, 4, 0);
18       //var_dump($head);
19       if($head != '') {
20         $a = unpack("ncmd/nlen", $head);
21         $cmd = $a['cmd'];
22         $len = $a['len'];
23         if($cmd == 8001) {
24           socket_recv($s, $body, $len, 0);
25           //echo $body;exit;
26           $b = json_decode($body, true);
27           socket_close($s);
28           return $b;
29         }
30       }
31       socket_close($s);
32     } catch(Exception $e) {
33       echo $e->getMessage();
34     }
35 }
36 $temp = insert_queue(8001, "insert into (num) values (%d)");
复制代码
CircularQueue.py

复制代码
 1 # !/usr/bin/python
 2 # coding=utf-8
 3 #
 4 # @Author: LiXiaoYu
 5 # @Time: 2013-11-06
 6 # @Info: CircularQueue Server.
 7 
 8 import Epoll
 9 from Config import Config
10 from App.Queue.CircularQueue import CircularQueue
11 
12 #获取队列服务配置
13 _config = Config("Queue")
14 
15 #初始参数
16 _port = _config.get("queue.port") #服务端口
17 _app = CircularQueue()
18 #_allow_ip = ['192.168.1.100'] #白名单IP列表
19 
20 #开始服务
21 s = Epoll.createServer(_app)
22 #s.setAllowIp(_allow_ip)
23 s.listen(_port)
24 
25 启动服务
26 python3 circularQueue.py
复制代码
测试工具
使用webbench模拟1万并发

webbench -c 10000 -t 30 http://192.168.1.100/client.php

测试结果
lxy@lenovo-pc:~$ webbench -c 10000 -t 30 http://192.168.1.100/client.php

Webbench - Simple Web Benchmark 1.5

Copyright (c) Radim Kolar 1997-2004, GPL Open Source Software.

Benchmarking: GET http://192.168.1.100/client.php

10000 clients, running 30 sec.

Speed=43226 pages/min, 129975 bytes/sec.

Requests: 21613 susceed, 0 failed.

每分钟相应请求数43226 pages/min，每秒钟传输数据量129975 bytes/sec

相当于每天可以处理（43226 * 60 * 24 = 62245440）个请求
