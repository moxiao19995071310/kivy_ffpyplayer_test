# @file    : play_video_ad_logic
# @time    : 2024/11/1
# @author  : yongpeng.yao
# @desc    :
import os
import pathlib
from enum import StrEnum
from typing import List, Optional

from kivy_ffpyplayer.common.global_var import APP_PATH
from kivy_ffpyplayer.logic.data_struct import PlayADMediaInfo

IMAGE_DURATION = 3  # 图片默认播放时长


class AdMediaType(StrEnum):
    IMAGE = 'image'
    VIDEO = 'video'
    UNKNOWN = 'unknown'


def get_local_ad_path() -> str:
    return APP_PATH + '\\local_file'


def is_image_or_video_by_suffix(suffix):
    image_suffix = ['.jpg', '.jpeg', '.png', '.gif']
    video_suffix = ['.mp4', '.mov', '.avi', '.wmv', '.ogv']
    if suffix in image_suffix:
        return AdMediaType.IMAGE
    elif suffix in video_suffix:
        return AdMediaType.VIDEO
    else:
        return AdMediaType.UNKNOWN


class PlayVideoAdLogic:
    play_list: Optional[List[PlayADMediaInfo]] = None  # 播放列表
    current_play_index = 0  # 当前播放索引

    @classmethod
    def update_play_list(cls):
        if not cls.play_list:
            local_play_list = LocalVideoAdLogic.get_local_video_advert_list()
            if local_play_list and local_play_list != cls.play_list:  # 本地广告列表
                cls.play_list = local_play_list

    @classmethod
    def get_play_list(cls) -> List[PlayADMediaInfo]:
        cls.update_play_list()
        return cls.play_list

    @classmethod
    def get_play_unit(cls):
        if not cls.play_list:
            return None
        if cls.current_play_index >= len(cls.play_list):
            cls.current_play_index = 0  # 当播放索引超出范围，重置为0
        return cls.play_list[cls.current_play_index]

    @classmethod
    def index_self_add(cls):
        cls.current_play_index += 1


class LocalVideoAdLogic:

    @classmethod
    def get_local_video_advert_list(cls) -> List[PlayADMediaInfo]:
        local_ad_path = get_local_ad_path()
        result = []
        if not os.path.isdir(local_ad_path):
            return result
        for file in os.listdir(local_ad_path):
            file_path = os.path.join(local_ad_path, file)
            if not os.path.isfile(file_path):
                continue
            file_path_obj = pathlib.Path(file)
            _, suffix = file_path_obj.stem, file_path_obj.suffix
            image_or_video = is_image_or_video_by_suffix(suffix)
            if image_or_video != AdMediaType.UNKNOWN:
                media_info = {
                    'media_path': file_path,
                    'media_type': image_or_video,
                    'media_duration': IMAGE_DURATION
                }
                result.append(PlayADMediaInfo.from_dict(media_info))
        return result
