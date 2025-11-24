"""
函数和类转换示例
展示py-ts对Python函数和类的TypeScript转换支持
"""

from typing import TypedDict, Callable, Optional, List, Dict, Any, Union
from dataclasses import dataclass, field
from py_ts import convert_to_ts, get_output_ts_str, output_ts_file, reset_store


@dataclass
class Team:
    """团队信息"""
    id: int
    name: str
    description: str
    employees: List['Employee'] = field(default_factory=list)
    
# r = convert_to_ts(Team)   # ❌ Employee is not defined

@dataclass
class Employee:
    """员工信息"""
    id: int
    name: str
    department: str
    salary: float
    manager: Optional['Employee']


convert_to_ts(Team)
res = get_output_ts_str(None)
print("类前置引用转换完成")
print(res)
reset_store()
    




print("\n=== 类的嵌套和自引用转换演示 ===")

# 嵌套数据类
class Address(TypedDict):
    """地址信息"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


# 自引用数据类
class Employee(TypedDict):
    """员工信息"""
    employee_id: int
    department: str
    salary: float
    address: Address
    skills: List[str]
    manager: Optional['Employee']


# 转换类
convert_to_ts(Employee)

res = get_output_ts_str(None)
print("类的嵌套和自引用转换完成")
print(res)
reset_store()




print("\n=== 回调模式转换演示 ===")

# 事件处理器类型
EventHandler = Callable[[Dict[str, Any]], None]

# 错误处理器
ErrorHandler = Callable[[Exception, Optional[str]], bool]

# 数据转换器
DataTransformer = Callable[[Any], Any]

# 验证器
Validator = Callable[[Any], bool]

# 带回调的函数
def event_emitter(
    event_name: str,
    data: Dict[str, Any],
    handlers: List[EventHandler]
) -> None:
    """事件发射器"""
    for handler in handlers:
        handler(data)

def data_pipeline(
    data: List[Any],
    transformers: List[DataTransformer],
    validator: Optional[Validator] = None
) -> List[Any]:
    """数据处理管道"""
    result = data
    for transformer in transformers:
        result = [transformer(item) for item in result]
    
    if validator:
        result = [item for item in result if validator(item)]
    
    return result

def error_boundary(
    operation: Callable[[], Any],
    on_error: ErrorHandler
) -> Any:
    """错误边界"""
    try:
        return operation()
    except Exception as e:
        if on_error(e, "Operation failed"):
            return None
        else:
            raise

# 转换回调模式
convert_to_ts(event_emitter)
convert_to_ts(data_pipeline)
convert_to_ts(error_boundary)

res = get_output_ts_str(None)
print("回调模式转换完成")
print(res)
reset_store()




print("\n=== 工具函数转换演示 ===")

# 工具函数集合

def deep_copy(obj: Any) -> Any:
    """深拷贝"""
    return obj

# 转换工具函数
convert_to_ts(deep_copy)


res = get_output_ts_str(None)
print("工具函数转换完成")
print(res)
reset_store()