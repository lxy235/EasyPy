# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Mysql Driver

from Db import Db
import pymysql
import Log
from Function import *

class Mysql(Db):
    
    def __init__(self, db_config=''):
        super().__init__()
        if db_config != '':
            self.dbConfig = db_config
    
    #链接数据库
    def connect(self, db_config='', linkNum=0):
        #print("db_config = %s" % db_config)
        #print("linkNum = %s" % linkNum)
        try:
            self.linkID[linkNum]
        except Exception as e:
            if db_config == '':
                db_config = self.dbConfig
            #print(db_config)
            #创建数据库连接
            try:
                database = {
                    "host":str(db_config['hostname']), 
                    "user":str(db_config['username']), 
                    "passwd":str(db_config['password'])
                }
                #处理不带端口号的socket连接情
                if '' != db_config['hostport']:
                    database['port']=int(db_config['hostport'])
                #print(database)
                self.linkID[linkNum] = pymysql.connect(**database)
                if '' != db_config['database']:
                    self.linkID[linkNum].select_db(str(db_config['database']))
                dbVersion = self.linkID[linkNum].server_version
                if dbVersion >= "4.1":
                    self.linkID[linkNum].query("SET NAMES %s" % self.config.get("db.charset"))
                #设置sql_mode
                if dbVersion > "5.0.1":
                    self.linkID[linkNum].query("SET sql_mode=''")
                #标记连接成功
                self.connected = True
                #注销数据库连接配置信息
                if 1 != self.config.get("db.deploy_type"):
                    self.dbConfig = ''
            except pymysql.Error as e:
                Log.error(e)
        #print(self.linkID[linkNum])
        return self.linkID[linkNum]
                
    #释放查询结果
    def free(self):
        self.queryID.close()
        self.queryID = None
    
    #关闭数据库
    def close():
        try:
            if None != self.queryID:
                self.queryID.close()
            if '' != self.clinkID:
                self.clinkID.close()
        except pymysql.Error as e:
            Log.error(e)
        self.clinkID = ''
        self.queryID = None
        
    #显示错误信息并显示当前sql
    def error(self, str=''):
        self.error = str.__str__()
        if self.debug and '' != self.queryStr:
            self.error += "\n [ SQL ] : "+self.queryStr
        return self.error
        
    #执行查询
    def query(self, sql=''):
        self.initConnect(False)
        if '' == self.clinkID: 
            return False
        self.queryStr = sql
        #释放前次查询结果
        if self.queryID:
            self.free()
        #记录开始执行时间
        G('queryStartTime')
        try:
            self.queryID = self.clinkID.cursor()
            self.queryID.execute(sql)
            self.Debug()
        except pymysql.Error as e:
            self.error(e)
            return False
        #print(self.queryID)
        self.numRows = self.queryID.rowcount
        #print(self.numRows)
        #exit()
        return self.queryID.fetchall()
    
    #执行语句
    def execute(self, sql):
        self.initConnect(True)
        if '' == self.clinkID: 
            return False
        self.queryStr = sql
        #释放前次查询结果
        if self.queryID:
            self.free()
        #记录开始执行时间
        G('queryStartTime')
        try:
            self.queryID = self.clinkID.cursor()
            self.queryID.execute(sql)
            self.Debug()
        except pymysql.Error as e:
            self.error(e)
            return False
        #print(self.queryID)
        self.numRows = self.clinkID.affected_rows()
        self.lastInsID = self.clinkID.insert_id()
        
    #启动事务
    def startTrans(self):
        self.initConnect(True)
        if '' == self.clinkID: 
            return False
        if 0 == self.transTimes:
            self.clinkID.query("START TRANSACTION")
        self.transTimes+=1
        return;
        
    #提交事务
    def commit(self):
        if self.transTimes > 0:
            try:
                self.clinkID.query("COMMIT")
                self.transTimes = 0
            except pymysql.Error as e:
                self.error(e)
        return True
        
    #回滚事务
    def rollback(self):
        if self.transTimes > 0:
            try:
                self.clinkID.query("ROLLBACK")
                self.transTimes = 0
            except pymysql.Error as e:
                self.error(e)
        return True
    
if __name__ == "__main__":
    pass
    
    
    
    
