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



def assemble_interface_type(plugin: Plugin, class_name: str, fields_str: str) -> str:
    """组装interface和type类型, 自动处理泛型参数和继承"""
    extends_str = ""
    if plugin.type_prefix == "interface":
        if plugin.class_extends_params:
            extends_str = f" extends {', '.join(plugin.class_extends_params)}"
        
        if plugin.class_generic_params["define_codes"]:
            generic_params = ", ".join(plugin.class_generic_params["define_codes"])
            return f"interface {class_name}{extends_str}<{generic_params}> {{\n  {fields_str}\n}}"
        
        return f"interface {class_name}{extends_str} {{\n  {fields_str}\n}}"
    else:
        if plugin.class_extends_params:
            extends_str = f" &{' & '.join(plugin.class_extends_params)};"
        
        if plugin.class_generic_params["define_codes"]:
            generic_params = ", ".join(plugin.class_generic_params["define_codes"])
            return f"type {class_name}<{generic_params}> = {{\n  {fields_str}\n}}{extends_str}"
        
        return f"type {class_name} = {{\n  {fields_str}\n}}{extends_str}"
