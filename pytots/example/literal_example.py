"""
Literal 类型转换示例
"""

from typing import Literal
from pytots import convert_to_ts

# 定义各种 Literal 类型示例

# 1. 字符串字面量
StringLiteral = Literal["success", "error", "pending"]

# 2. 数字字面量
NumberLiteral = Literal[1, 2, 3, 100]

# 3. 布尔字面量
BooleanLiteral = Literal[True, False]

# 4. 混合字面量
MixedLiteral = Literal["red", 255, True, "blue"]

# 5. 单值字面量
SingleLiteral = Literal["admin"]

# 6. 单字符字面量
CharLiteral = Literal["a", "b", "c"]

# 7. 复杂嵌套类型中的 Literal
class UserStatus:
    status: Literal["active", "inactive", "banned"]
    role: Literal["admin", "user", "guest"]

# 8. 联合类型中的 Literal
UnionWithLiteral = Literal["yes", "no"] | str | int

# 9. 可选类型中的 Literal
OptionalLiteral = Literal["high", "medium", "low"] | None

# 10. 复杂嵌套
class Settings:
    theme: Literal["light", "dark", "auto"]
    language: Literal["zh", "en", "jp"]
    notifications: Literal["enabled", "disabled"]

if __name__ == "__main__":
    # 转换并输出 TypeScript 代码
    print("=== Literal 类型转换示例 ===\n")
    
    # 转换单个 Literal 类型
    print("1. 字符串字面量:")
    ts_code = convert_to_ts(StringLiteral)
    print(ts_code)
    print()
    
    print("2. 数字字面量:")
    ts_code = convert_to_ts(NumberLiteral)
    print(ts_code)
    print()
    
    print("3. 布尔字面量:")
    ts_code = convert_to_ts(BooleanLiteral)
    print(ts_code)
    print()
    
    print("4. 混合字面量:")
    ts_code = convert_to_ts(MixedLiteral)
    print(ts_code)
    print()
    
    print("5. 单值字面量:")
    ts_code = convert_to_ts(SingleLiteral)
    print(ts_code)
    print()
    
    print("6. 单字符字面量:")
    ts_code = convert_to_ts(CharLiteral)
    print(ts_code)
    print()
    
    print("7. 复杂类型中的 Literal:")
    ts_code = convert_to_ts(UserStatus)
    print(ts_code)
    print()
    
    print("8. 联合类型中的 Literal:")
    ts_code = convert_to_ts(UnionWithLiteral)
    print(ts_code)
    print()
    
    print("9. 可选类型中的 Literal:")
    ts_code = convert_to_ts(OptionalLiteral)
    print(ts_code)
    print()
    
    print("10. 复杂嵌套类型:")
    ts_code = convert_to_ts(Settings)
    print(ts_code)
    print()
    
    # 生成完整的 TypeScript 文件
    print("=== 生成完整的 TypeScript 文件 ===\n")
    
    # 定义要转换的类型列表
    types_to_convert = [
        StringLiteral,
        NumberLiteral,
        BooleanLiteral,
        MixedLiteral,
        SingleLiteral,
        CharLiteral,
        UserStatus,
        UnionWithLiteral,
        OptionalLiteral,
        Settings
    ]
    
    # 生成 TypeScript 文件
    ts_output = convert_to_ts(types_to_convert)
    
    print("\n文件内容预览:")
    print(ts_output)