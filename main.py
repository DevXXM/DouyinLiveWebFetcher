#!/usr/bin/python
# coding:utf-8

# @FileName:    main.py
# @Time:        2024/1/2 22:27
# @Author:      bubu
# @Project:     douyinLiveWebFetcher

# from liveMan import DouyinLiveWebFetcher
from utils.gui import GUI
from liveMan import DouyinLiveWebFetcher

if __name__ == '__main__':
    gui = GUI()
    gui.gettim()  # 开启时钟
    gui.root.mainloop()
