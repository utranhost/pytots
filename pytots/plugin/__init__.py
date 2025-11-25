"""插件模块"""
from typing import Any
from abc import ABC, abstractmethod

class Plugin(ABC):
    """插件基类"""
    
    # 插件名称
    name: str = "pytots-plugin"
    
    # 类型前缀
    type_prefix: str = "interface"
    
    
    # 类型映射表
    TYPES_MAP: dict[type|str, str] = {}
    
    
    @abstractmethod
    def converter(self, python_type: Any, **extra) -> str:
        """转换类型"""
        ...

    @abstractmethod
    def is_supported(self, python_type: Any) -> bool:
        """检查是否支持该类型"""
        ...

    def map_type(self, python_type: Any) -> str|None:
        """检查是否为映射类型"""
        return self.TYPES_MAP.get(python_type, None)



PLUGINS: list[Plugin] = []  # 插件列表


def use_plugin(plugin: Plugin):
    """注册插件"""
    if not isinstance(plugin, Plugin):
        raise TypeError(f"非法插件 {plugin.__class__.__name__}, 必须继承自Plugin类")
    
    PLUGINS.append(plugin)
    print(f"插件 {plugin.__class__.__name__} 已注册")
