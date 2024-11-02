# @file    : data_class_mixin
# @time    : 2024/8/2
# @author  : yongpeng.yao
# @desc    :

from dataclasses import field, make_dataclass, MISSING


class DataClassMixin:

    @classmethod
    def from_dict(cls, data: dict) -> 'DataClassMixin':
        return make_part_dataclass(cls, **data)

    @classmethod
    def from_kwargs(cls, **kwargs) -> 'DataClassMixin':
        return make_part_dataclass(cls, **kwargs)


def make_part_dataclass(super_cls, **kwargs):
    """创建数据类 没有赋值的字段默认为None"""
    if not hasattr(super_cls, '__dataclass_fields__'):
        raise ValueError(f'{super_cls} is not a dataclass')
    part_cls_name = super_cls.__name__ + 'Part'  # 新的子类名称
    field_name_list, part_cls_fields = [], []
    for field_name, field_ in super_cls.__dataclass_fields__.items():
        field_name_list.append(field_name)
        field_default = None
        if field_.default != MISSING:  # 如果设置了默认值，使用默认值
            field_default = field_.default
        part_cls_fields.append((field_name, field_.type, field(default=field_default)))
    part_cls = make_dataclass(part_cls_name, part_cls_fields, bases=(super_cls,))
    # 删除kwargs中没有的字段
    new_kwargs = {key: kwargs[key] for key in kwargs if key in field_name_list}
    return part_cls(**new_kwargs)
