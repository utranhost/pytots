import typing
from typing import (
    Any,
    TypeVar,
    get_type_hints,
    NewType,
    get_origin,
    get_args,
    TYPE_CHECKING,
)
from builtins import Ellipsis

if TYPE_CHECKING:
    from .processer import (
        Extra,
        Processers,
        ProcessNewTypeFunc,
        ProcessTypeVarFunc,
        ProcessTypedDictFunc,
        ProcessEnumFunc,
        ProcessMissingFunc,
    )


from .clf import (
    ARRAY_TYPES_COLLECTION,
    LITERAL_TYPES_COLLECTION,
    OPTIONAL_TYPES_COLLECTION,
    RECORD_TYPES_COLLECTION,
    SET_TYPES_COLLECTION,
    SINGLE_TYPES_MAP,
    TUPLE_TYPES_COLLECTION,
    UNION_TYPES_COLLECTION,
    QUEUE_TYPES_COLLECTION,
    COUNTER_TYPES_COLLECTION,
    CHAINMAP_TYPES_COLLECTION,
    REPLACEABLE_TYPES_MAP,
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
    
    支持:
    - tuple[] -> any[] (可变长度元组)
    - tuple[T] -> [T] (单元素元组)
    - tuple[T1, T2, ...] -> [T1, T2, ...] (固定长度元组)
    - tuple[T, ...] -> T[] (可变长度元组)
    """
    if len(args) == 0:
        # tuple[] 表示可变长度元组
        return "any[]"
    elif len(args) == 1:
        # tuple[T] 表示单元素元组
        return f"[{args[0]}]"
    elif len(args) == 2 and (args[1] == "..." or args[1] is Ellipsis):
        # tuple[T, ...] 表示可变长度元组
        return f"{args[0]}[]"
    else:
        # tuple[T1, T2, ...] 表示固定长度元组
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


def handle_set_type(origin: type, args: list[str]) -> str:
    """
    处理 Set类型。
    
    支持:
    - set[T] -> Set<T>
    - frozenset[T] -> ReadonlySet<T>
    - set -> Set<any>
    - frozenset -> ReadonlySet<any>
    """
    typeName = "Set" if origin is set else "ReadonlySet"
    if len(args) == 0:
        return f"{typeName}<any>"
    elif len(args) == 1:
        return f"{typeName}<{args[0]}>"
    else:
        raise ValueError("Set type must have one argument.")


def handle_deque_type(args: list[str]) -> str:
    """
    处理 deque 类型。
    
    支持:
    - deque[T] -> Array<T>
    - deque -> Array<any>
    """
    if len(args) == 0:
        return "Array<any>"
    elif len(args) == 1:
        return f"Array<{args[0]}>"
    else:
        raise ValueError("Deque type must have one argument.")


def handle_counter_type(args: list[str]) -> str:
    """
    处理 Counter 类型。
    
    支持:
    - Counter[T] -> Record<T, number>
    - Counter -> Record<any, number>
    """
    if len(args) == 0:
        return "Record<any, number>"
    elif len(args) == 1:
        return f"Record<{args[0]}, number>"
    else:
        raise ValueError("Counter type must have one argument.")


def handle_chainmap_type(args: list[str]) -> str:
    """
    处理 ChainMap 类型。
    
    支持:
    - ChainMap[K, V] -> Record<K, V>
    - ChainMap -> Record<any, any>
    """
    if len(args) == 0:
        return "Record<any, any>"
    elif len(args) == 2:
        return f"Record<{args[0]}, {args[1]}>"
    else:
        raise ValueError("ChainMap type must have two arguments.")


def handle_callable_type(args: list[str]) -> str:
    """
    处理 Callable类型。
    """
    if len(args) == 2:
        return f"(...args:{args[0]}) => {args[1]}"
    else:
        raise ValueError("Callable type must have two arguments.")


def handle_literal_type(args: list[Any]) -> str:
    """
    处理 Literal 类型。
    将 Python 的 Literal 类型映射为 TypeScript 的联合类型。
    """
    if len(args) == 0:
        return "never"
    
    # 处理 Literal 参数，确保字符串类型正确引用
    literal_args = []
    for arg in args:
        if isinstance(arg, str):
            # 字符串类型需要添加引号
            literal_args.append(f"'{arg}'")
        elif isinstance(arg, bool):
            # 布尔值转为小写
            literal_args.append(str(arg).lower())
        elif isinstance(arg, (int, float)):
            # 数字类型直接使用
            literal_args.append(str(arg))
        else:
            # 其他类型尝试转换为字符串
            literal_args.append(str(arg))
    
    return join_type_args(literal_args, " | ")


def map_typedDict_type(typed_dict, **extra) -> str:
    """
    映射 TypedDict
    """
    if not typing.is_typeddict(typed_dict):
        raise TypeError("The argument must be a TypedDict.")

    fields = []
    for field, field_type in get_type_hints(typed_dict).items():
        ts_type = map_base_type(field_type, **extra)

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

def map_type_alias_type(type_alias, **extra) -> str:
    """
    映射 Python 中的 TypeAlias
    """
    if not isinstance(type_alias, typing.TypeAlias):
        raise TypeError("The argument must be a TypeAlias.")

    base_type = type_alias.__supertype__
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


def map_enum_type(enum_type, **extra) -> str:
    """
    映射 Python 中的枚举类型
    """
    import enum
    if not isinstance(enum_type, type) or not issubclass(enum_type, enum.Enum):
        raise TypeError("The argument must be an Enum class.")
    
    # 获取枚举成员
    members = []
    for member in enum_type:
        if isinstance(member.value, str):
            members.append(f"{member.name} = '{member.value}'")
        else:
            members.append(f"{member.name} = {member.value}")
    
    members_str = ",\n  ".join(members)
    return f"enum {enum_type.__name__} {{\n  {members_str},\n}}"


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
    python_type: Any,
    *,
    __stack: list[Any] = [],
    process_newType: 'ProcessNewTypeFunc',
    process_typeVar: 'ProcessTypeVarFunc',
    process_typedDict: 'ProcessTypedDictFunc',
    process_enum: 'ProcessEnumFunc',
    process_missing: 'ProcessMissingFunc',
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

    # 判断是否为自引用
    if python_type in __stack:
        return f"{python_type.__name__}"

    __stack.append(python_type)
    processer: "Processers" = {
        "process_newType": process_newType,
        "process_typeVar": process_typeVar,
        "process_typedDict": process_typedDict,
        "process_enum": process_enum,
        "process_missing": process_missing,
    }
    extra: "Extra" = {
        "__stack": __stack,
        **processer,
    }

    if typing.is_typeddict(python_type):  # TypedDict 类型, 只返回名称
        if process_typedDict:
            process_typedDict(*__stack, **processer)
        __stack.pop()
        return python_type.__name__  # type: ignore

    if isinstance(python_type, NewType):  # 处理 NewType 类型，只返回名称
        if process_newType:
            process_newType(*__stack, **processer)
        __stack.pop()
        return python_type.__name__  # type: ignore

    if isinstance(python_type, TypeVar):  # 处理 TypeVar 类型，只返回名称
        if process_typeVar:
            process_typeVar(*__stack, **processer)
        __stack.pop()
        return python_type.__name__

    # 0.特殊实例处理
    if type(python_type) is str:  # 处理字符串,它是字面量
        __stack.pop()
        return python_type
    
    
    if type(python_type) in [int,float]:  # 处理数字,它是字面量
        __stack.pop()
        return python_type
    
    
    if type(python_type) is typing.Any:  # 处理 Any 类型
        __stack.pop()
        return "any"
    

    if type(python_type) is tuple:  # 处理元组
        # 检查是否是可变长度元组 (tuple[T, ...])
        if len(python_type) == 2 and python_type[1] is Ellipsis:
            # tuple[T, ...] -> T[]
            element_type = map_base_type(python_type[0], **extra)
            res = f"{element_type}[]"
        else:
            # 固定长度元组
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
        # 检查是否是可变长度元组 (tuple[T, ...])
        if len(args) == 2 and args[1] is Ellipsis:
            # tuple[T, ...] -> T[]
            element_type = map_base_type(args[0], **extra)
            res = f"{element_type}[]"
        else:
            res = handel_tuple_type(arg_typpes)
        __stack.pop()
        return res

    if origin in RECORD_TYPES_COLLECTION:  # 映射 Dict
        res = handle_record_type(arg_typpes)
        __stack.pop()
        return res

    if origin in SET_TYPES_COLLECTION:  # 映射 Set
        res = handle_set_type(origin,arg_typpes)
        __stack.pop()
        return res

    if origin in QUEUE_TYPES_COLLECTION:  # 映射 Deque
        res = handle_deque_type(arg_typpes)
        __stack.pop()
        return res

    if origin in COUNTER_TYPES_COLLECTION:  # 映射 Counter
        res = handle_counter_type(arg_typpes)
        __stack.pop()
        return res

    if origin in CHAINMAP_TYPES_COLLECTION:  # 映射 ChainMap
        res = handle_chainmap_type(arg_typpes)
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

    if origin in LITERAL_TYPES_COLLECTION:  # 映射 Literal
        res = handle_literal_type(args)
        __stack.pop()
        return res

    if origin is typing.Callable or origin is get_origin(typing.Callable):
        if args[1] == type(None):
            arg_typpes[1] = "void"
        res = handle_callable_type(arg_typpes)
        __stack.pop()
        return res

    if process_missing and (
        res := process_missing(*__stack, **processer)
    ):  # 处理未知类型
        __stack.pop()
        if type(res) is str:
            return res
        return "any"

    if origin in REPLACEABLE_TYPES_MAP:
        res = REPLACEABLE_TYPES_MAP[origin]
        __stack.pop()
        return res
    
    # any 兜底
    __stack.pop()
    return "any"


__all__ = [
    "map_base_type",
    "map_typedDict_type",
    "map_newType_type",
    "map_type_alias_type",
    "map_typeVar_type",
    "map_enum_type",
    "handle_deque_type",
    "handle_counter_type",
    "handle_chainmap_type",
]
