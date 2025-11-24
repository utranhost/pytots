from collections import OrderedDict, defaultdict
import types
from typing import (
    Any,
    TypeVar,
    get_type_hints,
    Union,
    Optional,
    Literal,
    NewType,
    TypedDict,
    Protocol,
    Final,
    ClassVar,
    Callable,
    get_origin,
    get_args,
)
import typing
import inspect


from .clf import (
    ARRAY_TYPES_COLLECTION,
    OPTIONAL_TYPES_COLLECTION,
    RECORD_TYPES_COLLECTION,
    SET_TYPES_COLLECTION,
    SINGLE_TYPES_MAP,
    TUPLE_TYPES_COLLECTION,
    UNION_TYPES_COLLECTION,
)


def join_type_args(args: list[str] | tuple[str], sep: str = ", "):
    """
    将类型参数列表转换为字符串。
    """
    return sep.join(map(str, args))


def handle_list_type(args: list[str]) -> str:
    """
    处理list。
    """
    if len(args) == 0:
        return "any[]"
    if len(args) == 1:
        return f"Array<{args[0]}>"
    else:
        return f"[{join_type_args(args)}]"


def handel_tuple_type(args: list[str]) -> str:
    """
    处理tuple类型。
    """
    if len(args) == 0:
        return "any[]"
    if len(args) == 1:
        return f"[{args[0]}]"
    else:
        return f"[{join_type_args(args)}]"


def handle_union_type(args: list[str]) -> str:
    """
    处理 联合类型。
    """
    return join_type_args(args, " | ")


def handle_optional_type(args: list[str]) -> str:
    """
    处理可选类型。
    """
    return f"{handle_union_type(args)} | undefined"


def handle_record_type(args: list[str]) -> str:
    """
    处理 Record类型。
    """
    if len(args) == 0:
        return f"Record<string, any>"
    elif len(args) == 2:
        return f"Record<{args[0]}, {args[1]}>"
    else:
        raise ValueError("Record type must have two arguments.")


def handle_set_type(args: list[str]) -> str:
    """
    处理 Set类型。
    """
    if len(args) == 0:
        return "Set<any>"
    elif len(args) == 1:
        return f"Set<{args[0]}>"
    else:
        raise ValueError("Set type must have one argument.")


def handle_callable_type(args: list[str]) -> str:
    """
    处理 Callable类型。
    """
    if len(args) == 2:
        return f"(...args:{args[0]}) => {args[1]}"
    else:
        raise ValueError("Callable type must have two arguments.")


def map_typedDict_type(typed_dict, **extra) -> str:
    """
    映射 TypedDict
    """
    if not typing.is_typeddict(typed_dict):
        raise TypeError("The argument must be a TypedDict.")

    fields = []
    for field, field_type in get_type_hints(typed_dict).items():
        ts_type = map_base_type(field_type, **extra)
        
        if field_type.__dict__.get('_name') == 'Optional':
            fields.append(f"{field}?: {ts_type};")
        else:
            fields.append(f"{field}: {ts_type};")

    fields_str = "\n  ".join(fields)
    return f"{{\n  {fields_str}\n  }}"


def map_newType_type(new_type, **extra) -> str:
    """
    映射 Python 中的 NewType
    """
    if not isinstance(new_type, NewType):
        raise TypeError("The argument must be a NewType.")

    base_type = new_type.__supertype__
    ts_base_type = map_base_type(base_type, **extra)
    return ts_base_type


def map_typeVar_type(type_var, **extra) -> str:
    """
    映射 Python 中的 TypeVar
    """
    if not isinstance(type_var, TypeVar):
        raise TypeError("The argument must be a TypeVar.")
    bound = type_var.__bound__
    constraints = type_var.__constraints__

    if bound:
        return map_base_type(bound, **extra)
    if constraints:
        return handle_union_type([map_base_type(c, **extra) for c in constraints])

    return "any"


# # 原始复合类型
# ORIGIN_COMPOSITE_TYPES_MAP = {
#     list: "Array",
#     tuple: "Array",
#     dict: "Record",
#     OrderedDict: "Record",
#     defaultdict: "Record",
#     set: "Set",
#     frozenset: "Set",
#     # map: "Map",
# }


# # typing模块的复合类型
# TYPING_COMPOSITE_TYPES_MAP = {
#     Union: "Union",
#     Optional: "Optional",
#     Literal: "Literal",
#     Callable: "Callable",
#     NewType: "NewType",  # 定义新类型，类似于 typescript 中的类型别名
#     TypeVar: "TypeVar",  # 泛型类型变量
#     TypedDict: "TypedDict",  # 定义键值对类型，类似于 typescript 中的 interface
#     Protocol: "Protocol",  # 协议类型，类似于 typescript 中的 interface
#     Final: "Final",  # 修饰， 不可变类型，类似于typescript中的 const 或 readonly
#     ClassVar: "ClassVar",  # 修饰， 类变量，类似于typescript中的 static 变量
# }


def map_base_type(
    python_type,
    *,
    __stack: list[Any] = [],
    process_newType: Optional[Callable[[], None]] = None,
    process_typeVar: Optional[Callable[[], None]] = None,
    process_typedDict: Optional[Callable[[], None]] = None,
    process_missing: Optional[Callable[[], str]] = None,
) -> str:
    """
    基础类型映射
    #### 包含以下类型:
    - 单一类型:
    `int, float, str, bool, bytes, complex, range, type(None)`
    - 原始复合类型:
     `list, tuple, dict, set, frozenset`
    - typing模块的复合类型:
     `Union, Optional, Literal, Callable`

    #### 以下类型只返回名称，映射工作由具体的函数完成:
    - NewType 类型。
    - TypeVar 类型。
    - TypedDict 类型。
    """
    __stack.append(python_type)
    processer = {
        "process_newType": process_newType,
        "process_typeVar": process_typeVar,
        "process_typedDict": process_typedDict,
        "process_missing": process_missing,
    }
    extra = {
        "__stack": __stack,
        **processer,
    }

    if typing.is_typeddict(python_type):  # TypedDict 类型, 只返回名称
        if process_typedDict:
            process_typedDict(*__stack,**processer)
        __stack.pop()
        return python_type.__name__  # type: ignore

    if isinstance(python_type, NewType):  # 处理 NewType 类型，只返回名称
        if process_newType:
            process_newType(*__stack,**processer)
        __stack.pop()
        return python_type.__name__  # type: ignore

    if isinstance(python_type, TypeVar):  # 处理 TypeVar 类型，只返回名称
        if process_typeVar:
            process_typeVar(*__stack,**processer)
        __stack.pop()
        return python_type.__name__



    # 0.特殊实例处理
    if type(python_type) is str:  # 处理字符串,它是字面量
        __stack.pop()
        return python_type

    if type(python_type) is tuple:  # 处理元组
        res = handel_tuple_type([map_base_type(a, **extra) for a in python_type])
        __stack.pop()
        return res
    
    if type(python_type) is list:
        res = handel_tuple_type([map_base_type(a, **extra) for a in python_type])
        __stack.pop()
        return res


    # 1.处理单一类型
    if any(python_type == x for x in SINGLE_TYPES_MAP.keys()):
        __stack.pop()
        return SINGLE_TYPES_MAP[python_type]  # type: ignore


    origin = get_origin(python_type)
    args = get_args(python_type)

    if origin is None:
        origin = python_type

    arg_typpes = [map_base_type(arg, **extra) for arg in args]

    # 2.处理复合类型
    if origin in ARRAY_TYPES_COLLECTION:  # 映射 List
        res = handle_list_type(arg_typpes)
        __stack.pop()
        return res

    if origin in TUPLE_TYPES_COLLECTION:  # 映射 Tuple
        res = handel_tuple_type(arg_typpes)
        __stack.pop()
        return res

    if origin in RECORD_TYPES_COLLECTION:  # 映射 Dict
        res = handle_record_type(arg_typpes)
        __stack.pop()
        return res

    if origin in SET_TYPES_COLLECTION:  # 映射 Set
        res = handle_set_type(arg_typpes)
        __stack.pop()
        return res

    if origin in UNION_TYPES_COLLECTION:  # 映射 Union
        res = handle_union_type(arg_typpes)
        __stack.pop()
        return res

    if origin in OPTIONAL_TYPES_COLLECTION:  # 映射 Optional
        res = handle_optional_type(arg_typpes)
        __stack.pop()
        return res

    if origin is typing.Literal:
        res = join_type_args([repr(arg) for arg in arg_typpes],' | ')
        __stack.pop()
        return res

    if origin is typing.Callable or origin is get_origin(typing.Callable):
        if args[1] == type(None):
            arg_typpes[1] = "void"
        res = handle_callable_type(arg_typpes)
        __stack.pop()
        return res

    if process_missing and (res := process_missing(*__stack,**processer)):  # 处理未知类型
        __stack.pop()
        if type(res) is str:
            return res
        return "any"

    __stack.pop()
    return "any"


__all__ = [
    "map_base_type",
    "map_typedDict_type",
    "map_newType_type",
    "map_typeVar_type",
]
