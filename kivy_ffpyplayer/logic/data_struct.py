#
# @project : advertise
# @file    : data_struct.py
# @time    : 2024/08/02
# @author  : yongpeng.yao
# @version : 0.01
# @desc    : 数据储存处

from dataclasses import dataclass

from ..common.data_class_mixin import DataClassMixin


@dataclass
class PlayADMediaInfo(DataClassMixin):
    """播放广告媒体信息"""
    media_path: str  # 媒体路径
    media_type: str  # 媒体类型  AdvMediaType
    media_duration: int  # 媒体播放时长 单位秒 仅图片有效
