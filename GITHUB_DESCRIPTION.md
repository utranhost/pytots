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
from pytots import convert_to_ts, get_output_ts_str

# 转换Python类型为TypeScript
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

# 获取完整模块定义
ts_code = get_output_ts_str("UserModule")
```

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
| `List[T]` | `T[]` | `tags: string[]` |
| `Dict[K, V]` | `Record<K, V>` | `data: Record<string, number>` |
| `Optional[T]` | `T \| null` | `email?: string \| null` |
| `Union[T, U]` | `T \| U` | `status: 'active' \| 'inactive'` |

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