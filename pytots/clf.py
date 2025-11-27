from collections import OrderedDict, defaultdict, deque, ChainMap, Counter
import types
import typing
import decimal
import uuid
import datetime

# 单一类型映射表
SINGLE_TYPES_MAP = {
    int: "number",
    float: "number",
    str: "string",
    bool: "boolean",
    bytes: "Uint8Array",  # bytes类型映射为TypeScript的Uint8Array
    bytearray: "Uint8Array",  # bytearray类型也映射为Uint8Array
    complex: "{real: number, imag: number}",  # complex类型映射为包含实部和虚部的对象
    range: "{start: number, stop: number, step: number}",  # range类型映射为包含start/stop/step的对象
    type(None): "null | undefined",  # 需要特殊处理
    object: "any",  # Python的object类型映射为TypeScript的any
    decimal.Decimal: "number",  # decimal类型映射为TypeScript的number
    uuid.UUID: "string",  # uuid类型映射为TypeScript的string
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


SET_TYPES_COLLECTION = [
    set,
    frozenset,
    typing.Set,
    typing.FrozenSet,
    typing.get_origin(typing.MutableSet),
    typing.get_origin(typing.AbstractSet),
]

# 队列类型集合
QUEUE_TYPES_COLLECTION = [
    deque,
    typing.get_origin(typing.Deque),
]

# 计数器类型集合
COUNTER_TYPES_COLLECTION = [
    Counter,
]

# 链式映射类型集合
CHAINMAP_TYPES_COLLECTION = [
    ChainMap,
]

UNION_TYPES_COLLECTION = [typing.Union, types.UnionType]

OPTIONAL_TYPES_COLLECTION = [
    typing.Optional,
]

LITERAL_TYPES_COLLECTION = [
    typing.Literal,
]


# 可替换的类型映射
REPLACEABLE_TYPES_MAP = {
    datetime.date: "Date",
    datetime.datetime: "Date",
    None: "undefined | null",
}


# 可替换类型提供替换的函数接口
def replaceable_type_map(
    type_: datetime.date | datetime.datetime | None, 
    value: str
) -> bool:
    """
    可替换类型映射函数，用于将可替换类型映射为 TypeScript 类型。
    Args:
        type_: 可替换类型
        value: 可替换类型的默认值
    Returns:
        TypeScript 类型字符串
    """
    if type_ in REPLACEABLE_TYPES_MAP:
        REPLACEABLE_TYPES_MAP[type_] = value
        return True
    else:
        return False




__all__ = [
    "SINGLE_TYPES_MAP",
    "ARRAY_TYPES_COLLECTION",
    "TUPLE_TYPES_COLLECTION",
    "RECORD_TYPES_COLLECTION",
    "SET_TYPES_COLLECTION",
    "QUEUE_TYPES_COLLECTION",
    "COUNTER_TYPES_COLLECTION",
    "CHAINMAP_TYPES_COLLECTION",
    "UNION_TYPES_COLLECTION",
    "OPTIONAL_TYPES_COLLECTION",
    "LITERAL_TYPES_COLLECTION",
    "REPLACEABLE_TYPES_MAP",
    "replaceable_type_map",
]
