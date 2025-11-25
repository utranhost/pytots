"""
处理器和转换器函数
"""

import inspect
from typing import (
    Any,
    get_type_hints,
    get_origin,
    get_args,
    Callable,
    Final,
    ClassVar,
    TypedDict,NewType
)
from dataclasses import is_dataclass
from pytots.type_map import (
    map_base_type,
    map_typedDict_type,
    map_newType_type,
    map_typeVar_type,
)
from pytots.plugin import PLUGINS

STORE_PROCESSED_NEWTYPE = {}
STORE_PROCESSED_TYPEVAR = {}
STORE_PROCESSED_TYPEDDICT = {}
STORE_PROCESSED_MISSING = {}


def store_missing_type(type_,type_name, content: str):
    """
    存储缺失的类型映射
    """
    STORE_PROCESSED_MISSING[type_name] = STORE_PROCESSED_MISSING.get(type_name,{})
    STORE_PROCESSED_MISSING[type_name][type_] = content


def exist_missing_type(type_) -> bool:
    """
    检查是否存在缺失的类型映射
    """
    return any(type_ in STORE_PROCESSED_MISSING[type_name] for type_name in STORE_PROCESSED_MISSING.keys())



def convert_typedDict_to_ts(typed_dict, **extra: 'Extra') -> str:
    """
    将 Python 的 TypedDict 转换为 TypeScript 的 interface 定义。

    #### 示例:
    ```# python
    class MyDict(TypedDict):
        name: str
        age: int

    ```

    ```# typescript
    interface MyDict {
      name: string;
      age: number;
    }
    """
    fields_str = map_typedDict_type(typed_dict, **extra)
    return f"interface {typed_dict.__name__}\n  {fields_str}\n"


def convert_newType_to_ts(new_type, **extra:'Extra') -> str:
    """
    将 Python 中的 NewType 转换为 TypeScript 的类型别名。

    #### 示例:
    ```# python
    UserId = NewType("UserId", int)
    ```

    ```# typescript
    type UserId = number
    ```
    """
    ts_base_type = map_newType_type(new_type, **extra)
    return f"type {new_type.__name__} = {ts_base_type};"  # type: ignore


def convert_typeVar_to_ts(new_type, **extra:'Extra') -> str:
    """
    将 Python 中的 TypeVar 转换为 TypeScript 的类型变量。
    #### 示例:
    ```# python
    T = TypeVar("T", bound=(int|str))  #  T = TypeVar("T", str, int)
    ```

    ```# typescript
    type T = number | string
    # T extends number | string
    ```
    """
    ts_base_type = map_typeVar_type(new_type, **extra)
    return f"type {new_type.__name__} = {ts_base_type};"


def convert_dataclass_to_ts(cls: type, **extra:'Extra') -> str:
    """
    将 Python 类转换为 TypeScript 的 interface 定义。
    """
    class_name = cls.__name__
    type_hints = get_type_hints(cls)
    fields = []
    for field, field_type in type_hints.items():
        # 通过检查 __origin__ 属性来检测 Final 和 ClassVar
        if get_origin(field_type) in [Final, ClassVar]:
            field_type = get_args(field_type)[0]  # 获取 Final 或 ClassVar 的原始类型
        ts_type = map_base_type(field_type, **extra)
        
        if field_type.__dict__.get('_name') == 'Optional':
            fields.append(f"{field}?: {ts_type};")
        else:
            fields.append(f"{field}: {ts_type};")

    fields_str = "\n  ".join(fields)
    return f"interface {class_name} {{\n  {fields_str}\n}}"


def convert_function_to_ts(func: Callable, **extra:'Extra') -> str:
    """
    将 Python 函数类型注解转换为 TypeScript 函数签名。
    """
    type_hints = get_type_hints(func)
    parameters = []
    for param, param_type in type_hints.items():
        if param != "return":
            ts_type = map_base_type(param_type, **extra)
            
            if param_type is Any:
                parameters.append(f"{param}: any")
            elif param_type.__dict__.get('_name') == 'Optional':
                parameters.append(f"{param}?: {ts_type}")
            else:
                parameters.append(f"{param}: {ts_type}")

    return_type = type_hints.get("return", None)
    ts_return_type = (
        map_base_type(return_type, **extra) if return_type is not None else "void"
    )

    params_str = ", ".join(parameters)
    return f"function {func.__name__}({params_str}): {ts_return_type};"




def process_newType(*stack: list[type], **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_NEWTYPE.keys()):
        STORE_PROCESSED_NEWTYPE[cur] = convert_newType_to_ts(cur, **processer)


def process_typeVar(*stack: list[type], **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_TYPEVAR.keys()):
        STORE_PROCESSED_TYPEVAR[cur] = convert_typeVar_to_ts(cur, **processer)


def process_typedDict(*stack: list[type], **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_TYPEDDICT.keys()):
        STORE_PROCESSED_TYPEDDICT[cur] = convert_typedDict_to_ts(cur, **processer)


def process_missing(*stack: list[type], **processer) -> str | None:
    cur = stack[-1]
    if exist_missing_type(cur):
        return cur.__name__

    if inspect.isclass(cur) and is_dataclass(cur):  # 处理 dataclass
        store_missing_type(cur,'dataclass',convert_dataclass_to_ts(cur, **processer))
        return cur.__name__

    if inspect.isfunction(cur):  # 处理函数
        store_missing_type(cur,'function',convert_function_to_ts(cur, **processer))
        return f"typeof {cur.__name__}"
    
    # 处理类方法
    if inspect.ismethod(cur):
        store_missing_type(cur,'method',convert_function_to_ts(cur, **processer))
        return f"typeof {cur.__name__}"
    
    # 处理插件
    for plugin in PLUGINS:
        if (mapped_type := plugin.map_type(cur)) is not None:
            # store_missing_type(cur,'map_type',mapped_type)
            return mapped_type
        if plugin.is_supported(cur):
            store_missing_type(cur,plugin.name,plugin.converter(cur, **processer))
            return cur.__name__
        
    return None










ProcessNewTypeFunc = Callable[[list[Any], 'Processers'], None]
ProcessTypeVarFunc = Callable[[list[Any], 'Processers'], None]
ProcessTypedDictFunc = Callable[[list[Any], 'Processers'], None]
ProcessMissingFunc = Callable[[list[Any], 'Processers'], str | None]

class Processers(TypedDict):
    """处理函数"""
    process_newType: ProcessNewTypeFunc
    process_typeVar: ProcessTypeVarFunc
    process_typedDict: ProcessTypedDictFunc
    process_missing: ProcessMissingFunc


class Extra(Processers):
    """额外参数"""
    __stack: list[Any]
