from typing import Literal, TypedDict
from .. import Plugin
from ..tools import generic_feild_fill

from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    Json,
    SecretStr,
    SecretBytes,
    StrictStr,
    StrictInt,
    StrictFloat,
    StrictBool,
    PaymentCardNumber,
    ByteSize,
    PastDate,
    FutureDate,
    PastDatetime,
    FutureDatetime,
    condate,
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    FilePath,
    DirectoryPath,
    NewPath,
    AnyUrl,
    AnyHttpUrl,
    PostgresDsn,
    CockroachDsn,
    AmqpDsn,
    RedisDsn,
    MongoDsn,
    KafkaDsn,
    NatsDsn,
    validate_email,
)



class PydanticPluginOptions(TypedDict):
    """Pydantic 插件选项"""
    exclude: bool    # 是否排除被标记为 exclude 的字段
    type_prefix: Literal["interface", "type"]



class PydanticPlugin(Plugin):
    """Pydantic 插件"""

    name = "pydantic-plugin"
    TYPES_MAP = {
        EmailStr: "string",
        IPvAnyAddress: "string",
        IPvAnyInterface: "string",
        IPvAnyNetwork: "string",
        Json: "any",
        SecretStr: "string",
        SecretBytes: "Uint8Array",
        StrictStr: "string",
        StrictInt: "number",
        StrictFloat: "number",
        StrictBool: "boolean",
        PaymentCardNumber: "string",
        ByteSize: "number",
        PastDate: "Date",
        FutureDate: "Date",
        PastDatetime: "Date",
        FutureDatetime: "Date",
        condate: "Date",
        UUID1: "string",
        UUID3: "string",
        UUID4: "string",
        UUID5: "string",
        FilePath: "string",
        DirectoryPath: "string",
        NewPath: "string",
        AnyUrl: "string",
        AnyHttpUrl: "string",
        HttpUrl: "string",
        PostgresDsn: "string",
        CockroachDsn: "string",
        AmqpDsn: "string",
        RedisDsn: "string",
        MongoDsn: "string",
        KafkaDsn: "string",
        NatsDsn: "string",
        validate_email: "string",
    }
    
    def __init__(self, options: PydanticPluginOptions={}) -> None:
        self.options = options
        self.type_prefix = options.get("type_prefix", "interface")
        
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

        fields_str = "\n  ".join(fields)
        if self.type_prefix == "type":
            return f"{self.type_prefix} {python_type.__name__} = {{\n  {fields_str}\n}}"
        else:
            return f"{self.type_prefix} {python_type.__name__} {{\n  {fields_str}\n}}"

    def is_supported(self, type_: type) -> bool:
        """是否支持该类型"""
        if isinstance(type_, type) and issubclass(type_, BaseModel):
            return True
        return False
