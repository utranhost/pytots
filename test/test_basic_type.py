import pytest
from pytots import convert_to_ts
from typing import Set, FrozenSet, Deque, List, Dict, Any
from collections import deque, Counter, ChainMap
import datetime



# basic types
def test_basic_types():
    """测试基本类型转换"""
    assert convert_to_ts(str) == "string"
    assert convert_to_ts(int) == "number"
    assert convert_to_ts(float) == "number"
    assert convert_to_ts(bool) == "boolean"
    assert convert_to_ts(list) == "any[]"
    assert convert_to_ts(tuple) == "any[]"
    assert convert_to_ts(dict) == "Record<string, any>"
    assert convert_to_ts(set) == "Set<any>"
    assert convert_to_ts(frozenset) == "ReadonlySet<any>"
    assert convert_to_ts(Any) == "any"
    
    # 用户可替换类型
    assert convert_to_ts(None) == "undefined | null"
    assert convert_to_ts(datetime.datetime) == "Date"
    assert convert_to_ts(datetime.date) == "Date"
    
    
def test_set_types():
    """测试集合类型转换"""
    # 基本集合类型
    assert convert_to_ts(set) == "Set<any>"
    assert convert_to_ts(frozenset) == "ReadonlySet<any>"
    
    # 泛型集合类型
    assert convert_to_ts(Set[int]) == "Set<number>"
    assert convert_to_ts(FrozenSet[str]) == "ReadonlySet<string>"
    assert convert_to_ts(Set[List[str]]) == "Set<Array<string>>"
    
    # 复杂嵌套类型
    assert convert_to_ts(Set[Dict[str, int]]) == "Set<Record<string, number>>"


def test_queue_types():
    """测试队列类型转换"""
    # 基本队列类型
    assert convert_to_ts(deque) == "Array<any>"
    
    # 泛型队列类型
    assert convert_to_ts(Deque[int|str]) == "Array<number | string>"
    assert convert_to_ts(Deque[str]) == "Array<string>"
    assert convert_to_ts(Deque[List[bool]]) == "Array<Array<boolean>>"


def test_counter_types():
    """测试计数器类型转换"""
    # 基本计数器类型
    assert convert_to_ts(Counter) == "Record<any, number>"
    
    # 泛型计数器类型
    assert convert_to_ts(Counter[str]) == "Record<string, number>"
    assert convert_to_ts(Counter[int]) == "Record<number, number>"


def test_chainmap_types():
    """测试链式映射类型转换"""
    # 基本链式映射类型
    assert convert_to_ts(ChainMap) == "Record<any, any>"
    
    # 泛型链式映射类型
    assert convert_to_ts(ChainMap[str, int]) == "Record<string, number>"
    assert convert_to_ts(ChainMap[int, str]) == "Record<number, string>"


def test_complex_collection_types():
    """测试复杂嵌套集合类型"""
    assert convert_to_ts(list[dict[str, int]]) == "Array<Record<string, number>>"
    assert convert_to_ts(set[tuple[int, str]]) == "Set<[number, string]>"
    assert convert_to_ts(dict[str, list[set[int]]]) == "Record<string, Array<Set<number>>>"
    assert convert_to_ts(deque[Counter[str]]) == "Array<Record<string, number>>"
    assert convert_to_ts(ChainMap[str, list[int]]) == "Record<string, Array<number>>"


def test_tuple_types():
    """测试改进后的元组类型映射"""
    # 基本元组类型
    assert convert_to_ts(tuple) == "any[]"
    assert convert_to_ts(tuple[int]) == "[number]"
    assert convert_to_ts(tuple[int, str]) == "[number, string]"
    assert convert_to_ts(tuple[int, str, bool]) == "[number, string, boolean]"
    
    # 可变长度元组
    assert convert_to_ts(tuple[int, ...]) == "number[]"
    assert convert_to_ts(tuple[str, ...]) == "string[]"
    
    # 嵌套元组类型
    assert convert_to_ts(tuple[list[int], dict[str, bool]]) == "[Array<number>, Record<string, boolean>]"
    assert convert_to_ts(tuple[tuple[int, str], ...]) == "[number, string][]"


def test_additional_basic_types():
    """测试新增的基础类型映射"""
    import decimal
    import uuid
    
    # bytes类型
    assert convert_to_ts(bytes) == "Uint8Array"
    assert convert_to_ts(bytearray) == "Uint8Array"
    
    # object类型
    assert convert_to_ts(object) == "any"
    
    # decimal类型
    assert convert_to_ts(decimal.Decimal) == "number"
    
    # uuid类型
    assert convert_to_ts(uuid.UUID) == "string"
    
    # complex类型
    assert convert_to_ts(complex) == "{real: number, imag: number}"
    
    # range类型
    assert convert_to_ts(range) == "{start: number, stop: number, step: number}"


if __name__ == "__main__":
    pytest.main([__file__])