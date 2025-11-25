# pytots

一个轻量级的工具，帮助你将Python类型转换为TypeScript类型。

## 功能特性

- 支持基本Python类型到TypeScript类型的转换
- 支持高级类型（如Union、Optional等）
- 处理循环引用问题
- 支持自定义类型映射
- **支持 TypedDict 类型转换**
- **支持 dataclass 类型转换**
- **支持 Pydantic 模型转换**
- **支持 SQLModel 模型转换**

## 安装

使用uv安装：

```bash
uv add pytots
```

## 快速开始

```python
from py_ts import convert_to_typescript

# 基本类型转换
result = convert_to_typescript({
    'name': str,
    'age': int,
    'is_active': bool
})

print(result)
# 输出: interface GeneratedInterface {
#   name: string;
#   age: number;
#   is_active: boolean;
# }
```

## 示例

查看 `pytots/example/` 目录下的示例文件：

- `basic_types_example.py` - 基本类型转换示例
- `advanced_types_example.py` - 高级类型转换示例
- `circular_reference_example.py` - 循环引用处理示例
- `pydantic_example.py` - Pydantic 类型转换示例
- `sqlmodel_example.py` - SQLModel 类型转换示例

## Pydantic 支持

pytots 支持 Pydantic 模型的自动转换，包括：

- **BaseModel 类**：自动转换为 TypeScript 接口
- **Pydantic 字段类型**：EmailStr、HttpUrl、IPvAnyAddress 等
- **复杂嵌套模型**：支持模型间的嵌套关系
- **可选字段处理**：自动识别可选字段并添加 `?` 标记

示例：
```python
from pydantic import BaseModel, EmailStr
from pytots import convert_to_ts

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None

print(convert_to_ts(User))
# 输出: interface User {
#   id: number;
#   name: string;
#   email: string;
#   age?: number;
# }
```

## SQLModel 支持

pytots 支持 SQLModel 模型的自动转换，包括：

- **SQLModel 类**：基于 Pydantic 的数据库模型转换
- **数据库字段类型**：AutoString、BigInteger、Boolean 等
- **关系模型**：一对多、多对多关系支持
- **外键约束**：自动处理外键关系

示例：
```python
from sqlmodel import SQLModel, Field
from pytots import convert_to_ts

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)

print(convert_to_ts(User))
# 输出: interface User {
#   id?: number;
#   name: string;
#   email: string;
# }
```

## 开发

```bash
# 安装开发依赖
uv sync --group dev

# 运行测试
pytest
```

## 许可证

MIT License