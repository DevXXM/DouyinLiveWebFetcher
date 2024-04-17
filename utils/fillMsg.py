class FillMsg:
    def __init__(self):
        pass

    def fill_msg(self, obj):
        if (obj['status'] != 0):
            return False
        if (obj['type'] == "chat_message"):
            # 聊天信息
            return f"【{obj['type_name']}】[{obj['user_id']}]{obj['user_name']}: {obj['content']}"
        if (obj['type'] == "gift_message"):
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
        if (obj['status'] != 0):
            return False
        if (obj['type'] == "chat_message"):
            # 聊天信息
            pass
        if (obj['type'] == "gift_message"):
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
            "嘉年华": 30000,
            "梦幻城堡": 28888,
            "浪漫马车": 28888,
            "抖音飞艇": 20000,
            "无尽浪漫": 19999,
            "一路有你": 17999,
            "云中秘境": 13140,
            "蝶·化蝶飞": 10999,
            "抖音1号": 10001,
            "为爱启航": 10001,
            "情定三生": 9666,
            "金鳞化龙": 9000,
            "跨时空之恋": 9000,
            "真爱永恒": 8999,
            "新春狂欢城": 8888,
            "梦回紫禁城": 8666,
            "摩天大厦": 8222,
            "云霄大厦": 7888,
            "星级玫瑰": 7500,
            "等待花开": 7000,
            "蝶·寄相思": 6800,
            "团团圆圆": 6666,
            "月下瀑布": 6666,
            "天空之境": 6399,
            "豪华邮轮": 6000,
            "火龙爆发": 5000,
            "华灯初上": 5000,
            "壁上飞仙": 4999,
            "福佑万家": 4888,
            "奇幻花潮": 4520,
            "星河相望": 4520,
            "真情萌动": 4433,
            "心动丘比特": 4321,
            "海上生明月": 4166,
            "奏响人生": 3666,
            "薰衣草庄园": 3300,
            "私人飞机": 3000,
            "冰冻战车": 3000,
            "传送门": 2999,
            "直升机": 2999,
            "花海泛舟": 2800,
            "奇幻八音盒": 2399,
            "龙珠纳福": 2388,
            "开运醒狮": 2024,
            "浪漫恋人": 1999,
            "单车恋人": 1899,
            "红墙白雪": 1888,
            "炫彩射击": 1888,
            "点亮孤单": 1800,
            "蝶·比翼鸟": 1700,
            "浪漫营地": 1699,
            "花落长亭": 1588,
            "镜中奇缘": 1500,
            "羊羔崽崽": 1488,
            "繁花秘语": 1314,
            "保时捷": 1200,
            "蜜蜂叮叮": 1000,
            "为你而歌": 999,
            "纸短情长": 921,
            "璀璨舞台": 899,
            "掌上明珠": 888,
            "怦然心动": 766,
            "蝶·书中情": 750,
            "日出相伴": 726,
            "万象烟花": 688,
            "环球旅行车": 650,
            "灵龙现世": 600,
            "浪漫花火": 599,
            "娶你回家": 599,
            "热气球": 520,
            "真的爱你": 520,
            "永生花": 520,
            "花开烂漫": 466,
            "真爱玫瑰": 366,
            "一束花开": 366,
            "比心兔兔": 299,
            "真爱表白": 299,
            "ONE礼挑一": 299,
            "爱的守护": 299,
            "蝶·连理枝": 280,
            "星星点灯": 268,
            "一点心意": 266,
            "比心": 199,
            "为你举牌": 199,
            "礼花筒": 199,
            "拳拳出击": 199,
            "多喝热水": 126,
            "龙抬头": 99,
            "爱的小熊": 99,
            "Thuglife": 99,
            "心动玫瑰": 99,
            "龙的传人": 99,
            "爱的纸鹤": 99,
            "捏捏小脸": 99,
            "恋爱脑": 99,
            "黑凤梨": 99,
            "闪耀星辰": 99,
            "为你弹奏": 99,
            "黄桃罐头": 99,
            "荧光棒": 99,
            "亲吻": 99,
            "爱你呦": 52,
            "送你花花": 49,
            "加油鸭": 15,
            "鲜花": 10,
            "棒棒糖": 9,
            "大啤酒": 2,
            "你最好看": 2,
            "小心心": 1,
            "人气票": 1,
            "玫瑰": 1,
            "贺新春": 1,
            "抖音": 1,
            "称心如意": 1
        }
        times = 0
        if obj['gift_name'] not in gift_list:
            return False
        print(
            f"收到礼物啦，礼物名称：{obj['gift_name']},礼物数量：{obj['gift_cnt']},是否包含：{obj['gift_name'] in gift_list},数量为：{gift_list[obj['gift_name']]}")

        times = int(gift_list[obj['gift_name']]) * int(obj['gift_cnt'])
        print(f"最终次数为：{times}")
        return times
