
from collections import OrderedDict, defaultdict
import types
import typing

# 单一类型映射表
SINGLE_TYPES_MAP = {
    int: "number",
    float: "number",
    str: "string",
    bool: "boolean",
    bytes: "Uint8Array",
    complex: "string",  # complex 类型不能直接映射，使用字符串替代
    range: "number[]",  # range 类型不能直接映射，使用 number[] 代替
    type(None): "null | undefined",  # 需要特殊处理
}

# Pydantic 类型映射
PYDANTIC_TYPES_MAP = {
    # 基础字段类型
    "EmailStr": "string",
    "HttpUrl": "string", 
    "IPvAnyAddress": "string",
    "IPvAnyInterface": "string",
    "IPvAnyNetwork": "string",
    "Json": "any",
    "SecretStr": "string",
    "SecretBytes": "Uint8Array",
    "StrictStr": "string",
    "StrictInt": "number",
    "StrictFloat": "number",
    "StrictBool": "boolean",
    "PaymentCardNumber": "string",
    "ByteSize": "number",
    "PastDate": "Date",
    "FutureDate": "Date",
    "PastDatetime": "Date",
    "FutureDatetime": "Date",
    "condate": "Date",
    "UUID1": "string",
    "UUID3": "string",
    "UUID4": "string",
    "UUID5": "string",
    "FilePath": "string",
    "DirectoryPath": "string",
    "NewPath": "string",
    "AnyUrl": "string",
    "AnyHttpUrl": "string",
    "HttpUrl": "string",
    "PostgresDsn": "string",
    "CockroachDsn": "string",
    "AmqpDsn": "string",
    "RedisDsn": "string",
    "MongoDsn": "string",
    "KafkaDsn": "string",
    "NatsDsn": "string",
    "validate_email": "string",
}

# SQLModel 类型映射 (SQLModel 基于 Pydantic)
SQLMODEL_TYPES_MAP = {
    # SQLModel 特有类型
    "AutoString": "string",
    "BigInteger": "number",
    "Binary": "Uint8Array",
    "Boolean": "boolean",
    "Date": "Date",
    "DateTime": "Date",
    "Enum": "string",
    "Float": "number",
    "Integer": "number",
    "Interval": "number",
    "LargeBinary": "Uint8Array",
    "Numeric": "number",
    "SmallInteger": "number",
    "String": "string",
    "Text": "string",
    "Time": "string",
    "Unicode": "string",
    "UnicodeText": "string",
}


ARRAY_TYPES_COLLECTION = [
    list,
    typing.List,
]

TUPLE_TYPES_COLLECTION = [
    tuple,
    typing.Tuple,
]


RECORD_TYPES_COLLECTION = [
    dict,
    OrderedDict,
    defaultdict,
    typing.Dict,
    typing.OrderedDict,
    typing.DefaultDict,
    typing.get_origin(typing.Mapping),
    typing.get_origin(typing.MutableMapping),
]


SET_TYPES_COLLECTION =[
    set,
    frozenset,
    typing.Set,
    typing.FrozenSet,
    typing.get_origin(typing.MutableSet),
]

UNION_TYPES_COLLECTION = [
    typing.Union,
    types.UnionType
]

OPTIONAL_TYPES_COLLECTION = [
    typing.Optional,
]





__all__ = [
    "SINGLE_TYPES_MAP",
    "PYDANTIC_TYPES_MAP",
    "SQLMODEL_TYPES_MAP",
    "ARRAY_TYPES_COLLECTION",
    "TUPLE_TYPES_COLLECTION",
    "RECORD_TYPES_COLLECTION",
    "SET_TYPES_COLLECTION",
    "UNION_TYPES_COLLECTION",
    "OPTIONAL_TYPES_COLLECTION",
]