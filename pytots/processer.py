"""
处理器和转换器函数
"""

import enum
import inspect
import typing
from typing import (
    Any,
    get_type_hints,
    get_origin,
    get_args,
    Callable,
    Final,
    ClassVar,
    TypedDict,
    NewType,
)
from dataclasses import is_dataclass
from pytots.type_map import (
    map_base_type,
    map_newType_type,
    map_typeVar_type,
    map_enum_type,
)
from pytots.plugin import PLUGINS
from pytots.store import (
    STORE_GENERIC_INTERFACE,
    STORE_PROCESSED_GENERIC,
    STORE_PROCESSED_TYPEVAR,
    STORE_PROCESSED_NEWTYPE,
    STORE_PROCESSED_ENUM,
    STORE_PROCESSED_MISSING,
    TEMP_CONTEXT,
)


def store_missing_type(type_, type_name, content: str):
    """
    存储缺失的类型映射
    """
    STORE_PROCESSED_MISSING[type_name] = STORE_PROCESSED_MISSING.get(type_name, {})
    STORE_PROCESSED_MISSING[type_name][type_] = content


def exist_missing_type(type_) -> bool:
    """
    检查是否存在缺失的类型映射
    """
    return any(
        type_ in STORE_PROCESSED_MISSING[type_name]
        for type_name in STORE_PROCESSED_MISSING.keys()
    )


def convert_newType_to_ts(new_type, **extra: "Extra") -> str:
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


def convert_typeVar_to_ts(new_type, **extra: "Extra") -> str:
    """
    将 Python 中的 TypeVar 转换为 TypeScript 的类型变量。
    #### 示例:
    ```# python
    T = TypeVar("T", bound=(int|str))  #  T = TypeVar("T", str, int)
    ```
    输出：
    ```# typescript
    T extends number | string
    # type T = number | string   (废弃)
    ```
    """
    ts_base_type = map_typeVar_type(new_type, **extra)
    return f"{new_type.__name__} extends {ts_base_type}"


# def convert_generic_to_ts(generic_type, **extra: "Extra") -> str:
#     """
#     将 Python 中的 Generic 类型转换为 TypeScript 的类型参数。
#     #### 示例:
#     ```# python
#     class QueryResult(Generic[T]):
#         data: Array[T]
#         total_count: number
#     ```
#     输出：
#     ```# typescript
#     interface QueryResult<T> {
#       data: Array<T>;
#       total_count: number;
#     }
#     ```
#     """
#     return map_generic_type(generic_type, **extra)


def convert_enum_to_ts(enum_type, **extra: "Extra") -> str:
    """
    将 Python 中的枚举类型转换为 TypeScript 的 enum 定义。
    #### 示例:
    ```# python
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    ```

    ```# typescript
    enum Color {
      RED = 1,
      GREEN = 2,
      BLUE = 3
    }
    """
    return map_enum_type(enum_type, **extra)



def convert_function_to_ts(func: Callable, **extra: "Extra") -> str:
    """
    将 Python 函数类型注解转换为 TypeScript 函数签名。
    """
    type_hints = get_type_hints(func)
    parameters = []
    for param, param_type in type_hints.items():
        if param != "return":
            param_result = map_base_type(param_type, **extra)
            ts_type = param_result["code"] if isinstance(param_result, dict) and "code" in param_result else param_result

            if param_type is Any:
                parameters.append(f"{param}: any")
            elif param_type.__dict__.get("_name") == "Optional":
                parameters.append(f"{param}?: {ts_type}")
            else:
                parameters.append(f"{param}: {ts_type}")

    return_type = type_hints.get("return", None)
    if return_type is not None:
        return_result = map_base_type(return_type, **extra)
        ts_return_type = return_result["code"] if isinstance(return_result, dict) and "code" in return_result else return_result
    else:
        ts_return_type = "void"

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
        return cur.__name__
    else:
        if n:=TEMP_CONTEXT['typevar'].get(cur):
            return n
        return cur.__name__


def process_enum(*stack: list[type], **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_ENUM.keys()):
        STORE_PROCESSED_ENUM[cur] = convert_enum_to_ts(cur, **processer)


def process_missing(*stack: list[type], **processer) -> str | None:
    cur = stack[-1]
    if exist_missing_type(cur):
        return cur.__name__

    # 处理枚举类型

    if inspect.isclass(cur) and issubclass(cur, enum.Enum):
        store_missing_type(cur, "enum", convert_enum_to_ts(cur, **processer))
        return cur.__name__

    if inspect.isfunction(cur):  # 处理函数
        store_missing_type(cur, "function", convert_function_to_ts(cur, **processer))
        return f"typeof {cur.__name__}"

    # 处理类方法
    if inspect.ismethod(cur):
        store_missing_type(cur, "method", convert_function_to_ts(cur, **processer))
        return f"typeof {cur.__name__}"
    


    class_generic_params = {
        "names": [],
        "define_codes": [],
    }
    
    class_extends_params = []

    extra = {**processer, "__stack": list(stack)}
 
    def handle_generic_instance(cur):
        # 处理GenericType实例（如QueryResult[TicketType]） ===> QueryResult<TicketType>
        origin_result = map_base_type(cur.__origin__, **extra)
        res = origin_result["code"]
        args = []
        for arg in get_args(cur):
            arg_result = map_base_type(arg, **extra)
            args.append(arg_result["code"])
        define_code = f"{res}<{', '.join(args)}>"
        return define_code,args


    if type(cur) == typing._GenericAlias and get_origin(cur) != typing.Generic:
        define_code,args = handle_generic_instance(cur)
        origin = get_origin(cur)
        type_vars = [x.__parameters__ for x in origin.__orig_bases__ if hasattr(x, '__parameters__')]
        # 展平type_vars
        type_vars = [item for sublist in type_vars for item in sublist]
        STORE_GENERIC_INTERFACE[define_code] = {k: v for k, v in zip(type_vars, args)}
        return define_code
        
    if inspect.isclass(cur) and issubclass(cur, typing.Generic):
        # print(cur.__name__,'他是一个泛型类')
        if hasattr(cur, "__parameters__") and bool(cur.__parameters__):
            # 处理有参泛型类
            # print(cur.__name__,'他有类型参数')
            names_list = []
            for r in cur.__parameters__:
                r_result = map_base_type(r, **extra)
                names_list.append(r_result["code"])
            class_generic_params["names"] = names_list
            class_generic_params["define_codes"] = [
                STORE_PROCESSED_TYPEVAR[r] for r in cur.__parameters__
            ]

        else:
            # 无参泛型类
            # print(cur.__name__,'无参泛型类')
            # if hasattr(cur, "__orig_bases__"):
            #     print('他有orig_bases: ',cur.__orig_bases__)
            
            # origin = get_origin(cur)
            # print('他的origin: ',origin)
            # print('他的args: ',args)
            
            if hasattr(cur, '__origin__'):  
                # 处理GenericType实例（如QueryResult[TicketType]） ===> QueryResult<TicketType>
                define_code,args = handle_generic_instance(cur)
                type_vars = [x.__parameters__ for x in cur.__orig_bases__ if hasattr(x, '__parameters__')]
                # 展平type_vars
                type_vars = [item for sublist in type_vars for item in sublist]
                STORE_GENERIC_INTERFACE[define_code] = {k: v for k, v in zip(type_vars, args)}
                return define_code
            else:
                # 处理泛型类继承
                if cur.__orig_bases__:
                    # o = map_base_type(cur, **extra)

                    class_extends_params = []
                    for arg in cur.__orig_bases__:
                        arg_result = map_base_type(arg, **extra)
                        class_extends_params.append(arg_result["code"] if isinstance(arg_result, dict) and "code" in arg_result else arg_result)
                    STORE_PROCESSED_TYPEVAR
                    STORE_PROCESSED_GENERIC
                    # return o + f"<{', '.join(a)}>"
                else:
                    result = map_base_type(cur, **extra)
                    return result["code"] if isinstance(result, dict) and "code" in result else result
        

    # 处理插件
    for plugin in PLUGINS:
        plugin.class_generic_params = class_generic_params    # 为插件注入泛型类参数
        plugin.class_extends_params = class_extends_params    # 为插件注入继承类参数
        if (mapped_type := plugin.map_type(cur)) is not None:
            # store_missing_type(cur,'map_type',mapped_type)
            return mapped_type
        if plugin.is_supported(cur):
            store_missing_type(cur, plugin.name, plugin.converter(cur, **processer))
            return cur.__name__



        
    return None


ProcessNewTypeFunc = Callable[[list[Any], "Processers"], None]
ProcessTypeVarFunc = Callable[[list[Any], "Processers"], None]
ProcessTypedDictFunc = Callable[[list[Any], "Processers"], None]
ProcessEnumFunc = Callable[[list[Any], "Processers"], None]
ProcessMissingFunc = Callable[[list[Any], "Processers"], str | None]


class Processers(TypedDict):
    """处理函数"""

    process_newType: ProcessNewTypeFunc
    process_typeVar: ProcessTypeVarFunc
    process_typedDict: ProcessTypedDictFunc
    process_enum: ProcessEnumFunc
    process_missing: ProcessMissingFunc


class Extra(Processers):
    """额外参数"""

    __stack: list[Any]
