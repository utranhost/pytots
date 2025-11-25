"""
基础类型转换示例
展示py-ts对基本Python类型的TypeScript转换支持
"""

from typing import Any, Union, Optional, List, Dict, Tuple, Set
from pytots import convert_to_ts, get_output_ts_str, output_ts_file

import os
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'test_ts_output')


def basic_types_demo():
    """基础类型转换演示"""
    print("=== 基础类型转换演示 ===")
    
    # 基本类型
    print("\n1. 基本类型:")
    print(f"int -> {convert_to_ts(int)}")        # number
    print(f"float -> {convert_to_ts(float)}")    # number
    print(f"str -> {convert_to_ts(str)}")        # string
    print(f"bool -> {convert_to_ts(bool)}")      # boolean
    print(f"bytes -> {convert_to_ts(bytes)}")   # Uint8Array
    
    # 容器类型
    print("\n2. 容器类型:")
    print(f"List[int] -> {convert_to_ts(List[int])}")          # Array<number>
    print(f"Dict[str, int] -> {convert_to_ts(Dict[str, int])}") # Record<string, number>
    print(f"Tuple[int, str] -> {convert_to_ts(Tuple[int, str])}") # [number, string]
    print(f"Set[str] -> {convert_to_ts(Set[str])}")            # Set<string>
    
    # 联合类型和可选类型
    print("\n3. 联合类型和可选类型:")
    print(f"Union[int, str] -> {convert_to_ts(Union[int, str])}")     # number | string
    print(f"Optional[str] -> {convert_to_ts(Optional[str])}")       # string | null | undefined
    print(f"Union[None, str] -> {convert_to_ts(Union[None, str])}")  # null | undefined | string
    
    # 嵌套类型
    print("\n4. 嵌套类型:")
    print(f"List[List[int]] -> {convert_to_ts(List[List[int]])}")          # Array<Array<number>>
    print(f"Dict[str, List[int]] -> {convert_to_ts(Dict[str, List[int]])}") # Record<string, Array<number>>
    print(f"Tuple[List[str], Dict[str, int]] -> {convert_to_ts(Tuple[List[str], Dict[str, int]])}") # [Array<string>, Record<string, number>]


def complex_types_demo():
    """复杂类型转换演示"""
    print("\n=== 复杂类型转换演示 ===")
    
    # Any类型
    print("\n1. Any类型:")
    print(f"Any -> {convert_to_ts(Any)}")  # any
    
    # 复杂联合类型
    print("\n2. 复杂联合类型:")
    complex_union = Union[int, str, bool, List[str], Dict[str, int]]
    print(f"Union[int, str, bool, List[str], Dict[str, int]] -> {convert_to_ts(complex_union)}") # number | string | boolean | Array<string> | Record<string, number>
    
    # 可选嵌套类型
    print("\n3. 可选嵌套类型:")
    print(f"Optional[List[Dict[str, int]]] -> {convert_to_ts(Optional[List[Dict[str, int]]])}") # Array<Record<string, number>> | null | undefined




if __name__ == "__main__":
    """运行所有演示"""
    basic_types_demo()
    complex_types_demo()
    
    res = get_output_ts_str()
    print(res)
    path = os.path.join(output_dir, "test_basic_types.ts")
    output_ts_file(path, None)
    
    print("\n=== 演示完成 ===")
    print("请查看生成的文件: basic_types.ts")