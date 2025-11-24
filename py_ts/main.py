from dataclasses import is_dataclass
import inspect
from typing import (
    Any,
    Optional,
    get_type_hints,
    get_origin,
    get_args,
    Callable,
    Final,
    ClassVar,
)

from py_ts.type_map import (
    map_base_type,
    map_typedDict_type,
    map_newType_type,
    map_typeVar_type,
)


def convert_typedDict_to_ts(typed_dict, **extra) -> str:
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


def convert_newType_to_ts(new_type, **extra) -> str:
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
    return f"type {new_type.__name__} = {ts_base_type}"  # type: ignore


def convert_typeVar_to_ts(new_type, **extra) -> str:
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
    return f"type {new_type.__name__} = {ts_base_type}"


def convert_dataclass_to_ts(cls: type, **extra) -> str:
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


def convert_function_to_ts(func: Callable, **extra) -> str:
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
    return f"function {func.__name__}({params_str}): {ts_return_type}"


STORE_PROCESSED_NEWTYPE = {}
STORE_PROCESSED_TYPEVAR = {}
STORE_PROCESSED_TYPEDDICT = {}
STORE_PROCESSED_MISSING = {}


def process_newType(*stack: Any, **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_NEWTYPE.keys()):
        STORE_PROCESSED_NEWTYPE[cur] = convert_newType_to_ts(cur, **processer)


def process_typeVar(*stack: Any, **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_TYPEVAR.keys()):
        STORE_PROCESSED_TYPEVAR[cur] = convert_typeVar_to_ts(cur, **processer)


def process_typedDict(*stack: Any, **processer) -> None:
    cur = stack[-1]
    if all(cur != x for x in STORE_PROCESSED_TYPEDDICT.keys()):
        STORE_PROCESSED_TYPEDDICT[cur] = convert_typedDict_to_ts(cur, **processer)


def process_missing(*stack: Any, **processer) -> str | None:
    cur = stack[-1]
    if any(cur == x for x in STORE_PROCESSED_MISSING.keys()):
        return cur.__name__

    if inspect.isclass(cur) and is_dataclass(cur):  # 处理 dataclass
        STORE_PROCESSED_MISSING[cur] = convert_dataclass_to_ts(cur, **processer)
        return cur.__name__

    if inspect.isfunction(cur):  # 处理函数
        STORE_PROCESSED_MISSING[cur] = convert_function_to_ts(cur, **processer)
        return f"typeof {cur.__name__}"
    
    # 处理类方法
    if inspect.ismethod(cur):
        STORE_PROCESSED_MISSING[cur] = convert_function_to_ts(cur, **processer)
        return f"typeof {cur.__name__}"
    
    
    return None


# on_handle_final: Optional[Callable[[Any],None]] = None,
# on_handle_classVar: Optional[Callable[[Any],None]] = None,


def convert_to_ts(obj) -> str:
    """
    将 Python 对象转换为 TypeScript 定义。
    
    - `convert_to_ts` 可以自动识别引用的类型，并递归转换，确保所有类型都被正确处理。
    - `convert_to_ts`函数具有全局状态，每次调用会累积转换结果，如果需要重置状态，需调用`reset_store`函数
    """
    processer = {
        "process_newType": process_newType,
        "process_typeVar": process_typeVar,
        "process_typedDict": process_typedDict,
        "process_missing": process_missing,
    }
    return map_base_type(obj, **processer)



def get_output_ts_str(module_name: str|None = "PytsDemo") -> str:
    """
    将 Python 对象转换为 TypeScript 定义并返回字符串。
    Args:
        module_name: 模块名，默认值为 "PytsDemo", 当为 None 时，输出不添加模块声明。
    Returns:
        TypeScript 定义字符串
    """
    result = [
        *STORE_PROCESSED_NEWTYPE.values(),
        *STORE_PROCESSED_TYPEVAR.values(),
        *STORE_PROCESSED_TYPEDDICT.values(),
        *STORE_PROCESSED_MISSING.values(),
    ]
    if module_name is None or type(module_name) != str or not module_name.strip():
        return '\n  '.join(result)
    
    # 首字母大写
    module_name = module_name.capitalize()
    return "declare namespace {} {{\n  {}\n}}".format(module_name, '\n  '.join(result))


def output_ts_file(file_path: str,module_name: str|None = "PytsDemo") -> None:
    """
    将 Python 对象转换为 TypeScript 定义并输出到文件。
    Args:
        file_path: 输出文件路径
        module_name: 模块名，默认值为 "PytsDemo", 当为 None 时，输出不添加模块声明。
    """
    with open(file_path, "w", encoding="utf-8") as f:
        result = get_output_ts_str(module_name)
        f.write(result)




def reset_store() -> None:
    """
    清除所有已转换的 TypeScript 定义。
    """
    STORE_PROCESSED_NEWTYPE.clear()
    STORE_PROCESSED_TYPEVAR.clear()
    STORE_PROCESSED_TYPEDDICT.clear()
    STORE_PROCESSED_MISSING.clear()