"""
枚举类型转换示例

演示如何使用 pytots 将 Python 枚举类型转换为 TypeScript 枚举定义。
"""
import os
from enum import Enum, IntEnum
from typing import Optional
from pytots import convert_to_ts, get_output_ts_str, output_ts_file, reset_store

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'test_ts_output')
class Color(Enum):
    """基础枚举类型示例"""
    RED = 1
    GREEN = 2
    BLUE = 3


class Priority(IntEnum):
    """整数枚举类型示例"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Status(Enum):
    """字符串枚举类型示例"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class Direction(Enum):
    """混合值枚举类型示例"""
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    CENTER = 0


# 使用枚举类型的复杂类型示例
class User:
    """用户类，包含枚举类型字段"""
    def __init__(self, name: str, status: Status, priority: Priority):
        self.name = name
        self.status = status
        self.priority = priority


def enum_types_demo():
    """枚举类型转换演示"""
    print("=== 枚举类型转换演示 ===")
    
    # 转换单个枚举类型
    print("\n1. 基础枚举类型转换:")
    convert_to_ts(Color)
    print(get_output_ts_str())
    
    reset_store()
    
    print("\n2. 整数枚举类型转换:")
    convert_to_ts(Priority)
    print(get_output_ts_str())
    
    reset_store()
    
    print("\n3. 字符串枚举类型转换:")
    convert_to_ts(Status)
    print(get_output_ts_str())
    
    reset_store()
    
    print("\n4. 混合值枚举类型转换:")
    convert_to_ts(Direction)
    print(get_output_ts_str())


def complex_enum_demo():
    """复杂枚举类型使用演示"""
    print("\n=== 复杂枚举类型使用演示 ===")
    
    reset_store()
    
    # 转换包含枚举的复杂类型
    convert_to_ts(User)
    convert_to_ts(Status)
    convert_to_ts(Priority)
    
    ts_code = get_output_ts_str()
    print(ts_code)


def generate_enum_ts_file():
    """生成枚举类型的TypeScript文件"""
    print("\n=== 生成枚举类型TypeScript文件 ===")
    
    reset_store()
    
    # 转换所有枚举类型
    convert_to_ts(Color)
    convert_to_ts(Priority)
    convert_to_ts(Status)
    convert_to_ts(Direction)
    convert_to_ts(User)
    
    # 输出到文件
    output_ts_file(os.path.join(output_dir, "enum_types.ts"), "EnumTypes")
    print(f"枚举类型文件已生成: {os.path.join(output_dir, 'enum_types.ts')}")


if __name__ == "__main__":
    # 运行演示
    enum_types_demo()
    complex_enum_demo()
    generate_enum_ts_file()