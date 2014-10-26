# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: 公共方法库
import time
from Const import *
from Config import Config

_config = Config()
_default_lang = _config.get("default_lang")
_lang_set = getattr(__import__("Lang."+_default_lang), _default_lang)
#print(_lang_set._lang)

#获取内存信息
def get_mem_info():
    meminfo = {}
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

#内存使用
def memory_get_usage():
    meminfo = get_mem_info()
    return int(meminfo['Active'].split(" ")[0])

#格式化数字
def number_format(num=0, dec=2):
    if isinstance(num, float):
        format_str = "%."+str(dec)+"f"
        num = format_str % num
    return num

##
 # 记录和统计时间（微秒）和内存使用情况
 # 使用方法:
 # <code>
 # G('begin'); // 记录开始标记位
 # // ... 区间运行代码
 # G('end'); // 记录结束标签位
 # echo G('begin11','end',6); // 统计区间运行时间 精确到小数后6位
 # echo G('begin','end','m'); // 统计区间内存使用情况
 # 如果end标记位没有定义，则会自动以当前作为标记位
 # 其中统计内存使用需要 MEMORY_LIMIT_ON 常量为true才有效
 # </code>
 # @param string $start 开始标签
 # @param string $end 结束标签
 # @param integer|string $dec 小数位或者m
 # @return mixed
 ##
_info = {}; _mem = {}
def G(start='', end='', dec=4):
    global _info, _mem
    if isinstance(end, float):
        _info[start] = end
    elif '' != end:
        try:
            _info[end]
        except:
            _info[end] = round(time.time() * 1000) #获取豪秒
        if MEMORY_LIMIT_ON == 1 and dec == 'm':
            try:
                _mem[end]
            except:
                _mem[end] = memory_get_usage()
            #print(_mem[end]-_mem[start]/1024)
            return number_format(_mem[end]-_mem[start]/1024)
        else:
            #print(_info)
            return number_format(_info[end]-_info[start], dec)
    else:
        _info[start] = round(time.time() * 1000) #获取豪秒
        if MEMORY_LIMIT_ON == 1:
            _mem[start] = memory_get_usage()
        #print(_info)
        #print(_mem)

##
 # 获取和设置语言定义(不区分大小写)
 # @param string|array $name 语言变量
 # @param mixed $value 语言值或者变量
 # @return mixed
 ##
_L = _lang_set._lang
def L(name="", value=""):
    global _L
    if "" == name:
        return _L
    if isinstance(name, str):
        name = name.upper()
        if "" == value:
            try:
                temp = _L[name]
            except:
                temp = name
            return temp
        _L[name] = value
        return
    if isinstance(name,dict):
        _L = dict(_L, **name)
    return

if __name__ == "__main__":
    G('begin')
    for i in range(100000):
        i += i
    G('end')
    print(G('begin','end',6))
    print(G('begin','end','m'))

    L("_LOER_", "hehe")
    L("_UPPE_", "dddd")
    L({"_HEHE_":"kaokao"})
    print(L("_UPPE_"))
    print(L("_LOER_"))
    print(L("_HEHE_"))

    print(L("_TEMPLATE_ERROR_"))