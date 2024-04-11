# -*- coding: utf-8 -*-
# @Time : 2023/09/17 12:49
# @Author : yangyongzhen
# @Email : 534117529@qq.com
# @File : mqttclienttool.py
# @Project : study
import time
import os
from tkinter.ttk import *
from tkinter import *
from datetime import datetime
import time
import threading
from tkinter import messagebox
from ttkbootstrap import Style
import paho.mqtt.client as mqtt
from PIL import Image, ImageTk

global gui  # 全局型式保存GUI句柄

tx_cnt = 0  # 发送条数统计
rx_cnt = 0  # 接收条数统计


def ISHEX(data):  # 判断输入字符串是否为十六进制
    if len(data) % 2:
        return False
    for item in data:
        if item not in '0123456789ABCDEFabcdef':  # 循环判断数字和字符
            return False
    return True


'''GUI'''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('MQTT调试助手-author:blog.csdn.net/qq8864')  # 窗口名称
        self.root.geometry("820x560+500+150")  # 尺寸位置
        self.root.resizable(False, False)
        self.interface()
        Style(
            theme='pulse')  # 主题修改 可选['cyborg', 'journal', 'darkly', 'flatly' 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero','sandstone']
        # self.client.on_log = self.log_callback
        self.isConnect = False
        self._img = None

    def interface(self):
        """"界面编写位置"""
        # --------------------------------操作区域-----------------------------#
        self.fr1 = Frame(self.root)
        self.fr1.place(x=0, y=0, width=220, height=600)  # 区域1位置尺寸
        img_path = os.path.join(os.path.dirname(__file__), 'me.png')
        img = Image.open(img_path)  # 替换为你的图片路径
        img = img.resize((80, 80))
        # self._img = ImageTk.PhotoImage(file = "me.jpg")
        self._img = ImageTk.PhotoImage(img)
        self.about = Label(self.fr1)
        self.about.image = self._img
        self.about.configure(image=self._img)
        self.about.place(x=65, y=0, width=80, height=80)
        pos = 80
        self.lb_server = Label(self.fr1, text='地址:', anchor="e", fg='red')  # 点击可刷新
        self.lb_server.place(x=0, y=pos, width=50, height=35)
        self.txt_server = Text(self.fr1)
        self.txt_server.place(x=65, y=pos, width=155, height=26)
        self.txt_server.insert("1.0", "127.0.0.1")

        self.lb1 = Label(self.fr1, text='端口:', anchor="e", fg='red')  # 点击可刷新
        self.lb1.place(x=0, y=pos + 40, width=50, height=35)
        self.txt_port = Text(self.fr1)
        self.txt_port.place(x=65, y=pos + 40, width=155, height=26)
        self.txt_port.insert("1.0", 1883)

        self.lb1 = Label(self.fr1, text='clientID:', anchor="e", fg='red')  # 点击可刷新
        self.lb1.place(x=0, y=pos + 80, width=50, height=35)
        self.txt_id = Text(self.fr1)
        self.txt_id.place(x=65, y=pos + 80, width=155, height=26)
        self.txt_id.insert("1.0", "mqtt-client")

        self.lb1 = Label(self.fr1, text='用户名:', anchor="e", fg='red')  # 点击可刷新
        self.lb1.place(x=0, y=pos + 120, width=50, height=35)
        self.txt_name = Text(self.fr1)
        self.txt_name.place(x=65, y=pos + 120, width=155, height=26)

        self.lb1 = Label(self.fr1, text='密码 :', anchor="e", fg='red')  # 点击可刷新
        self.lb1.place(x=0, y=pos + 160, width=50, height=35)
        self.txt_pwd = Text(self.fr1)
        self.txt_pwd.place(x=65, y=pos + 160, width=155, height=26)

        self.lb1 = Label(self.fr1, text='心跳 :', anchor="e", fg='red')  # 点击可刷新
        self.lb1.place(x=0, y=pos + 200, width=50, height=35)
        self.txt_heart = Text(self.fr1)
        self.txt_heart.place(x=65, y=pos + 200, width=155, height=26)
        self.txt_heart.insert("1.0", 60)

        self.var_bt1 = StringVar()
        self.var_bt1.set("连接")
        self.btn1 = Button(self.fr1, textvariable=self.var_bt1, command=self.btn_connect)  # 绑定 btn_connect 方法
        self.btn1.place(x=170, y=pos + 240, width=50, height=30)

        self.lb_s = Label(self.fr1, text='订阅主题', bg="yellow", anchor='w')  # 字节统计
        self.lb_s.place(x=5, y=340, width=90, height=28)

        self.txt_sub = Text(self.fr1)
        self.txt_sub.place(x=5, y=368, width=155, height=28)
        self.btn5 = Button(self.fr1, text='订阅', command=self.btn_sub)  # 测试用
        self.btn5.place(x=170, y=368, width=50, height=28)

        self.subitem = Listbox(self.fr1)
        self.subitem.place(x=5, y=402, width=215, height=85)
        # self.subitem.insert(END, "This is a read-only Text widget.")
        self.subitem.bind("<Button-3>", self.on_right_click)

        # -------------------------------文本区域-----------------------------#
        self.fr2 = Frame(self.root)  # 区域1 容器  relief   groove=凹  ridge=凸
        self.fr2.place(x=220, y=0, width=620, height=560)  # 区域1位置尺寸

        self.txt_rx = Text(self.fr2)
        self.txt_rx.place(relheight=0.6, relwidth=0.9, relx=0.05, rely=0.01)  # 比例计算控件尺寸和位置

        self.scrollbar = Scrollbar(self.txt_rx)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_rx.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.txt_rx.yview)
        self.txt_rx.bind("<Configure>", self.check_scrollbar)

        self.lb_t = Label(self.fr2, text='发布主题', bg="yellow", anchor='w')  # 字节统计
        self.lb_t.place(relheight=0.04, relwidth=0.2, relx=0.05, rely=0.62)

        self.lb_qos = Label(self.fr2, text='QoS:', bg="yellow", anchor='w')  # 字节统计
        self.lb_qos.place(relheight=0.04, relwidth=0.15, relx=0.15, rely=0.62)

        self.var_cb1 = IntVar()
        self.comb1 = Combobox(self.fr2, textvariable=self.var_cb1)
        self.comb1['values'] = [0, 1, 2]  # 列出可用等级
        self.comb1.current(0)  # 设置默认选项 0开始
        self.comb1.place(relheight=0.04, relwidth=0.08, relx=0.22, rely=0.615)

        self.txt_topic = Text(self.fr2)
        self.txt_topic.place(relheight=0.05, relwidth=0.9, relx=0.05, rely=0.66)  # 比例计算控件尺寸位置

        self.txt_tx = Text(self.fr2)
        self.txt_tx.place(relheight=0.15, relwidth=0.9, relx=0.05, rely=0.72)  # 比例计算控件尺寸位置

        self.btn6 = Button(self.fr2, text='发送', command=self.btn_send)  # 绑定发送方法
        self.btn6.place(relheight=0.06, relwidth=0.11, relx=0.84, rely=0.88)

        self.btn3 = Button(self.fr2, text='清空', command=self.txt_clr)  # 绑定清空方法
        self.btn4 = Button(self.fr2, text='保存', command=self.savefiles)  # 绑定保存方法
        self.btn3.place(relheight=0.06, relwidth=0.11, relx=0.05, rely=0.88)
        self.btn4.place(relheight=0.06, relwidth=0.11, relx=0.18, rely=0.88)

        self.lb3 = Label(self.fr2, text='接收:0    发送:0', bg="yellow", anchor='w')  # 字节统计
        self.lb3.place(relheight=0.05, relwidth=0.3, relx=0.045, rely=0.945)

        self.lb4 = Label(self.fr2, text=' ', anchor='w', relief=GROOVE)  # 时钟
        self.lb4.place(relheight=0.05, relwidth=0.11, relx=0.84, rely=0.945)

    # ------------------------------------------方法-----------------------------------------------
    def check_scrollbar(self, *args):
        if self.txt_rx.yview() == (0.0, 1.0):
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.place(RIGHT, fill=Y)

    def on_right_click(self, w):
        idx = self.subitem.curselection()
        print("Right-Clicked idx:", idx)
        if idx == ():
            return
        selected_item = self.subitem.get(idx)
        print("Right-Clicked on:", selected_item, idx)
        ret = messagebox.askyesno('取消订阅', "取消订阅:\n" + selected_item)
        if ret:
            self.subitem.delete(idx)
            self.client.unsubscribe(selected_item)
            self.appendTxt("取消订阅:" + selected_item)

    def gettim(self):  # 获取时间 未用
        timestr = time.strftime("%H:%M:%S")  # 获取当前的时间并转化为字符串
        self.lb4.configure(text=timestr)  # 重新设置标签文本
        # tim_str = str(datetime.datetime.now()) + '\n'
        # self.lb4['text'] = tim_str
        # self.lb3['text'] = '接收：'+str(rx_cnt),'发送：'+str(tx_cnt)
        self.txt_rx.after(1000, self.gettim)  # 每隔1s调用函数 gettime 自身获取时间 GUI自带的定时函数

    def txt_clr(self):  # 清空显示
        self.txt_rx.delete(0.0, 'end')  # 清空文本框
        self.txt_tx.delete(0.0, 'end')  # 清空文本框

    def ascii_hex_get(self):  # 获取单选框状态
        if (self.var_cs.get()):
            return False
        else:
            return True

    def tx_rx_cnt(self, rx=0, tx=0):  # 发送接收统计
        global tx_cnt
        global rx_cnt

        rx_cnt += rx
        tx_cnt += tx
        self.lb3['text'] = '接收：' + str(rx_cnt), '发送：' + str(tx_cnt)

    def savefiles(self):  # 保存日志TXT文本
        try:
            with open('log.txt', 'a') as file:  # a方式打开 文本追加模式
                file.write(self.txt_rx.get(0.0, 'end'))
                messagebox.showinfo('提示', '保存成功')
        except:
            messagebox.showinfo('错误', '保存日志文件失败！')

    def log_callback(self, client, userdata, level, buf):
        print(buf)

    def appendTxt(self, msg, flag=None):
        current_t = datetime.now()
        current_ = current_t.strftime("%Y-%m-%d %H:%M:%S ")
        self.txt_rx.insert(END, current_)
        self.txt_rx.insert(END, msg)
        self.txt_rx.insert(END, "\n")
        # 滚动到末尾
        self.txt_rx.see(END)
        self.txt_rx.update_idletasks()

    def connect(self, addr, port, alive=60):
        self.client.connect(addr, port, alive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("disconnect!")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker ok!\n")
            self.appendTxt("Connected to MQTT Broker ok!\n")
            self.var_bt1.set("断开")
            self.isConnect = True
        else:
            print("Failed to connect, return code %d\n", rc)
            self.appendTxt(f"Failed to connect, return code: {rc}\n")
            self.isConnect = False

    def on_message(self, client, userdata, msg):
        self.tx_rx_cnt(1, 0)
        print("Received message: " + msg.payload.decode())
        self.appendTxt(f"Received message:\n[topic]:{msg.topic}\n{msg.payload.decode()}\n", "RECV")

    def subscribe(self, topic):
        # item = Entry(self.subitem).get()
        if topic in self.subitem.get(0, END):
            print("item already exists.")
        else:
            self.appendTxt(f"[订阅topic]:{topic}\n")
            self.client.subscribe(topic)
            self.subitem.insert(END, topic)

    def publish(self, topic, message, qos=0):
        self.client.publish(topic, message, qos)
        self.appendTxt(f"[发布topic]:{topic}\n{message}\n")

    def btn_connect(self):  # 连接
        global isConnect
        if self.var_bt1.get() == '连接':
            server = self.txt_server.get("1.0", END).strip()
            port = self.txt_port.get("1.0", END).strip()
            alive = self.txt_heart.get("1.0", END).strip()
            user = self.txt_name.get("1.0", END).strip()
            psd = self.txt_pwd.get("1.0", END).strip()
            cid = self.txt_id.get("1.0", END).strip()
            # 用户名密码设置
            if len(user) != 0:
                self.client.username_pw_set(user, psd)
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, cid)
            # self.client = mqtt.Client(cid)  # MQTT
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            print("btn connect click: " + server + "," + port + ",QoS:" + self.comb1.get())
            self.appendTxt(f"连接 {server},port:{port}\n")
            self.connect(server, int(port), int(alive))
        else:
            self.disconnect()
            self.var_bt1.set("连接")
            self.isConnect = False
            self.appendTxt(f"断开连接!\n")

    def btn_sub(self):  # 订阅
        if self.isConnect:
            sub = self.txt_sub.get("1.0", END).strip()
            print("btn sub click,topic: " + sub)
            self.subscribe(sub)
        else:
            messagebox.showinfo('提示', '服务器未连接!')

    def btn_send(self):  # 发布
        if self.isConnect:
            pub_topic = self.txt_topic.get("1.0", END).strip()
            payload = self.txt_tx.get("1.0", END).strip()
            print("btn pub click,topic: " + pub_topic)
            self.publish(pub_topic, payload, int(self.comb1.get()))
            self.tx_rx_cnt(0, 1)
        else:
            messagebox.showinfo('提示', '请连接服务器!')


if __name__ == '__main__':

    print('Start...')
    gui = GUI()
    gui.gettim()  # 开启时钟
    gui.root.mainloop()
    print('End...')