#!/usr/bin/env python
#coding:utf-8

import  wx
import  socket
import  time
import os
import json
import  chardet
from updown_load.AuthRecord.TableCreat import  *
from  MkSecret import mkaesecret
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')
userdict = {}
wildcard = u"Python 文件 (*.py)|*.py|" \
           u"编译的 Python 文件 (*.pyc)|*.pyc|" \
           u" 垃圾邮件文件 (*.spam)|*.spam|" \
           "Egg file (*.egg)|*.egg|" \
           "All files (*.*)|*.*"

class FileTran(wx.Frame):
    def __init__(self,):
        """
        super:继承父类的init方法，传入Frame必须要的参数
        定义一些按钮或者文本框的变量，方便调用
        self.panel:创建幕布，继承self,也就是Frame框架
        self.title、self.content 定义弹框需要的变量
        self.BosSet()、self.Eventbind()构造函数调用的时候就直接初始化这些函数
        :param args:
        :param kwargs:
        """
        super(FileTran,self).__init__(None,title="文件传输",size=(500,300))
        self.panel = wx.Panel(self)
        self.filetrandict = {}
        self.register = wx.Button(self.panel,label="注册")
        self.login = wx.Button(self.panel,label="登录")
        self.logout = wx.Button(self.panel,label="退出")
        self.selectfile = wx.Button(self.panel,label="选择文件")
        self.upload = wx.Button(self.panel,label="上传")
        self.download = wx.Button(self.panel,label="下载文件")
        self.username = wx.StaticText(self.panel,-1,label="登录用户：")
        self.passwd = wx.StaticText(self.panel,style=wx.ALIGN_CENTER,label="登录密码：")
        self.uploadpath = wx.StaticText(self.panel,label="上传路径：",style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
        self.savepath = wx.StaticText(self.panel,label="存放路径：",style=wx.ALIGN_CENTER)
        self.usercontent = wx.TextCtrl(self.panel)
        self.passwdcontent = wx.TextCtrl(self.panel,style=wx.TE_PASSWORD)
        self.uploadfile = wx.TextCtrl(self.panel)
        self.downloadfile = wx.TextCtrl(self.panel)
        self.uploadpathcontent = wx.TextCtrl(self.panel)
        self.savepathcontent = wx.TextCtrl(self.panel)
        self.title = ""
        self.content = ""
        self.BosSet()
        self.Eventbind()
        #self.Show()

    def BosSet(self):
        """
        规划这个界面布局，定义好相应的尺寸器
        往每个尺寸器里面添加对应的按钮或者文本框，并设置相应的样式，比如比例
        self.panel.SetSizer(finallbox) 设置主尺寸器
        :return:
        """
        userbox = wx.BoxSizer()
        passwdbox = wx.BoxSizer()
        logoutbox = wx.BoxSizer()
        loginbox = wx.BoxSizer(wx.VERTICAL)
        registerbox = wx.BoxSizer()
        uploadbox = wx.BoxSizer()
        downloadbox = wx.BoxSizer()
        finallbox = wx.BoxSizer(wx.VERTICAL)
        userbox.Add(self.username,0, wx.ALL|wx.ALIGN_CENTRE,border=3)
        userbox.Add(self.usercontent, proportion=3, flag=wx.EXPAND | wx.ALL, border=3)
        passwdbox.Add(self.passwd,0, wx.ALL|wx.ALIGN_CENTRE,border=3)
        passwdbox.Add(self.passwdcontent, proportion=3, flag=wx.EXPAND | wx.ALL, border=3)
        logoutbox.Add(self.login,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        logoutbox.Add(self.logout,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        loginbox.Add(userbox,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        loginbox.Add(passwdbox,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        loginbox.Add(logoutbox,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        registerbox.Add(self.register,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        registerbox.Add(loginbox,proportion=3,flag=wx.EXPAND|wx.ALL,border=3)
        uploadbox.Add(self.selectfile,proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        uploadbox.Add(self.uploadfile,proportion=2,flag=wx.EXPAND|wx.ALL,border=3)
        uploadbox.Add(self.upload, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        uploadbox.Add(self.uploadpath,0, wx.ALL|wx.ALIGN_CENTRE,border=3)
        uploadbox.Add(self.uploadpathcontent,proportion=2,flag=wx.EXPAND|wx.ALL,border=3)
        downloadbox.Add(self.download,proportion=1,flag=wx.EXPAND|wx.ALL,border=3)
        downloadbox.Add(self.downloadfile,proportion=2,flag=wx.EXPAND|wx.ALL,border=3)
        downloadbox.Add(self.savepath,0, wx.ALL|wx.ALIGN_CENTRE,border=3)
        downloadbox.Add(self.savepathcontent,proportion=2,flag=wx.EXPAND|wx.ALL,border=3)
        finallbox.Add(registerbox,proportion=3,flag=wx.EXPAND|wx.ALL,border=5)
        finallbox.Add(uploadbox,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        finallbox.Add(downloadbox,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        self.panel.SetSizer(finallbox)

    def window_dispaly(self):
        """
        窗口展示
        :return:
        """
        self.Show()

    def LoginDecorator(func):
        """
        装饰器，每次操作之前调用这个以确保登录之后才能继续其他操作
        :return:
        """
        def Auth(*args):
            print userdict
            if userdict:
                func(*args)
            else:
                message = "请先登录，如果没有账号请先注册"
                FileTran().OnAbout("event","login",message)
        return Auth

    def UserLogin(self,event):
        user = str(self.usercontent.GetValue())
        passwd = str(self.passwdcontent.GetValue())
        passwd = mkaesecret(passwd)
        if user == "" or user.strip() == "" or passwd == "" or passwd.strip() == "":
            self.OnAbout(event, "login", "请输入用户和密码")
        else:
            count =  UserAuth.select().where(UserAuth.username==user,UserAuth.passwd==passwd)
            if count:
                global userdict
                userdict = {user:passwd}
                self.OnAbout(event, "login", "登录成功")
            else:
                self.OnAbout(event, "login", "很抱歉，您输入的用户名或密码不正确")

    def UserRegister(self,event):
        user = str(self.usercontent.GetValue())
        passwd = str(self.passwdcontent.GetValue())
        print passwd
        if user == "" or user.strip() == "" or passwd == "" or passwd.strip() == "":
            self.OnAbout(event, "注册", "请输入用户和密码")
        else:
            passwd = mkaesecret(passwd)
            count = UserAuth.select().where(UserAuth.username==user)
            if not count:
                timenow = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                try:
                    UserAuth.insert(username=user,passwd=passwd,create_date=timenow).execute()
                    self.OnAbout(event, "注册", "注册成功")
                except Exception,e:
                    #self.usercontent.SetValue(e.message)
                    self.OnAbout(event, "注册", e.message)
            else:
                self.OnAbout(event,"注册","抱歉!您输入的用户名已存在")

    def UserLogout(self,event):
        global userdict
        userdict = {}
        self.OnAbout(event, "注销", "注销成功")

    @LoginDecorator
    def FileUpload(self,event):
        # if not userdict:
        #     self.uploadfile.SetValue("请先登录，如果没有账号请先注册")
        # else:
        filepath = str(self.uploadfile.GetValue())
        savepath = str(self.uploadpathcontent.GetValue())
        if os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            filename = os.path.basename(filepath)
            self.filetrandict = {"filename":filename,"filesize":filesize,"flag":0,"savepath":savepath,"username":userdict.keys()[0]}
            print self.filetrandict
            socketclient = MySocketClient()
            socketclient.Send(json.dumps(self.filetrandict))
            tran_judge = socketclient.Receive()
            if tran_judge == "ok":
                file = open(filepath,"rb")
                while True:
                    filecontent = file.read(1024)
                    if filecontent:
                        socketclient.Send(filecontent)
                    else:
                        break
                file.close()
                receive = socketclient.Receive()
                self.OnAbout(event,"上传文件",receive)
            else:
                self.OnAbout(event,"上传文件",tran_judge)
        else:
            self.OnAbout(event,"上传文件","文件或者路径不存在，请确认")

    @LoginDecorator
    def FileDownload(self,event):
        # if not userdict:
        #     self.downloadfile.SetValue("请先登录，如果没有账号请先注册")
        # else:
        filepath = str(self.downloadfile.GetValue())
        savepath = str(self.savepathcontent.GetValue())
        filename = os.path.basename(filepath)
        downloadpath = os.path.dirname(filepath)
        self.filetrandict = {"filename":filename,"flag":1,"filepath":downloadpath}
        socketclient = MySocketClient()
        socketclient.Send(json.dumps(self.filetrandict))
        receive_message_init = socketclient.Receive()
        receive_message = eval(receive_message_init)
        if not receive_message["error"]:
            print "开始接收数据"
            filesize = receive_message["filesize"]
            if not os.path.exists(savepath):
                os.makedirs(savepath,777)
            os.chdir(savepath)
            init_size = 0
            file = open(filename,"ab")
            start_time = time.strftime("%Y-%m-%d %H:%M:%S")
            while  True:
                receive_message = socketclient.Receive()
                file.write(receive_message)
                if len(receive_message) < 1024:
                    init_size += len(receive_message)
                    break
                else:
                    init_size += 1024
            file.close()
            end_time = time.strftime("%Y-%m-%d %H:%M:%S")
            if filesize == init_size:
                self.OnAbout(event, "下载", "下载成功")
                LogRecord.insert(username=userdict.keys()[0],tran_type="get",file_path=savepath,file_name=filename,
                                 start_date=start_time,end_date=end_time).execute()
            else:
                self.OnAbout(event,"下载","下载失败")
        else:
            self.title = "下载"
            self.content = json.loads(receive_message_init)["message"]
            self.OnAbout(event,self.title,self.content)

    def OnAbout(self, event,title,content):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        dlg = wx.MessageDialog(self, "{}".format(content), \
                               "{}".format(title), wx.OK)  # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()  # 显示对话框
        dlg.Destroy()  # 当结束之后关闭对话框

    def OnOpen(self,event):
        """ Open a file"""
        filesFilter = "Dicom (*.dcm)|*.dcm|" "All files (*.*)|*.*"
        fileDialog = wx.FileDialog(self, message="选择单个文件", wildcard=filesFilter, style=wx.FD_OPEN)
        dialogResult = fileDialog.ShowModal()
        if dialogResult != wx.ID_OK:
            return
        path = fileDialog.GetPath()
        self.uploadfile.SetLabel(path)

    def __BuildMenus(self):
        """
        wx.MenuBar，在你的框架的顶部放一个菜单栏
        wx.Statusbar，在你的框架底部设置一个区域，来显示状态信息等等
        :return:
        """
        mainMenuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenuItem = fileMenu.Append(0, "打开单个文件")
        self.Bind(wx.EVT_MENU, self.OnOpen, fileMenuItem)
        # saveMenuItem = fileMenu.Append(-1, "保存文件")
        # self.Bind(wx.EVT_MENU, self.__SaveFile, saveMenuItem)
        # savePromptMenuItem = fileMenu.Append(-1, "保存文件及提示覆盖")
        # self.Bind(wx.EVT_MENU, self.__SavePromptFile, savePromptMenuItem)
        # multipleOpenMenuItem = fileMenu.Append(-1, "多文件选择")
        # self.Bind(wx.EVT_MENU, self.__MultipleSelectFiles, multipleOpenMenuItem)
        mainMenuBar.Append(fileMenu, title=u'&文件')
        self.SetMenuBar(mainMenuBar)

    def OnButton1(self, event):
        """
        利用wx.FileDialog创建一个文件选择框，获取选择文件的路径以及可选文件类型
        如果有选择文件的话dlg.ShowModal()  == wx.ID_OK，如果没有选择文件就是不等于
        :param event:
        :return:
        """
        dlg = wx.FileDialog(self, message=u"选择文件",
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()  # 返回一个list，如[u'E:\\test_python\\Demo\\ColourDialog.py', u'E:\\test_python\\Demo\\DirDialog.py']
            print paths[0]
            self.uploadfile.SetValue(paths[0])
            for path in paths:
                print path  # E:\test_python\Demo\ColourDialog.py E:\test_python\Demo\DirDialog.py
        dlg.Destroy()

    def Eventbind(self):
        self.login.Bind(wx.EVT_BUTTON,self.UserLogin)
        self.logout.Bind(wx.EVT_BUTTON,self.UserLogout)
        self.register.Bind(wx.EVT_BUTTON,self.UserRegister)
        self.selectfile.Bind(wx.EVT_BUTTON,self.OnButton1)
        self.upload.Bind(wx.EVT_BUTTON,self.FileUpload)
        self.download.Bind(wx.EVT_BUTTON,self.FileDownload)

class MySocketClient:
    def __init__(self):
        self.init = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.conn = self.init.connect(("192.192.1.34",8822))

    def Send(self,data):
        self.init.send(data)

    def Receive(self):
        message = self.init.recv(1024)
        return  message

if __name__ == "__main__":
    app = wx.App()
    FileTran().window_dispaly()
    app.MainLoop()