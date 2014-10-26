# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Install Server.
# @exam: sudo python install.py

import os, sys, time
from distutils.sysconfig import get_python_lib

sp = get_python_lib()
print('::This site-package path is: %s.' % sp)
time.sleep(1)

libfile = sp + '/library.pth'

if os.path.isfile(libfile):
	print('The python lib install is succfull!')
	sys.exit()

path = os.getcwd()+"/Iserver/Lib"
common = os.getcwd()+"/Iserver/Common"
print('::Python lib path is: %s.' % path)
print('::Python common lib path is: %s.' % common)
time.sleep(2)

if os.path.isfile(path):
	path = os.path.dirname(path)

io = open(libfile, 'w+')
io.write(path+"\n")
io.write(common)
io.close()

print('::Write the <library.pth> in %s dir, File content is python lib path.' % sp)
time.sleep(1)

if os.path.isfile(libfile) == False:
	print('System install error: -1001')
	sys.exit()

print('...........................................')
print('.     [Welcome Use The Python Server]     .')
print('.                                         .')
print('. System Last Modify Time Is : 2014-05-13 .')
print('...........................................')

