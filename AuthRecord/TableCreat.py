#!/usr/bin/env python
#coding:utf-8

import  os
from peewee import *
import  peewee
import  system_classify
import  ConfigParser

config = ConfigParser.ConfigParser()
configfile = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+os.sep+"Configs"+os.sep+"Baseconfig.conf"
config.read(configfile)

class MysqlConn:
    def __init__(self,host,user,passwd,port,database,charset):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__port = port
        self.__database = database
        self.__charset = charset

    def initconn(self):
        conn = peewee.MySQLDatabase(
            host = self.__host,
            user =  self.__user,
            passwd = self.__passwd,
            port = self.__port,
            database = self.__database,
            charset = self.__charset
        )
        return  conn
mysqlinit = MysqlConn(config.get("test","host"),config.get("test","user"),config.get("test","passwd"),
            int(config.get("test","port")),config.get("test","database"),config.get("test","charset")).initconn()

# conn = MySQLDatabase(
#     host = config.get("test","host"),
#     user = config.get("test","user"),
#     passwd = config.get("test","passwd"),
#     port = int(config.get("test","port")),
#     database = config.get("test","database"),
#     charset = config.get("test","charset")
# )
class UserAuth(Model):
    """
    这种模型类名就是要创建的表名，
    database = conn  这个就是连接目标数据库，其他都是定义的字段
    """
    id = PrimaryKeyField()
    username = CharField(max_length=30)
    passwd = CharField(max_length=50)
    create_date = DateTimeField()
    class Meta:
        database = mysqlinit


class LogRecord(Model):
    id = PrimaryKeyField()
    #username = ForeignKeyField(UserAuth)
    username = CharField(max_length=30)
    tran_type = CharField(max_length=20)
    file_path = CharField(max_length=50)
    file_name = CharField(max_length=50)
    start_date = DateTimeField()
    end_date = DateTimeField()
    class Meta:
        database = mysqlinit

if __name__ == "__main__":
    UserAuth.create_table()
    LogRecord.create_table()
    # AserAuth.create_table()