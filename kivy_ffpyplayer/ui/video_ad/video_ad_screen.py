# @file    : video_ad_screen
# @time    : 2024/5/28
# @author  : yongpeng.yao
# @desc    :
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from ..utils.load_kv import KvLoad

"""
为解决以下问题，修改了部分源码
1. 播放器的音量设置为0但是还有声音的问题
    在源文件 \\Lib\\site-packages\\kivy\\core\\video\\video_ffpyplayer.py
    VideoFFPy类中，MediaPlayer的ff_opts参数中增加了 'an': True 选项 使播放视频时不播放音频 
"""


class VideoAdScreen(Screen):

    def __init__(self, app, **kwargs):
        self.app = app
        KvLoad.load(__file__)
        super(VideoAdScreen, self).__init__(**kwargs)

    def on_leave(self, *args):
        self.clear_data()

    def on_touch_down(self, touch):
        Clock.schedule_once(lambda dt: self.switch_home_screen(), 0.001)
        return super(VideoAdScreen, self).on_touch_down(touch)

    def switch_home_screen(self):
        from ..home.home_screen import HomeScreen
        self.app.switch_screen(HomeScreen)

    def play_video(self, file_path):
        self.hide_widget('id_image')
        self.show_widget('id_video')
        self.ids['id_video'].source = file_path
        self.ids['id_video'].state = 'play'

    def is_playing_video(self):
        return self.ids['id_video'].state == 'play'

    def get_play_video_remaining_time(self):
        return self.ids['id_video'].duration - self.ids['id_video'].position

    def play_image(self, file_path):
        self.hide_widget('id_video')
        self.show_widget('id_image')
        self.ids['id_image'].source = file_path

    def hide_widget(self, name='id_image'):
        """
        隐藏控件
        :param name: 控件名称 id_image / id_video
        """
        self.ids[name].opacity = 0
        self.ids[name].size_hint = (0, 0)
        if name == 'id_video':
            self.ids[name].state = 'stop'

    def show_widget(self, name='id_image'):
        self.ids[name].opacity = 1
        self.ids[name].size_hint = (1, 1)

    def clear_data(self):
        self.ids['id_video'].state = 'stop'
