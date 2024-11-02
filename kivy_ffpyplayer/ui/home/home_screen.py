# @file    : home_screen
# @time    : 2024/11/1
# @author  : yongpeng.yao
# @desc    :
from kivy.uix.screenmanager import Screen

from ..utils.load_kv import KvLoad


class HomeScreen(Screen):

    def __init__(self, app, **kwargs):
        KvLoad.load(__file__)
        self.app = app
        super().__init__(**kwargs)

    def switch_video_ad_screen(self):
        from ..video_ad.video_ad_screen_ctrl import VideoAdCtrl
        self.app.switch_screen(VideoAdCtrl)