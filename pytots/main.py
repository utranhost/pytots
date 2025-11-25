
from pytots.type_map import map_base_type
from pytots.processer import (
    process_newType,
    process_typeVar,
    process_typedDict,
    process_missing,
    STORE_PROCESSED_NEWTYPE,
    STORE_PROCESSED_TYPEVAR,
    STORE_PROCESSED_TYPEDDICT,
    STORE_PROCESSED_MISSING,
)



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