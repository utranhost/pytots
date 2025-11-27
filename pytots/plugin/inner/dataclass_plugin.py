"""
dataclass类处理插件
"""

from dataclasses import is_dataclass
import inspect
from typing import (
    get_type_hints,
    get_origin,
    get_args,
    Final,
    ClassVar
)

from .. import Plugin
from pytots.type_map import map_base_type


class DataclassPlugin(Plugin):
    """
    dataclass类处理插件
    """
    
    name = "dataclass"
    
    
    def is_supported(self, python_type: type) -> bool:
        """
        是否支持该类型
        """
        if inspect.isclass(python_type) and is_dataclass(python_type):
            return True
        return False
    
    
    def converter(self, python_type: type, **extra) -> str:
        """
        转换该类型为 TypeScript 类型
        """
        class_name = python_type.__name__
        
        type_hints = get_type_hints(python_type)
        fields = []
        for field, field_type in type_hints.items():
            # 通过检查 __origin__ 属性来检测 Final 和 ClassVar
            if get_origin(field_type) in [Final, ClassVar]:
                field_type = get_args(field_type)[0]  # 获取 Final 或 ClassVar 的原始类型
            ts_type = map_base_type(field_type, **extra)

            if field_type.__dict__.get("_name") == "Optional":
                fields.append(f"{field}?: {ts_type};")
            else:
                fields.append(f"{field}: {ts_type};")

        fields_str = "\n  ".join(fields)
        
        if self.class_generic_params["define_codes"]:
            generic_params = ", ".join(self.class_generic_params["define_codes"])
            return f"interface {class_name}<{generic_params}> {{\n  {fields_str}\n}}"
        
        return f"interface {class_name} {{\n  {fields_str}\n}}"