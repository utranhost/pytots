"""pytots: A lightweight tool that helps you convert Python types to TypeScript types"""

__version__ = "0.3.0"

# 导入主要功能
from .main import (
    convert_to_ts,
    get_output_ts_str,
    output_ts_file,
    reset_store
)

from .plugin import Plugin, use_plugin

# 导出主要功能
__all__ = [
    "convert_to_ts",
    "get_output_ts_str", 
    "output_ts_file",
    "reset_store",
    "Plugin",
    "use_plugin",
]