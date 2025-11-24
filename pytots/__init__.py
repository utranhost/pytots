"""pytots: A lightweight tool that helps you convert Python types to TypeScript types"""

__version__ = "0.2.0"

# 导入主要功能
from .main import (
    convert_to_ts,
    get_output_ts_str,
    output_ts_file,
    convert_typedDict_to_ts,
    convert_newType_to_ts,
    convert_typeVar_to_ts,
    convert_dataclass_to_ts,
    convert_function_to_ts,
    reset_store
)

# 导出主要功能
__all__ = [
    "convert_to_ts",
    "get_output_ts_str", 
    "output_ts_file",
    "convert_typedDict_to_ts",
    "convert_newType_to_ts",
    "convert_typeVar_to_ts",
    "convert_dataclass_to_ts",
    "convert_function_to_ts",
    "reset_store"
]