from typing import Literal, TypedDict

from .. import Plugin,use_plugin
from ..plus.pydantic_plugin import PydanticPlugin
from ..tools import generic_feild_fill,assemble_interface_type

from sqlmodel import (
    SQLModel,
    AutoString,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time,
    Unicode,
    UnicodeText,
)




class SqlModelPluginOptions(TypedDict):
    """SQLModel 插件选项"""
    exclude: bool    # 是否排除被标记为 exclude 的字段
    type_prefix: Literal["interface", "type"]

class SqlModelPlugin(Plugin):
    """SQLModel 插件"""

    name = "sqlmodel-plugin"
    TYPES_MAP = {
        # SQLModel 特有类型
        AutoString: "string",
        BigInteger: "number",
        Boolean: "boolean",
        Date: "Date",
        DateTime: "Date",
        Enum: "string",
        Float: "number",
        Integer: "number",
        Interval: "number",
        LargeBinary: "Uint8Array",
        Numeric: "number",
        SmallInteger: "number",
        String: "string",
        Text: "string",
        Time: "string",
        Unicode: "string",
        UnicodeText: "string",
    }
    
    def __init__(self, options: SqlModelPluginOptions={}) -> None:
        self.options = options
        self.type_prefix = options.get("type_prefix", "type")
        use_plugin(PydanticPlugin(options))

    def converter(self, python_type: type, **extra) -> str:
        """类型转换"""
        fields = []
        for field_name, field_info in python_type.model_fields.items():
            # 获取字段类型
            field_type = field_info.annotation
            if field_type is None:
                # 如果注解为空，尝试从字段信息中获取类型
                field_type = field_info


            # 检查是否排除被标记为 exclude 的字段
            if self.options.get("exclude", False) and field_info.exclude:
                continue
            
            ts_type = generic_feild_fill(self,field_type)
            
            # 检查是否为可选字段
            if field_info.is_required():
                fields.append(f"{field_name}: {ts_type};")
            else:
                fields.append(f"{field_name}?: {ts_type};")
        
        class_name = python_type.__name__
        fields_str = "\n  ".join(fields)
        return assemble_interface_type(self, class_name, fields_str)


    def is_supported(self, python_type: type) -> bool:
        """是否支持"""
        if isinstance(python_type, type) and issubclass(python_type, SQLModel):
            return True
        return False
