<p align="center">
  <a href="https://github.com/utranhost/pytots">
    <img src="https://img.shields.io/github/stars/utranhost/pytots?style=for-the-badge&labelColor=232323&color=ffcb47" alt="GitHub Stars"/>
  </a>
  <a href="https://github.com/utranhost/pytots">
    <img src="https://img.shields.io/github/forks/utranhost/pytots?style=for-the-badge&labelColor=232323&color=4ecdc4" alt="GitHub Forks"/>
  </a>
  <a href="https://github.com/utranhost/pytots/issues">
    <img src="https://img.shields.io/github/issues/utranhost/pytots?style=for-the-badge&labelColor=232323&color=ff6b6b" alt="GitHub Issues"/>
  </a>
  <a href="https://github.com/utranhost/pytots/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/utranhost/pytots?style=for-the-badge&labelColor=232323&color=6a994e" alt="GitHub License"/>
  </a>
</p>


# 🐍➡️🚀 pytots

一个轻量级工具，帮助你将 **Python 类型** 优雅地转换为 **TypeScript 类型**。


---

## ✨ 特性

- 🔧 **基础 Python → TypeScript 类型转换**  
- 🌈 **高级类型转换**：联合类型、可选类型、字面量类型等  
- 🔄 **循环引用处理**：自动检测并化解类型循环依赖  
- 🎨 **自定义类型映射**：可扩展的映射表，随心定制  
- 🔌 **插件系统**：即插即用，轻松扩展新类型  
- 📄 **多种输出格式**：一键生成字符串或落盘文件  

---

## 📦 支持的类型

| 类别 | 图标 | 类型示例 |
|---|---|---|
| 基础类型 | 🔤 | `str`, `int`, `float`, `bool`, `None`, `Any`, `object` |
| 容器类型 | 📚 | `List`, `Dict`, `Set`, `Tuple`, `Union`, `Optional` |
| 自定义类型 | 🧩 | `NewType`, `TypeVar`, `TypedDict` |
| 类类型 | 🏗️ | `dataclass` 自动转换 |
| 函数类型 | ⚙️ | 函数签名级转换 |
| 插件加持 | 🔌 | Pydantic BaseModel, SQLModel … |

---

## 🚀 安装

| 包管理器 | 命令 |
|---|---|
| **uv** | `uv add pytots` |
| **pip** | `pip install pytots` |

---

## 🏁 快速开始

### 1️⃣ 基础使用

```python
from pytots import convert_to_ts,get_output_ts_str
from typing import List,TypedDict

class TicketType(TypedDict):
    id: int
    name: str
    description: str
    
# 基础类型转换
o_type = convert_to_ts(TicketType)
print(o_type)  #输出 -> TicketType

# 获取完整的TypeScript代码字符串
ts_code = get_output_ts_str(None,True)
print(ts_code)
```
输出结果：
``` typescript
type TicketType = {
    id : number;
    name : string;
    description : string;
}
```

#### 1.1 获取类型字符串

```python
# 获取类型字符串
type_str = convert_to_ts(TicketType)
print(type_str)  # 输出: "TicketType"
```

#### 1.2 输出到文件

```python
# 直接输出到文件
output_ts_file("output/types.d.ts", "MyModule",True)
```



### 2️⃣ 自定义类型映射
目前支持以下类型自定义，默认的映射关系如下：
- `datetime.date`  => `string`
- `datetime.datetime`  => `string`
- `None`  => `"undefined | null"`

修改默认映射关系：
```python
from pytots import replaceable_type_map
import datetime

# 自定义可替换类型映射
replaceable_type_map({
    datetime.date: "Date",
    datetime.datetime: "Date",
})
```

### 3️⃣ 插件系统
pytots提供了一个灵活的插件系统，允许你扩展对特定类型的支持。
#### 3.1 内置插件
当前已内置了以下插件，无需注册自动启用：
- `DataclassPlugin`：数据类插件，将Python dataclass转换为TypeScript类型。
- `TypedDictPlugin`：字典插件，将Python TypedDict转换为TypeScript类型。

#### 3.2 扩展插件
当前已集成了以下扩展插件：
- `PydanticPlugin`：支持将Pydantic BaseModel转换为TypeScript类型。
- `SqlModelPlugin`：支持将SQLModel转换为TypeScript类型。

扩展插件需要手动注册才能生效，使用方式：
```python
from pytots import use_plugin
from pytots.plugin.plus import PydanticPlugin, SqlModelPlugin

# 注册插件
use_plugin(PydanticPlugin(), SqlModelPlugin())
```

#### 3.3 修改插件默认行为：
系统默认在处理dataclass和typedict时，会使用`type`前缀的TypeScript类型。如果需要将其修改为`interface`，可以通过覆盖插件默认行为实现。

```python
from pytots import override_plugin
from pytots.plugin.inner import DataclassPlugin, TypedDictPlugin

# 覆盖默认插件行为
override_plugin(
    DataclassPlugin(dict(type_prefix="interface")),
    TypedDictPlugin(dict(type_prefix="interface"))
    )
```

#### 3.4 自定义插件
根据需要自定义插件，继承`DataclassPlugin`插件类，并实现`is_supported`方法。

##### 3.4.1 插件简单用法示例
假设你有一些类，你想将其转换为TypeScript类型。
```python
from typing import Generic,TypeVar

T = TypeVar("T")

class MyUser:
    id: int
    name: str

class MyAdmin(MyUser):
    role: str

class MyTicket(Generic[T]):
    id: int
    name: str
    description: str|None
    exc: T|None


class MyTicketAdmin(MyTicket[MyAdmin]):
    pass
    
```

自定义插件
```python
from pytots import Plugin
from typing import Any

class MyCustomPlugin(DataclassPlugin):
    name = "MyCustomPlugin"    # 插件名称
    type_prefix = "interface"  # 使用interface前缀

    def is_supported(self, python_type) -> bool:
        return python_type in [MyUser,MyTicket,MyAdmin,MyTicketAdmin]
```
使用自定义插件
```python
from pytots import use_plugin
from pytots import convert_to_ts,get_output_ts_str

use_plugin(MyCustomPlugin())

# 转换自定义类型
o_type = convert_to_ts(MyTicketAdmin)
print(o_type)  #输出 -> MyTicketAdmin

# 查看转换后的具体ts代码
ts_code = get_output_ts_str(None,True)
print(ts_code)

```
转换结果:
```typescript
interface MyAdmin {
    id : number;
    name : string;
    role : string;
}
interface MyTicket<T extends any> {
    id : number;
    name : string;
    description ? : string | null | undefined;
    exc ? : T | null | undefined;
}
interface MyTicketAdmin extends MyTicket<MyAdmin> {
    id : number;
    name : string;
    description ? : string | null | undefined;
    exc ? : MyAdmin | null | undefined;
}
```
##### 3.4.2 插件高级用法示例
实现对特定类型的转换或过滤一些类型时。可继承`Plugin`类，实现`converter`和`is_supported`方法。如有大量现有类需要直接进行字符串映射时，可以定义`TYPES_MAP`字典，键为Python类型，值为对应的TypeScript类型的字符串。

以下示例演示过滤掉`id`字段：
```python
from pytots.plugin.tools import generic_feild_fill,assemble_interface_type

class MyCustomPlugin(Plugin):
    
    name = "MyCustomPlugin"
    type_prefix = "interface"
    
    def is_supported(self, python_type) -> bool:
        return python_type in [MyUser,MyTicket,MyAdmin,MyTicketAdmin]

    def converter(self, python_type, **extra) -> str:
        class_name = python_type.__name__
        fields = []
        for field, field_type in get_type_hints(python_type).items():
            ts_type = generic_feild_fill(self,field_type)

            # 过滤掉id字段
            if field == "id":
                continue
            
            # 处理可选字段
            if "undefined" in ts_type:
                fields.append(f"{field}?: {ts_type};")
            else:
                fields.append(f"{field}: {ts_type};")

        fields_str = "\n  ".join(fields)
        
        return assemble_interface_type(self, class_name, fields_str)
```
同上面一样执行，得到转换结果：
```typescript
interface MyAdmin {
    name : string;
    role : string;
}
interface MyTicket<T extends any> {
    name : string;
    description ? : string | null | undefined;
    exc ? : T | null | undefined;
}
interface MyTicketAdmin extends MyTicket<MyAdmin> {
    name : string;
    description ? : string | null | undefined;
    exc ? : MyAdmin | null | undefined;
}
```



## 🔌 核心接口

| 函数 | 说明 | 签名 |
|---|---|---|
| `convert_to_ts` | 将单个 Python 类型转为 TypeScript 类型字符串 | `convert_to_ts(python_type) -> str` |
| `get_output_ts_str` | 获取当前已转换的全部 TypeScript 代码 | `get_output_ts_str(module_name=None, format=False) -> str` |
| `output_ts_file` | 将结果直接写入 `.d.ts` 文件 | `output_ts_file(file_path, module_name=None, format=False) -> None` |
| `replaceable_type_map` | 全局覆盖默认类型映射表 | `replaceable_type_map(type_map: dict[type, str]) -> None` |
| `use_plugin` | 注册一个或多个插件 | `use_plugin(*plugins: Plugin) -> None` |
| `override_plugin` | 用新实例覆盖同名插件 | `override_plugin(*plugins: Plugin) -> None` |


✨ **重要特性：**
>  **自动级联**：只要调用一次 `convert_to_ts`，其依赖的所有类型会被隐式转换并缓存，后续直接通过 `get_output_ts_str` 即可一次性拿到完整代码。

> 你可能发现了前面的示例我们并没有每一个类型都去处理，但是却转换了全部相关的类型。
这是因为pytots在处理类型时，会自动地处理所有相关的类型。



### convert_to_ts

将Python类型转换为TypeScript类型。

```python
convert_to_ts(python_type) -> str
```




### get_output_ts_str

获取转换后的TypeScript代码字符串。

```python
get_output_ts_str(module_name: str | None = "PytsDemo", format: bool = False) -> str
```

### output_ts_file

将转换结果输出到文件。

```python
output_ts_file(file_path: str, module_name: str | None = "PytsDemo", format: bool = False) -> None
```

### replaceable_type_map

自定义可替换类型映射。

```python
replaceable_type_map(type_map: dict[type, str]) -> None
```

### use_plugin

注册插件。

```python
use_plugin(*plugins: Plugin) -> None
```

### override_plugin

覆盖已注册的插件。

```python
override_plugin(*plugins: Plugin) -> None
```

