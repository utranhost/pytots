from typing import TypeVar
from . import Plugin


def generic_feild_fill(plugin: Plugin, type_: type) -> str:
    """泛型字段填充"""
    from ..main import convert_to_ts
    from pytots.store import TEMP_CONTEXT, STORE_GENERIC_INTERFACE

    # 提取泛型参数
    gp = (
        [type_]
        if isinstance(type_, TypeVar)
        else type_.__parameters__
        if hasattr(type_, "__parameters__")
        else None
    )
    todo = {}
    if plugin.class_extends_params and gp:
        for param in plugin.class_extends_params:
            if dvs := STORE_GENERIC_INTERFACE.get(param, None):
                for g in gp:
                    if dv := dvs.get(g, None):
                        todo[g] = dv
    if todo:
        TEMP_CONTEXT["typevar"].clear()
        TEMP_CONTEXT["typevar"] = todo
    else:
        TEMP_CONTEXT["typevar"].clear()
    res = convert_to_ts(type_)
    TEMP_CONTEXT["typevar"].clear()
    return res
