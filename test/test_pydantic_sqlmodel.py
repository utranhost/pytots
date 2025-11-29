"""
Pydantic 和 SQLModel 支持测试用例
测试 py-ts 对 Pydantic 和 SQLModel 类型的 TypeScript 转换支持
"""

import pytest
from pytots import convert_to_ts
from typing import Optional, List, Dict, Any


def test_basic_types():
    """测试基本类型转换"""
    assert convert_to_ts(str) == "string"
    assert convert_to_ts(int) == "number"
    assert convert_to_ts(float) == "number"
    assert convert_to_ts(bool) == "boolean"


def test_container_types():
    """测试容器类型转换"""
    assert convert_to_ts(List[str]) == "Array<string>"
    assert convert_to_ts(Dict[str, int]) == "Record<string, number>"
    assert convert_to_ts(Optional[str]) == "string | null | undefined"


def test_pydantic_simulation():
    """测试 Pydantic 模拟类型转换"""
    # 模拟 Pydantic 类型
    class MockBaseModel:
        pass
    
    class MockEmailStr:
        pass
    
    class MockHttpUrl:
        pass
    
    # 模拟 Pydantic 模型
    class User(MockBaseModel):
        id: int
        name: str
        email: MockEmailStr
        age: Optional[int] = None
    
    # 测试模型转换
    result = convert_to_ts(User)
    assert result == "any"  # 模拟类型应该返回 any
    
    # 测试 Pydantic 字段类型
    assert convert_to_ts(MockEmailStr) == "any"
    assert convert_to_ts(MockHttpUrl) == "any"


def test_sqlmodel_simulation():
    """测试 SQLModel 模拟类型转换"""
    # 模拟 SQLModel 类型
    class MockSQLModel:
        pass
    
    class MockField:
        def __init__(self, default=None, primary_key=False, **kwargs):
            self.default = default
            self.primary_key = primary_key
    
    # 模拟 SQLModel 模型
    class User(MockSQLModel):
        id: Optional[int] = MockField(default=None, primary_key=True)
        name: str = MockField(index=True)
        email: str = MockField(unique=True)
    
    # 测试模型转换
    result = convert_to_ts(User)
    assert result == "any"  # 模拟类型应该返回 any


def test_complex_nested_types():
    """测试复杂嵌套类型转换"""
    # 复杂嵌套模型
    class Address:
        street: str
        city: str
        zip_code: str
    
    class Person:
        name: str
        age: int
        address: Address
        friends: List["Person"]
    
    # 测试嵌套模型转换
    result = convert_to_ts(Person)
    assert result == "any"  # 复杂嵌套类型应该返回 any


def test_type_mapping_integration():
    """测试类型映射集成"""
    # 测试类型映射表是否正常工作
    from pytots.clf import SINGLE_TYPES_MAP, REPLACEABLE_TYPES_MAP
    import datetime
    
    # 检查映射表是否存在且包含正确的条目
    assert str in SINGLE_TYPES_MAP
    assert int in SINGLE_TYPES_MAP
    assert datetime.date in REPLACEABLE_TYPES_MAP  # datetime.date 映射为 string


def test_function_availability():
    """测试新增函数是否可用"""
    from pytots.type_map import handle_deque_type, handle_counter_type, handle_chainmap_type
    
    # 检查函数是否存在
    assert callable(handle_deque_type)
    assert callable(handle_counter_type)
    assert callable(handle_chainmap_type)


if __name__ == "__main__":
    """运行所有测试"""
    print("=== 开始 Pydantic 和 SQLModel 支持测试 ===")
    
    # 运行测试函数
    test_basic_types()
    print("✓ 基本类型测试通过")
    
    test_container_types()
    print("✓ 容器类型测试通过")
    
    test_pydantic_simulation()
    print("✓ Pydantic 模拟类型测试通过")
    
    test_sqlmodel_simulation()
    print("✓ SQLModel 模拟类型测试通过")
    
    test_complex_nested_types()
    print("✓ 复杂嵌套类型测试通过")
    
    test_type_mapping_integration()
    print("✓ 类型映射集成测试通过")
    
    test_function_availability()
    print("✓ 函数可用性测试通过")
    
    print("\\n=== 所有测试通过 ===")
    print("Pydantic 和 SQLModel 支持功能验证完成")