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
            # 关注信息
            return f"{obj['type_name']}】"


    def send_to_mqtt(self, obj):
        pass