"""插件模块"""

from typing import Any,TypedDict
from abc import ABC, abstractmethod

class ClassGenericParams(TypedDict):
    """类泛型参数"""
    names: list[str]
    define_codes: list[str]


class Plugin(ABC):
    """插件基类"""

    # 插件名称
    name: str = "pytots-plugin"

    # 类型前缀
    type_prefix: str = "interface"

    # 类型映射表
    TYPES_MAP: dict[type | str, str] = {}
    
    
    # 如果是泛型类且有类型参数，系统将自动处理并填充
    class_generic_params: ClassGenericParams = {}


    @abstractmethod
    def converter(self, python_type: Any, **extra) -> str:
        """转换类型"""
        ...

    @abstractmethod
    def is_supported(self, python_type: Any) -> bool:
        """检查是否支持该类型"""
        ...

    def map_type(self, python_type: Any) -> str | None:
        """检查是否为映射类型"""
        return self.TYPES_MAP.get(python_type, None)


PLUGINS: list[Plugin] = []  # 插件列表


def use_plugin(*plugins: Plugin):
    """注册插件"""

    for plugin in plugins:
        if not isinstance(plugin, Plugin):
            raise TypeError(f"非法插件 {plugin.__class__.__name__}, 必须继承自Plugin类的实例")

        PLUGINS.append(plugin)
        print(f"插件 {plugin.__class__.__name__} 已注册")


def override_plugin(*plugins: Plugin):
    """
    ### 覆盖已有的插件
    替换时以插件名作为唯一标识
    """
    for plugin in plugins:
        if not isinstance(plugin, Plugin):
            raise TypeError(f"非法插件 {plugin.__class__.__name__}, 必须继承自Plugin类")

        # 从PLUGINS实例中替换掉相同name的插件
        for i, p in enumerate(PLUGINS):
            if p.name == plugin.name:
                PLUGINS[i] = plugin
                break
        else:
            print(f"覆盖失败,未找到插件 {plugin.__class__.__name__}")

        print(f"插件 {plugin.name} 已覆盖")

