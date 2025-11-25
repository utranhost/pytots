"""
调试 Literal 类型转换
"""

from typing import Literal
from pytots import convert_to_ts

# 测试单个 Literal 类型
print("=== 调试 Literal 类型转换 ===\n")

# 1. 字符串字面量
StringLiteral = Literal["success", "error", "pending"]
print("1. 字符串字面量:")
print(f"类型: {type(StringLiteral)}")
print(f"参数: {StringLiteral.__args__}")
print(f"转换结果: {convert_to_ts(StringLiteral)}")
print()

# 2. 数字字面量
NumberLiteral = Literal[1, 2, 3, 100]
print("2. 数字字面量:")
print(f"类型: {type(NumberLiteral)}")
print(f"参数: {NumberLiteral.__args__}")
print(f"转换结果: {convert_to_ts(NumberLiteral)}")
print()

# 3. 布尔字面量
BooleanLiteral = Literal[True, False]
print("3. 布尔字面量:")
print(f"类型: {type(BooleanLiteral)}")
print(f"参数: {BooleanLiteral.__args__}")
print(f"转换结果: {convert_to_ts(BooleanLiteral)}")
print()

# 4. 混合字面量
MixedLiteral = Literal["red", 255, True, "blue"]
print("4. 混合字面量:")
print(f"类型: {type(MixedLiteral)}")
print(f"参数: {MixedLiteral.__args__}")
print(f"转换结果: {convert_to_ts(MixedLiteral)}")
print()