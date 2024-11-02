# @file    : main_window
# @time    : 2024/11/1
# @author  : yongpeng.yao
# @desc    :
from kivy.uix.boxlayout import BoxLayout

from ..home.home_screen import HomeScreen
from ..utils.load_kv import KvLoad


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        KvLoad.load(__file__)
        super(MainWindow, self).__init__(**kwargs)
        self.switch_screen(HomeScreen)

    def switch_screen(self, screen):
        self.ids['id_screen_manager'].switch_to(screen(self))

    def get_current_screen(self):
        return self.ids['id_screen_manager'].current_screen