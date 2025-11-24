# pytots

一个轻量级的工具，帮助你将Python类型转换为TypeScript类型。

## 功能特性

- 支持基本Python类型到TypeScript类型的转换
- 支持高级类型（如Union、Optional等）
- 处理循环引用问题
- 支持自定义类型映射

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

查看 `py_ts/example/` 目录下的示例文件：

- `basic_types_example.py` - 基本类型转换示例
- `advanced_types_example.py` - 高级类型转换示例
- `circular_reference_example.py` - 循环引用处理示例

## 开发

```bash
# 安装开发依赖
uv sync --group dev

# 运行测试
pytest
```

## 许可证

MIT License