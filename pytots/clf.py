
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

LITERAL_TYPES_COLLECTION = [
    typing.Literal,
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
    "LITERAL_TYPES_COLLECTION",
]