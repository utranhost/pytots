"""
dataclass类处理插件
"""

import typing
from dataclasses import is_dataclass
import inspect
from typing import get_type_hints


from .. import Plugin
from ..tools import generic_feild_fill,assemble_interface_type

class DataclassPluginOptions(typing.TypedDict):
    """
    dataclass类处理插件选项
    """
    type_prefix: typing.Literal["interface", "type"] = "type"


class DataclassPlugin(Plugin):
    """
    dataclass类处理插件
    """
    
    name = "dataclass"
    
    
    def __init__(self, options: DataclassPluginOptions={}) -> None:
        self.options = options
        self.type_prefix = options.get("type_prefix", self.type_prefix)
    
    
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
        
        fields = []
        for field, field_type in get_type_hints(python_type).items():
            ts_type = generic_feild_fill(self,field_type)
            if "undefined" in ts_type:
                fields.append(f"{field}?: {ts_type};")
            else:
                fields.append(f"{field}: {ts_type};")

        fields_str = "\n  ".join(fields)
        
        return assemble_interface_type(self, class_name, fields_str)
