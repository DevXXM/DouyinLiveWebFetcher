# -*- coding: utf-8 -*-
# @Time : 2023/09/17 12:49
# @Author : yangyongzhen
# @Email : 534117529@qq.com
# @File : mqttclienttool.py
# @Project : study
from queue import Queue


class QueueManager:
    def __init__(self):
        self.queue = Queue()
        # 创建一个先进先出的队列
        # 创建一个先进后出的栈
        # 创建一个带有优先级的队列


    @staticmethod
    def get_queue():
        return QueueManager().queue