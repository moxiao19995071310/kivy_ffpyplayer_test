# @file    : main_app
# @time    : 2024/11/1
# @author  : yongpeng.yao
# @desc    :
import os
import threading
import time

import psutil
from kivy.app import App
from kivy.logger import Logger

from ui import MainWindow


class MainApp(App):
    def build(self):
        self.start_listen()
        return MainWindow()

    def start_listen(self):
        def listen():
            while True:
                self.check_process_info()
                time.sleep(60)

        threading.Thread(target=listen, name='Listen', daemon=True).start()

    @staticmethod
    def check_process_info():
        Logger.info("System cpu info:{}".format(psutil.cpu_times_percent()))
        _m_process = psutil.Process(os.getpid())
        fmt = "Process cpu:{:.2f}%, mem:{:.2f}%/{:.2f}Mb, threads:{}/{}"
        Logger.info(fmt.format(_m_process.cpu_percent(), _m_process.memory_percent(),
                               _m_process.memory_info().rss / 1024 / 1024,
                               _m_process.num_threads(),
                               threading.active_count()))

        thread_info = map(lambda t: "{}-0x{}".format(t.name, hex(t.ident).rjust(8, "0")), threading.enumerate())
        Logger.info("Threads:{}".format(", ".join(thread_info)))


if __name__ == '__main__':
    MainApp().run()
