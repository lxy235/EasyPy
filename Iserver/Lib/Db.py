# !/usr/bin/python
# coding=utf-8
#
# @Author: LiXiaoYu
# @Time: 2013-10-17
# @Info: Db

import sys, re, random, math, datetime
import Log
from Function import *
from Config import Config

class Db():

    #配置对象
    config = ""
    #数据库类型
    dbType = ""
    #数据库链接ID，支持多个连接
    linkID = {}
    #当前链接ID
    clinkID = ''
    #是否已经连接数据库
    connected = False
    #数据库连接参数配置
    dbConfig = {}
    #数据配置缓存
    __config_dbs = {}
    #错误信息
    error = ''
    #是否显示调试信息，如果启用会在日志文件里记录SQL语句
    debug = False
    #当前SQL指令
    queryStr = ""
    #日期格式
    __format = "%Y-%m-%d %H:%M:%S"
    #数据库类实例
    __instance = None
    #返回或影响记录数
    numRows = 0
    #当前查询ID
    queryID = None
    #最后插入ID
    lastInsID = 0
    #事务指令数
    transTimes = 0
    
    def __init__(self):
        self.config = Config()
    
    #取得数据库类实例
    @classmethod
    def getinstance(cls, db_config=''):
        if(cls.__instance == None):
            db = Db()
            cls.__instance = db.factory(db_config)
        return cls.__instance
        
    #加载数据库 支持配置文件或DSN
    def factory(self, db_config=''):
        #读取数据库配置
        db_config = self.__parseConfig(db_config)
        #print(db_config)
        
        if db_config['dbms'] == '':
            Log.error(L('_NO_DB_CONFIG_'))
        #数据库类型
        self.dbType = db_config['dbms'].capitalize() #首字母大写
        #加载数据库驱动
        module_name = "Dbs."+self.dbType
        #print(dir(__import__(module_name)))
        #print(sys.modules)
        
        m = getattr(__import__(module_name), self.dbType)
        #print(m)
        
        if module_name not in sys.modules:
            Log.error(L('_NO_DB_MODULE_'))
        #实例化数据库驱动类
        if hasattr(m, self.dbType):
            dbClass = getattr(m, self.dbType)
            db = dbClass(db_config)
            if "pdo" != db_config['dbms'].lower():
                db.dbType = self.dbType.upper()
            if self.config.get('debug'):
                db.debug = True
        else:
            Log.error(L('_NO_SUPPORT_DB_'))
        return db
        
    #分析数据库配置信息
    def __parseConfig(self, db_config=''):
        if db_config != '' and isinstance(db_config, str):
            db_config = self.__parseDSN(db_config)
        else:
            db_config = {
                "dbms":self.config.get('db.type'),
                "username":self.config.get('db.username'),
                "password":self.config.get('db.password'),
                "hostname":self.config.get('db.hostname'),
                "hostport":self.config.get('db.hostport'),
                "database":self.config.get('db.database')
            }
        return db_config
        
    #DSN解析（Data Source Name）
    #事例：mysql://username:password@localhost:3306/dbname
    def __parseDSN(self, dsn_str=''):
        if(dsn_str == ''):
            return False
        p = re.compile("^(.*?)\:\/\/(.*?)\:(.*?)\@(.*?)\:([0-9]{1,6})\/(.*?)$")
        info = p.findall(dsn_str)
        dsn = {
            "dbms":info[0][0],
            "username":info[0][1],
            "password":info[0][2],
            "hostname":info[0][3],
            "hostport":info[0][4],
            "database":info[0][5]
        }
        return dsn
        
    #初始化数据库链接
    def initConnect(self, master=True):
        if 1 == self.config.get('db.deploy_type'): # 部署类型，多库或单库
            #采用分布式主从服务器
            self.clinkID = self.multiConnect(master)
        else:
            #默认单数据库
            if self.connected == False:
                self.clinkID = self.connect()
                
    #连接分布式服务器
    def multiConnect(self,master=False):
        if len(self.__config_dbs) == 0:
        
            if len(self.dbConfig) == 0:
                self.dbConfig = self.config.getSection('db')
                
            for (k, v) in self.dbConfig.items():
                self.__config_dbs[k] = v.split(',')
        
        #数据库读写是否分离
        #是：读写区分服务器，否：读写不区分服务器
        if self.config.get('db.rw_separate'):
            # “写” 操作时master=true，默认往第一个数据库里写数据
            if master:
                r = 0
            else:
                # “读” 操作时master=false，随机抽取一个服务器做读取操作
                r = math.trunc(random.randint(1,len(self.__config_dbs['hostname'])-1))
        else:
            #每次随机链接数据库，从第一个数据库开始
            r = math.trunc(random.randint(0,len(self.__config_dbs['hostname'])-1))
            
        username = self.__config_dbs['username']
        password = self.__config_dbs['password']
        hostname = self.__config_dbs['hostname']
        hostport = self.__config_dbs['hostport']
        database = self.__config_dbs['database']
        #print("r = %s" % r)
        db_config = {
            "username":username[r] if r <= len(username)-1 else username[0],
            "password":password[r] if r <= len(password)-1 else password[0],
            "hostname":hostname[r] if r <= len(hostname)-1 else hostname[0],
            "hostport":hostport[r] if r <= len(hostport)-1 else hostport[0],
            "database":database[r] if r <= len(database)-1 else database[0]
        }
        return self.connect(db_config, r)
        
    #数据库调试，记录当前SQL
    def Debug(self):
        if self.debug:
            G('queryEndTime')
            Log.record(self.queryStr+" [ RunTime:"+str(G('queryStartTime', 'queryEndTime', 6))+"s ]")

    #最近一次查询的SQL语句
    def getLastSql(self):
        return self.queryStr
        
    #最近一次的错误信息
    def getError(self):
        return self.error
            
if __name__ == "__main__":
    #dsn = "mysql://username:password@localhost:3306/dbname"
    db = Db.getinstance()
    print(db.query("SELECT * FROM tp_msg where content = 'ee'"))
    
    #db.execute("insert into tp_msg (content) values ('hehe')")
    #db.execute("update tp_msg set content = 'ee' where content = 'hehe'")
    print(db.error)
    print(db.numRows)
    print(db.lastInsID)






