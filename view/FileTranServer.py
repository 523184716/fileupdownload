#!/usr/bin/env python
#coding:utf-8

import SocketServer
import os
import  time
import json
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')
from updown_load.AuthRecord.TableCreat import LogRecord
class Mysocket(SocketServer.BaseRequestHandler):
    def setup(self):
        print "start"

    def handle(self):
        while True:
            print "##############################################################"
            receive = self.request.recv(512)
            print receive
            if receive:
                result = eval(receive)
            print result
            if not result["flag"]:
                print "上传文件"
                recsize = result["filesize"]
                filename = result["filename"]
                savepath = result["savepath"]
                if savepath:
                    if not os.path.exists(savepath):
                        os.makedirs(savepath,777)
                    #if os.path.
                    init_size = 0
                    uploadpath = savepath+"\\"+filename
                    self.request.send("ok")
                    file = open(uploadpath,"ab")
                    print "start receiving"
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    receivedata = self.request.recv(1024)
                    while True:
                        file.write(receivedata)
                        if len(receivedata) < 1024:
                            init_size += len(receivedata)
                            break
                        else:
                            init_size += 1024
                        receivedata = self.request.recv(1024)
                    file.close()
                    end_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    print "transfer over"
                    if recsize == init_size:
                        self.request.send("上传成功")
                        LogRecord.insert(username=result["username"],tran_type="post",file_path=savepath,file_name=filename,
                        start_date=start_time,end_date=end_time).execute()
                    else:
                        self.request.send("上传失败")
                else:
                    self.request.send("请填写上传目录")
            else:
                print "下载文件"
                downloadpath = result["filepath"]
                if not downloadpath:
                    downloadpath = os.getcwd()
                if  os.path.exists(downloadpath):
                    filename = result["filename"]
                    if  filename in os.listdir(downloadpath):
                        os.chdir(downloadpath)
                        file_size = os.stat(filename).st_size
                        send_dict = {"error":0,"message":"文件存在,开始下载","filesize":file_size}
                        self.request.send(json.dumps(send_dict))
                        file = open(filename,"rb")
                        while True:
                            message = file.read(1024)
                            if message:
                                self.request.send(message)
                            else:
                                break
                        file.close()
                    else:
                        send_dict = {"error":1,"message":"文件不存在,请确认"}
                        self.request.send(json.dumps(send_dict))
                else:
                    send_dict = {"error": 1, "message": "目录不存在,请确认"}
                    self.request.send(json.dumps(send_dict))
            break

    def finish(self):
        pass

if __name__ == "__main__":
    server = SocketServer.ThreadingTCPServer(("0.0.0.0",8822),Mysocket)
    server.serve_forever()