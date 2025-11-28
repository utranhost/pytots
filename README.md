# pytots - Python到TypeScript类型转换工具

[![GitHub stars](https://img.shields.io/github/stars/utranhost/pytots?style=for-the-badge)](https://github.com/utranhost/pytots)
[![GitHub forks](https://img.shields.io/github/forks/utranhost/pytots?style=for-the-badge)](https://github.com/utranhost/pytots)
[![GitHub issues](https://img.shields.io/github/issues/utranhost/pytots?style=for-the-badge)](https://github.com/utranhost/pytots/issues)
[![GitHub license](https://img.shields.io/github/license/utranhost/pytots?style=for-the-badge)](https://github.com/utranhost/pytots/blob/main/LICENSE)

**pytots** 是一个轻量级但功能强大的工具，专门用于将Python类型定义自动转换为TypeScript类型定义。无论您是构建全栈应用、API接口还是需要前后端类型同步，pytots都能帮助您保持类型一致性，提高开发效率。

## ✨ 核心特性

### 🔄 智能类型转换
- **基础类型映射**: `str` → `string`, `int/float` → `number`, `bool` → `boolean`
- **容器类型支持**: `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[...]`
- **高级类型处理**: `Union`, `Optional`, `Literal`, `TypedDict`
- **枚举类型支持**: Python `enum.Enum` → TypeScript `enum`
- **自定义类型**: `NewType`, `TypeVar`, 用户定义类

### 🧩 插件生态系统
- **Pydantic集成**: 自动转换Pydantic BaseModel为TypeScript接口
- **SQLModel支持**: 数据库模型无缝转换为前端类型
- **可扩展架构**: 轻松添加对新类型系统的支持

### 🔧 开发者友好
- **循环引用检测**: 自动识别并处理类型间的循环依赖
- **多种输出格式**: 支持字符串输出和文件直接写入
- **代码格式化**: 生成整洁、可读的TypeScript代码

## 🚀 快速开始

### 安装
```bash
# 使用uv（推荐）
uv add pytots

# 或使用pip
pip install pytots
```

### 基本使用
```python
from pytots import convert_to_ts, get_output_ts_str, output_ts_file
from typing import List, Dict, Optional
import enum

# 转换Python类型为TypeScript
print("=== 基础类型转换演示 ===")

# 基本类型
print(f"str -> {convert_to_ts(str)}")        # string
print(f"int -> {convert_to_ts(int)}")        # number
print(f"bool -> {convert_to_ts(bool)}")      # boolean

# 容器类型
print(f"List[int] -> {convert_to_ts(List[int])}")          # Array<number>
print(f"Dict[str, int] -> {convert_to_ts(Dict[str, int])}") # Record<string, number>
print(f"Optional[str] -> {convert_to_ts(Optional[str])}")   # string | null | undefined

# 集合类型（新增支持）
print(f"Set[int] -> {convert_to_ts(Set[int])}")            # Set<number>
print(f"FrozenSet[str] -> {convert_to_ts(FrozenSet[str])}") # ReadonlySet<string>
print(f"tuple[int, str] -> {convert_to_ts(tuple[int, str])}") # [number, string]
print(f"tuple[int, ...] -> {convert_to_ts(tuple[int, ...])}") # number[]

# collections模块类型
from collections import deque, Counter, ChainMap
print(f"deque[str] -> {convert_to_ts(deque[str])}")          # Array<string>
print(f"Counter[str] -> {convert_to_ts(Counter[str])}")      # Record<string, number>
print(f"ChainMap[str, int] -> {convert_to_ts(ChainMap[str, int])}") # Record<string, number>

# 新增基础类型
import decimal
import uuid
print(f"bytes -> {convert_to_ts(bytes)}")                    # Uint8Array
print(f"object -> {convert_to_ts(object)}")                  # any
print(f"decimal.Decimal -> {convert_to_ts(decimal.Decimal)}") # number
print(f"uuid.UUID -> {convert_to_ts(uuid.UUID)}")           # string
print(f"complex -> {convert_to_ts(complex)}")               # {real: number, imag: number}
print(f"range -> {convert_to_ts(range)}")                   # {start: number, stop: number, step: number}

# 枚举类型
class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Status(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

print(f"Color enum -> {convert_to_ts(Color)}")  # enum Color { RED = 1, GREEN = 2, BLUE = 3 }
print(f"Status enum -> {convert_to_ts(Status)}") # enum Status { PENDING = 'pending', ... }

# 获取完整的TypeScript代码字符串
ts_code = get_output_ts_str()
print(ts_code)

# 直接输出到文件
output_ts_file("output/types.ts")
```

### 自定义类型映射

pytots 提供了 `replaceable_type_map` 函数，允许您自定义特定类型的映射规则。这对于需要特殊处理或自定义类型转换的场景非常有用。

```python
from pytots import convert_to_ts, replaceable_type_map
import datetime

print("=== 自定义类型映射演示 ===")

# 默认情况下，datetime.date 会被转换为 "Date"
print(f"默认 datetime.date -> {convert_to_ts(datetime.date)}")  # Date

# 使用 replaceable_type_map 自定义映射规则
# 将 datetime.date 映射为自定义的字符串类型
result = replaceable_type_map(datetime.date, "string")
print(f"自定义datetime.date映射结果: {result}")  # True

# 现在 datetime.date 会被转换为 "string"
print(f"自定义后的 datetime.date -> {convert_to_ts(datetime.date)}")  # string

# 将 None 类型映射为更简洁的 "undefined"
replaceable_type_map(None, "undefined")
print(f"自定义后的 None -> {convert_to_ts(None)}")  # undefined

# 将 datetime.datetime 映射为更精确的时间戳类型
replaceable_type_map(datetime.datetime, "number")
print(f"自定义后的 datetime.datetime -> {convert_to_ts(datetime.datetime)}")  # number

# 尝试映射不支持的类型的示例
class CustomType:
    pass

result = replaceable_type_map(CustomType, "any")
print(f"尝试映射自定义类型: {result}")  # False，因为CustomType不在可替换类型列表中
```

**可替换类型列表**：
- `datetime.date`
- `datetime.datetime` 
- `None`

**使用场景**：
- 当您需要将日期类型映射为不同的TypeScript类型时
- 当您想要简化 `None` 类型的映射时
- 当您需要与现有TypeScript代码库保持类型一致性时

### Pydantic模型转换
```python
from pytots.plugin.plus import PydanticPlugin
from pytots import use_plugin, convert_to_ts
from pydantic import BaseModel

# 启用Pydantic插件
use_plugin(PydanticPlugin())

class User(BaseModel):
    id: int
    name: str
    email: str

# 自动转换为TypeScript接口
convert_to_ts(User)
```

## 📊 支持的类型系统

| Python类型 | TypeScript类型 | 示例 |
|-----------|---------------|------|
| `str` | `string` | `name: string` |
| `int`, `float` | `number` | `age: number` |
| `bool` | `boolean` | `is_active: boolean` |
| `bytes` | `Uint8Array` | `data: Uint8Array` |
| `bytearray` | `Uint8Array` | `buffer: Uint8Array` |
| `complex` | `{real: number, imag: number}` | `value: {real: number, imag: number}` |
| `range` | `{start: number, stop: number, step: number}` | `range: {start: number, stop: number, step: number}` |
| `type(None)` | `null \| undefined` | `value: null \| undefined` |
| `object` | `any` | `obj: any` |
| `decimal.Decimal` | `number` | `price: number` |
| `uuid.UUID` | `string` | `id: string` |
| `List[T]` | `Array<T>` | `tags: Array<string>` |
| `Dict[K, V]` | `Record<K, V>` | `data: Record<string, number>` |
| `Set[T]` | `Set<T>` | `unique_ids: Set<number>` |
| `FrozenSet[T]` | `ReadonlySet<T>` | `constants: ReadonlySet<string>` |
| `tuple[T]` | `[T]` | `coordinates: [number]` |
| `tuple[T1, T2]` | `[T1, T2]` | `point: [number, number]` |
| `tuple[T, ...]` | `T[]` | `items: number[]` |
| `deque[T]` | `Array<T>` | `queue: Array<string>` |
| `Counter[T]` | `Record<T, number>` | `word_count: Record<string, number>` |
| `ChainMap[K, V]` | `Record<K, V>` | `config: Record<string, any>` |
| `Optional[T]` | `T \| null \| undefined` | `email?: string \| null \| undefined` |
| `Union[T, U]` | `T \| U` | `status: 'active' \| 'inactive'` |
| `enum.Enum` | `enum` | `enum Color { RED = 1, GREEN = 2, BLUE = 3 }` |

## 🎯 使用场景

### 全栈开发
保持前后端类型定义同步，减少手动维护成本

### API文档生成
自动从Python模型生成TypeScript客户端类型

### 微服务架构
在多个服务间共享类型定义，确保接口一致性

### 数据库模型同步
将SQLModel/Pydantic模型转换为前端可用的类型

## 🔗 相关链接

- 📖 **文档**: [查看完整文档](https://github.com/utranhost/pytots#readme)
- 🐛 **问题反馈**: [提交Issue](https://github.com/utranhost/pytots/issues)
- 💡 **功能建议**: [参与讨论](https://github.com/utranhost/pytots/discussions)
- ⭐ **支持项目**: 如果这个工具对您有帮助，请给个Star！

## 🤝 贡献

我们欢迎各种形式的贡献！无论是代码改进、文档完善还是功能建议，都可以通过以下方式参与：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！特别感谢：

- Pydantic 团队提供的优秀类型系统
- TypeScript 社区的灵感
- 所有使用和反馈这个项目的开发者

---

**开始使用 pytots，让您的类型定义工作变得更加高效和愉快！** 🎉

---

## 功能特性

- **支持基本Python类型到TypeScript类型的转换**
- **支持高级类型转换**：Union、Optional、Literal等
- **处理循环引用问题**：自动检测并处理类型间的循环依赖
- **增强的泛型支持**：支持复杂的泛型类、泛型接口和参数替换机制
- **统一的类型映射**：改进的类型映射系统，提供更丰富的类型信息和处理能力
- **支持自定义类型映射**：可扩展的类型映射系统
- **插件系统**：支持通过插件扩展功能
- **多种输出格式**：支持字符串输出和文件输出

### 支持的具体类型

- **基本类型**：`str`, `int`, `float`, `bool`, `None`, `Any`, `object`
- **容器类型**：`List`, `Dict`, `Set`, `FrozenSet`, `Tuple`, `deque`, `Counter`, `ChainMap`, `Union`, `Optional`
- **自定义类型**：`NewType`, `TypeVar`
- **类类型**：`dataclass` 类转换
- **函数类型**：函数签名转换
- **泛型类型**：增强的泛型类和泛型接口支持
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
from typing import List, Dict, Optional

# 基本类型转换
print("=== 基础类型转换演示 ===")

# 基本类型
print(f"str -> {convert_to_ts(str)}")        # string
print(f"int -> {convert_to_ts(int)}")        # number
print(f"bool -> {convert_to_ts(bool)}")      # boolean

# 容器类型
print(f"List[int] -> {convert_to_ts(List[int])}")          # Array<number>
print(f"Dict[str, int] -> {convert_to_ts(Dict[str, int])}") # Record<string, number>
print(f"Optional[str] -> {convert_to_ts(Optional[str])}")   # string | null | undefined

# 获取完整的TypeScript代码字符串
ts_code = get_output_ts_str()
print(ts_code)

# 直接输出到文件
output_ts_file("output/types.ts")
```

### 支持的类型示例

```python
from typing import NewType, TypeVar, Optional, List, Generic
from dataclasses import dataclass
from pytots import convert_to_ts, get_output_ts_str

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

# 泛型类转换
class QueryResult(Generic[T]):
    data: List[T]
    total_count: int

# 函数类型转换
def process_user(user: User) -> bool:
    return True

# 转换所有类型
convert_to_ts(UserId)
convert_to_ts(T)
convert_to_ts(User)
convert_to_ts(QueryResult[User])
convert_to_ts(process_user)

# 获取完整的TypeScript定义
ts_code = get_output_ts_str()
print(ts_code)
```

## 插件系统

pytots 提供了插件系统，可以扩展支持更多类型系统。插件系统现在支持通过 `generic_feild_fill` 函数实现高级泛型类型处理。

### Pydantic 支持

```python
from pytots.plugin.plus.pydantic_plugin import PydanticPlugin
from pytots import use_plugin, convert_to_ts, get_output_ts_str
from pydantic import BaseModel, EmailStr, Generic as PydanticGeneric

# 启用Pydantic插件
use_plugin(PydanticPlugin())

# 基本模型转换
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None

# 泛型模型转换
class ResponseModel(PydanticGeneric[T]):
    data: T
    success: bool

# 转换Pydantic模型
convert_to_ts(User)
convert_to_ts(ResponseModel[User])
ts_code = get_output_ts_str()
print(ts_code)
```

### SQLModel 支持

```python
from pytots.plugin.plus.sqlmodel_plugin import SqlModelPlugin
from pytots import use_plugin, convert_to_ts, get_output_ts_str
from sqlmodel import SQLModel, Field
from typing import Generic, TypeVar

# 启用SQLModel插件
use_plugin(SqlModelPlugin())

# 基本模型转换
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)

# 泛型响应模型
class PaginatedResponse(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

# 转换SQLModel和泛型模型
convert_to_ts(User)
convert_to_ts(PaginatedResponse[User])
ts_code = get_output_ts_str()
print(ts_code)
```

## API 参考

### 主要函数

- `convert_to_ts(obj) -> str`：转换单个Python类型为TypeScript定义
- `get_output_ts_str(module_name: str | None = "PytsDemo", format: bool = False) -> str`：获取完整的TypeScript代码字符串
- `output_ts_file(file_path: str, module_name: str | None = "PytsDemo", format: bool = True) -> None`：输出TypeScript代码到文件
- `reset_store() -> None`：清除所有已转换的类型定义缓存

### 类型映射配置

- `replaceable_type_map(type_, value) -> bool`：自定义可替换类型的映射规则

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
- `replaceable_type_map_example.py` - 自定义类型映射示例

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
├── type_map.py          # 类型映射系统（增强的泛型支持）
├── processer.py         # 类型处理器（改进的泛型接口处理）
├── formart.py           # 代码格式化
├── store.py             # 存储机制（新增泛型接口存储）
└── plugin/              # 插件系统
    ├── __init__.py
    ├── tools.py         # 插件工具（包含generic_feild_fill函数）
    └── plus/            # 扩展插件
        ├── pydantic_plugin.py
        └── sqlmodel_plugin.py
```

## 许可证

MIT License