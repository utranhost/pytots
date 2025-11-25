# pytots

一个轻量级的工具，帮助你将Python类型转换为TypeScript类型。

## 功能特性

- **支持基本Python类型到TypeScript类型的转换**
- **支持高级类型转换**：Union、Optional、Literal等
- **处理循环引用问题**：自动检测并处理类型间的循环依赖
- **支持自定义类型映射**：可扩展的类型映射系统
- **插件系统**：支持通过插件扩展功能
- **多种输出格式**：支持字符串输出和文件输出

### 支持的具体类型

- **基本类型**：`str`, `int`, `float`, `bool`, `None`, `Any`, `object`
- **容器类型**：`List`, `Dict`, `Set`, `Tuple`, `Union`, `Optional`
- **自定义类型**：`NewType`, `TypeVar`, `TypedDict`
- **类类型**：`dataclass` 类转换
- **函数类型**：函数签名转换
- **插件支持**：Pydantic BaseModel、SQLModel

## 安装

使用uv安装：

```bash
uv add pytots
```

或者使用pip：

```bash
pip install pytots
```

## 快速开始

### 基本使用

```python
from pytots import convert_to_ts, get_output_ts_str, output_ts_file

# 基本类型转换
result = convert_to_ts({
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

# 获取完整的TypeScript代码字符串
ts_code = get_output_ts_str("MyModule")
print(ts_code)

# 直接输出到文件
output_ts_file("output/types.ts", "MyModule")
```

### 支持的类型示例

```python
from typing import TypedDict, NewType, TypeVar, Optional, List
from dataclasses import dataclass

# TypedDict 转换
class UserDict(TypedDict):
    name: str
    age: int

# NewType 转换
UserId = NewType("UserId", int)

# TypeVar 转换
T = TypeVar("T", int, str)

# dataclass 转换
@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None

# 函数类型转换
def process_user(user: UserDict) -> bool:
    return True

# 转换所有类型
convert_to_ts(UserDict)
convert_to_ts(UserId)
convert_to_ts(T)
convert_to_ts(User)
convert_to_ts(process_user)

# 获取完整的TypeScript定义
ts_code = get_output_ts_str("UserModule")
print(ts_code)
```

## 插件系统

pytots 提供了插件系统，可以扩展支持更多类型系统。

### Pydantic 支持

```python
from pytots.plugin.plus import PydanticPlugin
from pytots import use_plugin
from pydantic import BaseModel, EmailStr

# 启用Pydantic插件
use_plugin(PydanticPlugin())

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None

# 转换Pydantic模型
convert_to_ts(User)
ts_code = get_output_ts_str("PydanticModule")
print(ts_code)
```

### SQLModel 支持

```python
from pytots.plugin.plus import SqlModelPlugin
from pytots import use_plugin
from sqlmodel import SQLModel, Field

# 启用SQLModel插件
use_plugin(SqlModelPlugin())

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)

# 转换SQLModel模型
convert_to_ts(User)
ts_code = get_output_ts_str("SQLModelModule")
print(ts_code)
```

## API 参考

### 主要函数

- `convert_to_ts(obj) -> str`：转换单个Python类型为TypeScript定义
- `get_output_ts_str(module_name: str | None = "PytsDemo", format: bool = False) -> str`：获取完整的TypeScript代码字符串
- `output_ts_file(file_path: str, module_name: str | None = "PytsDemo", format: bool = True) -> None`：输出TypeScript代码到文件
- `reset_store() -> None`：清除所有已转换的类型定义缓存

### 插件相关

- `Plugin`：插件基类
- `use_plugin(plugin: Plugin) -> None`：启用插件

## 示例

查看 `pytots/example/` 目录下的示例文件：

- `basic_types_example.py` - 基本类型转换示例
- `advanced_types_example.py` - 高级类型转换示例
- `circular_reference_example.py` - 循环引用处理示例
- `pydantic_example.py` - Pydantic 类型转换示例
- `sqlmodel_example.py` - SQLModel 类型转换示例

## 开发

### 安装开发依赖

```bash
uv sync --group dev
```

### 运行测试

```bash
pytest
```

### 项目结构

```
pytots/
├── __init__.py          # 主模块导出
├── main.py              # 主要功能函数
├── type_map.py          # 类型映射系统
├── processer.py         # 类型处理器
├── formart.py           # 代码格式化
└── plugin/              # 插件系统
    ├── __init__.py
    └── plus/            # 扩展插件
        ├── pydantic_plugin.py
        └── sqlmodel_plugin.py
```

## 许可证

MIT License