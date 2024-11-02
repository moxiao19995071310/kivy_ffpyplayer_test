# @file    : video_ad_ctrl
# @time    : 2024/6/13
# @author  : yongpeng.yao
# @desc    :
from abc import abstractmethod

from kivy.clock import Clock
from kivy.logger import Logger

from .video_ad_screen import VideoAdScreen
from kivy_ffpyplayer import logic as ad_logic

PLAY_END_PAUSE_TIME = 0.1  # 视频播放结束后的停顿时间


class VideoAdPathMix:

    @staticmethod
    @abstractmethod
    def is_can_play(video_advert_list) -> bool:
        """是否可以播放广告视频"""
        raise NotImplementedError()


class VideoAdCtrl(VideoAdScreen, VideoAdPathMix):

    def __init__(self, app, **kwargs):
        self.play_logic = ad_logic.PlayVideoAdLogic  # 播放逻辑静态类
        super().__init__(app, **kwargs)
        self.play_advert_task = Clock.create_trigger(self._do_play_advert)  # 播放广告任务
        self.play_video_advert_check_state_task = None  # 播放视频广告检查状态任务
        self.play_next_image_delayed_task = None  # 图片广告延迟任务

    def on_enter(self, *args):
        self.play_advert_task.timeout = 0  # 立即播放广告
        self.play_advert_task()

    def on_leave(self, *args):
        self.play_advert_task.cancel()
        if self.play_video_advert_check_state_task:
            self.play_video_advert_check_state_task.cancel()
            self.play_video_advert_check_state_task = None
        if self.play_next_image_delayed_task:
            self.play_next_image_delayed_task.cancel()
            self.play_next_image_delayed_task = None
        super().on_leave(*args)
        Logger.info('VideoAdCtrl on_leave')

    def update_play_list(self):
        """更新播放列表"""
        self.play_logic.update_play_list()

    @staticmethod
    def is_can_play(video_advert_list):
        play_list = ad_logic.PlayVideoAdLogic.get_play_list()
        if not play_list:
            return False

        return True

    def _do_play_advert(self, *args):
        """
        播放广告
        """
        _ = args
        if self.app.get_current_screen() != self:  # 判断在当前页面
            return

        self.update_play_list()  # 更新当前播放列表
        play_unit = self.play_logic.get_play_unit()
        Logger.info(f'播放广告 _do_play_advert 当前播放索引：{self.play_logic.current_play_index} {play_unit}')

        try:
            if play_unit.media_type == ad_logic.AdMediaType.VIDEO:  # 视频广告
                self.play_video(play_unit.media_path)
                Logger.info(f'play_video 播放视频:{play_unit.media_path}')
                # 对播放的视频广告检查状态
                self.play_video_advert_check_state_task = Clock.create_trigger(
                    self._do_play_video_advert_check_state)
                self.play_video_advert_check_state_task()
            else:  # 图片广告
                self.play_image(play_unit.media_path)
                duration_time = play_unit.media_duration
                Logger.info(f'play_image 播放图片:{play_unit.media_path} duration_time:{duration_time}')
                # 图片停留duration_time秒  之后播放下一个广告
                self.play_next_image_delayed_task = Clock.create_trigger(
                    lambda dt: self._play_next_advert(), duration_time)
                self.play_next_image_delayed_task()
        except Exception as e:
            _ = e
            Logger.exception('_do_play_advert error')

    def _do_play_video_advert_check_state(self, *args):
        """对播放的视频广告检查状态"""
        _ = args
        if self.app.get_current_screen() != self:  # 判断在当前页面
            return

        try:
            is_playing = self.is_playing_video()
            remaining_time = self.get_play_video_remaining_time()
            Logger.info('检查视频广告 is_playing {}, remaining_time {}'.format(is_playing, remaining_time))
            if not is_playing:  # 视频广告播放完毕，播放下一个广告
                self._play_next_advert(PLAY_END_PAUSE_TIME)
            else:
                # 注* 当播放第一个视频时，ffmpeg播放组件需要初始化，视频剩余时间不准确 [-1 - (-1) = 0] 所以这里设置一个间隔，再次检查
                once_timeout = round(remaining_time, 4) if remaining_time > 0 else PLAY_END_PAUSE_TIME
                self.play_video_advert_check_state_task.timeout = once_timeout
                self.play_video_advert_check_state_task()
        except Exception as e:
            _ = e
            Logger.exception('_do_play_video_advert_check_state error')

    def _play_next_advert(self, timeout=0.0):
        """播放下一个广告"""
        if self.app.get_current_screen() != self:  # 判断在当前页面
            return

        self.play_logic.index_self_add()  # 播放索引自增
        self.play_advert_task.timeout = timeout
        self.play_advert_task()
