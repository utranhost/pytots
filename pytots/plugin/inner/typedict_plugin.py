"""
typedict类处理插件
"""
import typing
from typing import (
    get_type_hints,
    get_origin,
    get_args,
    Final,
    ClassVar
)

from .. import Plugin
from ..tools import generic_feild_fill,assemble_interface_type



class TypedDictPluginOptions(typing.TypedDict):
    """
    typedict类处理插件选项
    """
    type_prefix: typing.Literal["interface", "type"] = "type"


class TypedDictPlugin(Plugin):
    """
    typedict类处理插件
    """
    
    name = "typedict"
    
    
    def __init__(self, options: TypedDictPluginOptions={}) -> None:
        self.options = options
        self.type_prefix = options.get("type_prefix", "type")
    
    
    def is_supported(self, python_type: type) -> bool:
        """
        是否支持该类型
        """
        if typing.is_typeddict(python_type):
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
            # 检查是否为可选类型
            origin = get_origin(field_type)
            if origin is typing.Optional or (
                hasattr(field_type, "__dict__")
                and field_type.__dict__.get("_name") == "Optional"
            ):
                fields.append(f"{field}?: {ts_type};")
            else:
                fields.append(f"{field}: {ts_type};")

        fields_str = "\n  ".join(fields)

        return assemble_interface_type(self, class_name, fields_str)
