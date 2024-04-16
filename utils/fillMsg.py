class FillMsg:
    def __init__(self):
        pass

    def fill_msg(self, obj):
        if(obj['status'] != 0):
            return False
        if(obj['type'] == "chat_message"):
            #聊天信息
            return f"【{obj['type_name']}】[{obj['user_id']}]{obj['user_name']}: {obj['content']}"
        if(obj['type'] == "gift_message"):
            # 礼物信息
            return f"【{obj['type_name']}】[{obj['user_name']}] 送出了 {obj['gift_name']} x {obj['gift_cnt']}"
        if (obj['type'] == "like_message"):
            # 点赞信息
            return f"【{obj['type_name']}】[{obj['user_name']}] 点了 {obj['count']} 个赞"
        if (obj['type'] == "social_message"):
            # 关注信息
            return f"【{obj['type_name']}】[{obj['user_name']}] 关注了主播"
        if (obj['type'] == "fansclub_message"):
            # 粉丝团信息
            return f"【{obj['type_name']}】[{obj['content']}] "
        if (obj['type'] == "live_closed"):
            # 关闭直播间信息
            return f"{obj['type_name']}】"

    # 根据不同类型的消息触发不同的动作，生成动作json然后返回
    def fill_mqtt_json(self, obj):
        if(obj['status'] != 0):
            return False
        if(obj['type'] == "chat_message"):
            #聊天信息
            pass
        if(obj['type'] == "gift_message"):
            # 礼物信息
            return self.fill_gift(obj)
            # return f"【{obj['type_name']}】[{obj['user_name']}] 送出了 {obj['gift_name']} x {obj['gift_cnt']}"
        if (obj['type'] == "like_message"):
            pass
        if (obj['type'] == "social_message"):
            # 关注信息
            pass
        if (obj['type'] == "fansclub_message"):
            # 粉丝团信息
            pass
        if (obj['type'] == "live_closed"):
            # 关闭直播间信息
            return f"{obj['type_name']}】"

    def fill_gift(self, obj):
        print('fill_giftttttt')
        print(obj)
        if obj['gift_name'] == "":
            return False
        if obj['gift_cnt'] <= 0:
            return False
        gift_list = {
            "小心心": 1,
            "大啤酒": 2,
            "粉丝团灯牌": 2,
            "亲吻": 99,
            "抖音": 1,
            "玫瑰": 1,
            "称心如意": 1,
            "人气票": 1,
            "你最好看": 2,
            "棒棒糖": 9,
            "鲜花": 10,
            "加油鸭": 15,
            "送你花花": 49,
            "爱你呦": 52,
            "Thuglife": 99
        }
        times = 0
        if obj['gift_name'] not in gift_list:
            return False
        print(f"收到礼物啦，礼物名称：{obj['gift_name']},礼物数量：{obj['gift_cnt']},是否包含：{obj['gift_name'] in gift_list},数量为：{gift_list[obj['gift_name']]}")


        times = int(gift_list[obj['gift_name']]) * int(obj['gift_cnt'])
        print(f"最终次数为：{times}")
        return times
