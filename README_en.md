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

A lightweight tool to elegantly convert **Python types** to **TypeScript types**.

---

## ✨ Features

- 🔧 **Basic Python → TypeScript type conversion**
- 🌈 **Advanced type conversion**: Union types, optional types, literal types, etc.
- 🔄 **Circular reference handling**: Automatically detects and resolves type circular dependencies
- 🎨 **Customizable type mapping**: Extensible mapping table for customization
- 🔌 **Plugin system**: Plug-and-play, easily extend with new types
- 📄 **Multiple output formats**: One-click generation of strings or file output

---

## 📦 Supported Types

| Category | Icon | Type Examples |
|---|---|---|
| Basic Types | 🔤 | `str`, `int`, `float`, `bool`, `None`, `Any`, `object` |
| Container Types | 📚 | `List`, `Dict`, `Set`, `Tuple`, `Union`, `Optional` |
| Custom Types | 🧩 | `NewType`, `TypeVar`, `TypedDict` |
| Class Types | 🏗️ | Automatic conversion of `dataclass` |
| Function Types | ⚙️ | Function signature level conversion |
| Plugin Enhanced | 🔌 | Pydantic BaseModel, SQLModel … |

---

## 🚀 Installation

| Package Manager | Command |
|---|---|
| **uv** | `uv add pytots` |
| **pip** | `pip install pytots` |

---

## 🏁 Quick Start

### 1️⃣ Basic Usage

```python
from pytots import convert_to_ts,get_output_ts_str
from typing import List,TypedDict

class TicketType(TypedDict):
    id: int
    name: str
    description: str
    
# Basic type conversion
o_type = convert_to_ts(TicketType)
print(o_type)  # Output -> TicketType

# Get complete TypeScript code string
ts_code = get_output_ts_str(None,True)
print(ts_code)
```

Output result:
```typescript
type TicketType = {
    id : number;
    name : string;
    description : string;
}
```

#### 1.1 Get Type String

```python
# Get type string
type_str = convert_to_ts(TicketType)
print(type_str)  # Output: "TicketType"
```

#### 1.2 Output to File

```python
# Direct output to file
output_ts_file("output/types.d.ts", "MyModule",True)
```

### 2️⃣ Custom Type Mapping

Currently supports the following customizable type mappings. Default mappings are as follows:
- `datetime.date`  => `string`
- `datetime.datetime`  => `string`
- `None`  => `"undefined | null"`

Modify default mappings:
```python
from pytots import replaceable_type_map
import datetime

# Custom replaceable type mapping
replaceable_type_map({
    datetime.date: "Date",
    datetime.datetime: "Date",
})
```

### 3️⃣ Plugin System

pytots provides a flexible plugin system that allows you to extend support for specific types.

#### 3.1 Built-in Plugins

The following plugins are currently built-in and automatically enabled without registration:
- `DataclassPlugin`: Data class plugin, converts Python dataclass to TypeScript types.
- `TypedDictPlugin`: Dictionary plugin, converts Python TypedDict to TypeScript types.

#### 3.2 Extended Plugins

The following extended plugins are currently integrated:
- `PydanticPlugin`: Supports converting Pydantic BaseModel to TypeScript types.
- `SqlModelPlugin`: Supports converting SQLModel to TypeScript types.

Extended plugins need to be manually registered to take effect:
```python
from pytots import use_plugin
from pytots.plugin.plus import PydanticPlugin, SqlModelPlugin

# Register plugins
use_plugin(PydanticPlugin(), SqlModelPlugin())
```

#### 3.3 Modify Plugin Default Behavior

By default, the system uses TypeScript types with `type` prefix when processing dataclass and typedict. If you need to change this to `interface`, you can achieve this by overriding plugin defaults.

```python
from pytots import override_plugin
from pytots.plugin.inner import DataclassPlugin, TypedDictPlugin

# Override default plugin behavior
override_plugin(
    DataclassPlugin(dict(type_prefix="interface")),
    TypedDictPlugin(dict(type_prefix="interface"))
    )
```

#### 3.4 Custom Plugins

Customize plugins according to your needs by inheriting from the `DataclassPlugin` class and implementing the `is_supported` method.

##### 3.4.1 Simple Plugin Usage Example

Suppose you have some classes that you want to convert to TypeScript types:
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

Custom plugin:
```python
from pytots import Plugin
from typing import Any

class MyCustomPlugin(DataclassPlugin):
    name = "MyCustomPlugin"    # Plugin name
    type_prefix = "interface"  # Use interface prefix

    def is_supported(self, python_type) -> bool:
        return python_type in [MyUser,MyTicket,MyAdmin,MyTicketAdmin]
```

Using custom plugin:
```python
from pytots import use_plugin
from pytots import convert_to_ts,get_output_ts_str

use_plugin(MyCustomPlugin())

# Convert custom type
o_type = convert_to_ts(MyTicketAdmin)
print(o_type)  # Output -> MyTicketAdmin

# View the converted specific ts code
ts_code = get_output_ts_str(None,True)
print(ts_code)

```

Conversion result:
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

##### 3.4.2 Advanced Plugin Usage Example

When implementing conversion for specific types or filtering some types, you can inherit the `Plugin` class and implement the `converter` and `is_supported` methods. If you have many existing classes that need direct string mapping, you can define a `TYPES_MAP` dictionary with Python types as keys and corresponding TypeScript type strings as values.

The following example demonstrates filtering out the `id` field:
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

            # Filter out id field
            if field == "id":
                continue
            
            # Handle optional fields
            if "undefined" in ts_type:
                fields.append(f"{field}?: {ts_type};")
            else:
                fields.append(f"{field}: {ts_type};")

        fields_str = "\n  ".join(fields)
        
        return assemble_interface_type(self, class_name, fields_str)
```

Executing the same as above, getting the conversion result:
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

## 🔌 Core Interfaces

| Function | Description | Signature |
|---|---|---|
| `convert_to_ts` | Converts a single Python type to TypeScript type string | `convert_to_ts(python_type) -> str` |
| `get_output_ts_str` | Gets all converted TypeScript code | `get_output_ts_str(module_name=None, format=False) -> str` |
| `output_ts_file` | Writes results directly to `.d.ts` file | `output_ts_file(file_path, module_name=None, format=False) -> None` |
| `replaceable_type_map` | Globally overrides default type mapping table | `replaceable_type_map(type_map: dict[type, str]) -> None` |
| `use_plugin` | Registers one or more plugins | `use_plugin(*plugins: Plugin) -> None` |
| `override_plugin` | Overrides plugins with the same name with new instances | `override_plugin(*plugins: Plugin) -> None` |

✨ **Key Features:**
> **Automatic Cascading**: Just call `convert_to_ts` once, and all dependent types will be implicitly converted and cached. Later, you can get the complete code at once through `get_output_ts_str`.

> You may have noticed that in the previous examples, we didn't process every type individually, but still converted all related types.
This is because pytots automatically handles all related types when processing types.

### convert_to_ts

Converts Python types to TypeScript types.

```python
convert_to_ts(python_type) -> str
```

### get_output_ts_str

Gets the converted TypeScript code string.

```python
get_output_ts_str(module_name: str | None = "PytsDemo", format: bool = False) -> str
```

### output_ts_file

Outputs conversion results to a file.

```python
output_ts_file(file_path: str, module_name: str | None = "PytsDemo", format: bool = False) -> None
```

### replaceable_type_map

Customizes replaceable type mapping.

```python
replaceable_type_map(type_map: dict[type, str]) -> None
```

### use_plugin

Registers plugins.

```python
use_plugin(*plugins: Plugin) -> None
```

### override_plugin

Overrides registered plugins.

```python
override_plugin(*plugins: Plugin) -> None
```