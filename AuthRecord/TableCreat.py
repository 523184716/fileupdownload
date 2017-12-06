#!/usr/bin/env python
#coding:utf-8

import  os
from peewee import *
import  peewee
import  system_classify
import  ConfigParser
config = ConfigParser.ConfigParser()
sys_result = system_classify.system_classfy()
if sys_result == "window":
    configfile = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\Configs\\baseconf"
else:
    configfile = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/Configs/baseconf"
config.read(configfile)

# class Mydata:
#     def __init__(self,host,user,passwd,port,databases,charset):
#         self.host = host
#         self.user = user
#         self.passed = passwd
#         self.port = port
#         self.database = databases
#         self.charset = charset
#
#     def mysqlconn(self):
#         self.conn = MySQLDatabase(
#             host = self.host,
#             user = self.user,
#             passwd = self.passed,
#             port = self.port,
#             database = self.database,
#             charset = self.charset
#         )
#         return self.conn
# conn = Mydata(config.get("test","host"),config.get("test","user"),config.get("test","passwd"),
#               config.get("test","port"),config.get("test","database"),config.get("test","charset")).mysqlconn()

conn = MySQLDatabase(
    host = config.get("test","host"),
    user = config.get("test","user"),
    passwd = config.get("test","passwd"),
    port = int(config.get("test","port")),
    database = config.get("test","database"),
    charset = config.get("test","charset")
)
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
        database = conn


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
        database = conn

if __name__ == "__main__":
    UserAuth.create_table()
    LogRecord.create_table()
    # AserAuth.create_table()