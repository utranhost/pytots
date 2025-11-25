from . import Plugin
from pytots.type_map import map_base_type
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

    def converter(self, python_type: type, **extra) -> str:
        """类型转换"""
        fields = []
        for field_name, field_info in python_type.model_fields.items():
            # 获取字段类型
            field_type = field_info.annotation
            if field_type is None:
                # 如果注解为空，尝试从字段信息中获取类型
                field_type = field_info

            ts_type = map_base_type(field_type, **extra)

            # 检查是否为可选字段
            if field_info.is_required():
                fields.append(f"{field_name}: {ts_type};")
            else:
                fields.append(f"{field_name}?: {ts_type};")

        fields_str = "\n  ".join(fields)
        return f"{{\n  {fields_str}\n  }}"


    def is_supported(self, python_type: type) -> bool:
        """是否支持"""
        if isinstance(python_type, type) and issubclass(python_type, SQLModel):
            return True
        return False
