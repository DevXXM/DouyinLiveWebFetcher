class formatMsg():
    def __init__(self):
        pass


    def formatQue(self, obj):
        ret = {
            'type': "live_closed",
            'type_id': -1,
            'status': 3,
            'type_name': "直播间已结束",
            'content': content,
        }

    def _create_ret(self, type_name, **kwargs):
        ret = {
            'type': type_name,
            'status': 0,
            **kwargs
        }
        self.q.put(ret)