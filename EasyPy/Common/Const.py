# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Const

#日志类型
LOG_SYSTEM = 1 # 系统日志
LOG_QUEUE  = 2 # 队列日志

#日志级别
CRITICAL = 50  # 临界值错误: 超过临界值的错误，例如一天24小时，而输入的是25小时这样
ERROR = 40     # 一般错误: 一般性错误
WARNING = 30   # 警告性错误: 需要发出警告的错误
INFO = 20      # 信息: 程序输出信息
DEBUG = 10     # 调试: 调试信息

#系统级别
MEMORY_LIMIT_ON = 1
