# pytots

A lightweight tool that helps you convert Python types to TypeScript types.

## Features

- **Basic Python to TypeScript type conversion**
- **Advanced type conversion**: Union, Optional, Literal, etc.
- **Circular reference handling**: Automatically detects and handles circular dependencies between types
- **Custom type mapping**: Extensible type mapping system
- **Plugin system**: Extend functionality through plugins
- **Multiple output formats**: Support for string output and file output

### Supported Types

- **Basic types**: `str`, `int`, `float`, `bool`, `None`, `Any`, `object`
- **Container types**: `List`, `Dict`, `Set`, `Tuple`, `Union`, `Optional`
- **Custom types**: `NewType`, `TypeVar`, `TypedDict`
- **Class types**: `dataclass` conversion
- **Function types**: Function signature conversion
- **Plugin support**: Pydantic BaseModel, SQLModel

## Installation

Using uv:

```bash
uv add pytots
```

Or using pip:

```bash
pip install pytots
```

## Quick Start

### Basic Usage

```python
from pytots import convert_to_ts, get_output_ts_str, output_ts_file

# Basic type conversion
result = convert_to_ts({
    'name': str,
    'age': int,
    'is_active': bool
})

print(result)
# Output: interface GeneratedInterface {
#   name: string;
#   age: number;
#   is_active: boolean;
# }

# Get complete TypeScript code string
ts_code = get_output_ts_str("MyModule")
print(ts_code)

# Direct output to file
output_ts_file("output/types.ts", "MyModule")
```

### Supported Type Examples

```python
from typing import TypedDict, NewType, TypeVar, Optional, List
from dataclasses import dataclass

# TypedDict conversion
class UserDict(TypedDict):
    name: str
    age: int

# NewType conversion
UserId = NewType("UserId", int)

# TypeVar conversion
T = TypeVar("T", int, str)

# dataclass conversion
@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None

# Function type conversion
def process_user(user: UserDict) -> bool:
    return True

# Convert all types
convert_to_ts(UserDict)
convert_to_ts(UserId)
convert_to_ts(T)
convert_to_ts(User)
convert_to_ts(process_user)

# Get complete TypeScript definitions
ts_code = get_output_ts_str("UserModule")
print(ts_code)
```

## Plugin System

pytots provides a plugin system to extend support for more type systems.

### Pydantic Support

```python
from pytots.plugin.plus import PydanticPlugin
from pytots import use_plugin
from pydantic import BaseModel, EmailStr

# Enable Pydantic plugin
use_plugin(PydanticPlugin())

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None

# Convert Pydantic model
convert_to_ts(User)
ts_code = get_output_ts_str("PydanticModule")
print(ts_code)
```

### SQLModel Support

```python
from pytots.plugin.plus import SqlModelPlugin
from pytots import use_plugin
from sqlmodel import SQLModel, Field

# Enable SQLModel plugin
use_plugin(SqlModelPlugin())

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)

# Convert SQLModel model
convert_to_ts(User)
ts_code = get_output_ts_str("SQLModelModule")
print(ts_code)
```

## API Reference

### Main Functions

- `convert_to_ts(obj) -> str`: Convert a single Python type to TypeScript definition
- `get_output_ts_str(module_name: str | None = "PytsDemo", format: bool = False) -> str`: Get complete TypeScript code string
- `output_ts_file(file_path: str, module_name: str | None = "PytsDemo", format: bool = True) -> None`: Output TypeScript code to file
- `reset_store() -> None`: Clear all converted type definition cache

### Plugin Related

- `Plugin`: Plugin base class
- `use_plugin(plugin: Plugin) -> None`: Enable plugin

## Examples

Check the example files in the `pytots/example/` directory:

- `basic_types_example.py` - Basic type conversion examples
- `advanced_types_example.py` - Advanced type conversion examples
- `circular_reference_example.py` - Circular reference handling examples
- `pydantic_example.py` - Pydantic type conversion examples
- `sqlmodel_example.py` - SQLModel type conversion examples

## Development

### Install Development Dependencies

```bash
uv sync --group dev
```

### Run Tests

```bash
pytest
```

### Project Structure

```
pytots/
├── __init__.py          # Main module exports
├── main.py              # Main functionality functions
├── type_map.py          # Type mapping system
├── processer.py         # Type processors
├── formart.py           # Code formatting
└── plugin/              # Plugin system
    ├── __init__.py
    └── plus/            # Extension plugins
        ├── pydantic_plugin.py
        └── sqlmodel_plugin.py
```

## License

MIT License