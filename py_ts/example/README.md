# py-ts 示例代码

本目录包含 py-ts 项目的完整示例代码，展示了项目的各种功能和最佳实践。

## 示例文件说明

### 1. 基础类型转换示例
**文件**: `basic_types_example.py`

展示 py-ts 对基本 Python 类型的 TypeScript 转换支持：
- 基本类型：`int`, `float`, `str`, `bool`, `bytes`
- 容器类型：`List`, `Dict`, `Tuple`, `Set`
- 联合类型和可选类型：`Union`, `Optional`
- 嵌套类型和复杂类型组合

**运行方法**:
```bash
cd d:\Mycode\py_ts\py_ts\example
python basic_types_example.py
```

**生成文件**: `basic_types.ts`

### 2. 高级类型转换示例
**文件**: `advanced_types_example.py`

展示 py-ts 对高级 Python 类型的 TypeScript 转换支持：
- `TypedDict`: 转换为 TypeScript 的 interface
- `NewType`: 转换为 TypeScript 的类型别名
- `TypeVar`: 泛型类型变量转换
- `dataclass`: 数据类转换
- 函数类型转换
- 集成演示

**运行方法**:
```bash
python advanced_types_example.py
```

**生成文件**: `advanced_types.ts`

### 3. 函数和类转换示例
**文件**: `functions_classes_example.py`

展示 py-ts 对 Python 函数和类的 TypeScript 转换支持：
- 函数签名转换
- 类结构转换
- 方法签名转换
- 回调模式转换
- 工具函数转换

**运行方法**:
```bash
python functions_classes_example.py
```

**生成文件**: `functions_classes.ts`

### 4. 实际应用场景示例
**文件**: `real_world_scenarios.py`

展示 py-ts 在真实项目中的使用：
- API 客户端类型定义
- 数据库模型类型定义
- 前端组件 Props 和状态类型
- 电商平台类型定义
- 配置管理类型定义

**运行方法**:
```bash
python real_world_scenarios.py
```

**生成文件**: `real_world_scenarios.ts`

### 5. 使用指南和最佳实践
**文件**: `best_practices_guide.py`

提供 py-ts 的完整使用指南和最佳实践：
- 基础使用指南
- 类型映射最佳实践
- 复杂类型使用指南
- 函数转换模式
- 模块组织技巧
- 常见陷阱和解决方案
- 性能优化技巧
- 构建系统集成

**运行方法**:
```bash
python best_practices_guide.py
```

**生成文件**: `best_practices.ts`

## 快速开始

### 1. 安装依赖
确保已安装 py-ts 项目依赖：
```bash
cd d:\Mycode\py_ts
uv sync
```

### 2. 运行示例
选择要运行的示例文件：
```bash
cd py_ts\example
python basic_types_example.py
```

### 3. 查看生成的文件
每个示例都会生成对应的 TypeScript 文件，位于示例目录中。

## 示例代码结构

每个示例文件都包含：
1. **导入部分**: 导入必要的模块和类型
2. **演示函数**: 多个演示函数展示不同功能
3. **转换调用**: 使用 `convert_to_ts()` 转换类型
4. **输出功能**: 使用 `get_output_ts_str()` 和 `output_ts_file()` 输出结果
5. **主函数**: 运行所有演示

## 学习路径建议

建议按以下顺序学习示例：

1. **初学者**: 从 `basic_types_example.py` 开始，了解基础类型转换
2. **进阶用户**: 学习 `advanced_types_example.py`，掌握高级类型转换
3. **实际应用**: 查看 `real_world_scenarios.py`，了解真实项目中的应用
4. **最佳实践**: 阅读 `best_practices_guide.py`，掌握专业用法

## 常见问题

### Q: 如何运行所有示例？
A: 可以逐个运行每个示例文件，或者创建一个批处理脚本运行所有示例。

### Q: 生成的 TypeScript 文件如何使用？
A: 可以将生成的文件复制到 TypeScript 项目中，或作为类型定义的参考。

### Q: 如何自定义模块名？
A: 在调用 `get_output_ts_str()` 或 `output_ts_file()` 时指定模块名参数。

### Q: 如何处理循环引用？
A: 使用字符串字面量引用类型，如 `List['User']` 而不是 `List[User]`。

## 贡献

欢迎为示例代码库贡献新的示例或改进现有示例！

## 许可证

本示例代码遵循与 py-ts 项目相同的许可证。

---

通过学习和运行这些示例，您将能够：
- 掌握 py-ts 的所有功能
- 了解类型转换的最佳实践
- 在实际项目中有效使用 py-ts
- 避免常见的陷阱和问题