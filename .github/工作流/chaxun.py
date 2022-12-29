import wx
import pymysql

class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        # frame = wx.Frame(parent=None, title='登陆界面', size=(450, 300))
        self.Center()
        self.panel = wx.Panel(self)
        self.LoginInterface()
    def LoginInterface(self):
        # 添加静态标签
        label_user = wx.StaticText(self.panel, -1, "学号:", pos=(80, 50))
        label_pass = wx.StaticText(self.panel, -1, "密码:", pos=(80, 100))
        # 设置输入
        self.entry_user = wx.TextCtrl(self.panel, -1, size=(200, 30), pos=(130, 50))
        self.entry_pass = wx.TextCtrl(self.panel, -1, size=(200, 30), pos=(130, 100), style=wx.TE_PASSWORD)
        # 添加按钮
        self.but_teclogin = wx.Button(self.panel, -1, "教师登陆", size=(80, 30), pos=(80, 150))
        self.but_login = wx.Button(self.panel, -1, "登陆", size=(80, 30), pos=(165, 150))
        self.but_register = wx.Button(self.panel, -1, "注册", size=(80, 30), pos=(250, 150))
        # 给按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.on_but_login, self.but_login)
        self.Bind(wx.EVT_BUTTON, self.on_but_register, self.but_register)
        self.Bind(wx.EVT_BUTTON, self.on_but_teclogin, self.but_teclogin)

    # 单击登陆按钮弹出的对话框----成功
    def show_message(self, word=""):
        dlg = wx.MessageDialog(None, word, u"提示", wx.YES_NO | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            pass
        dlg.Destroy()

    # 点击登陆后的绑定事件
    def on_but_login(self, event):
        # 将输入赋值给定量
        user_name = self.entry_user.GetValue()
        pass_word = self.entry_pass.GetValue()

        sql = """select * from t_user where USERNAME ='%s' """ % (user_name)
        # 判断用户名和密码是否为空
        if user_name and pass_word:
            # 连接数据库
            db = pymysql.connect(host="localhost", user="root",
                                 password="Passw0rd", db="testdb", port=3306)

            cur = db.cursor()
            try:
                cur.execute(sql)

                results = cur.fetchall()
                # 察看用户名是否存在
                if results:
                    # 察看密码是否正确
                    if results[0][2] == pass_word:
                        self.show_message(word="登陆成功")
                        from information import MyApp_information
                        operation = MyApp_information(name=user_name,parent=None, title='查询界面', size=(450, 300))
                        operation.Show()
                        self.Close(True)
                        #from  information import MyApp_information
                        #MyApp_information()
                        pass
                    else:
                        self.show_message(word="密码错误")
                else:
                    self.show_message(word='用户名不存在')
            except Exception as e:
                db.rollback()
            finally:
                # 关闭连接
                db.close()
        else:
            self.show_message(word='学号和密码不能为空')

    def on_but_register(self, event):
        from register import MyApp_register
        operation = MyApp_register(parent=None, title='登陆界面', size=(450, 300))
        operation.Show()
        self.Close(True)
    def on_but_teclogin(self, event):
        from teacherlogin import MyApp_teclogin
        operation = MyApp_teclogin(parent=None, title='教师登陆界面', size=(450, 300))
        operation.Show()
        self.Close(True)

if __name__ == '__main__':
    app = wx.App()
    login = MyApp(None, title="CSDN学生信息管理系统", size=(450, 300))
    login.Show()
    app.MainLoop()