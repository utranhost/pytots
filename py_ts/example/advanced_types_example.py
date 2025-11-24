"""
高级类型转换示例
本章节演示
- `convert_to_ts` 可以自动识别引用的类型，并递归转换，确保所有类型都被正确处理。
- `convert_to_ts`函数具有全局状态，每次调用会累积转换结果，如果需要重置状态，调用`reset_store`函数
- `convert_to_ts`函数结合`get_output_ts_str`或`output_ts_file`函数实现灵活输出
- `get_output_ts_str`函数获取当前累积的转换结果
- `output_ts_file`函数将当前累积的转换结果保存到指定文件。
"""

from typing import TypedDict, NewType, TypeVar, Generic, Callable, Optional, List, Dict, Any
from dataclasses import dataclass
from py_ts import convert_to_ts, get_output_ts_str, output_ts_file, reset_store


def typed_dict_demo():
    """TypedDict转换演示"""
    print("=== TypedDict转换演示 ===")
    
    # 基础TypedDict
    class User(TypedDict):
        """用户信息类型"""
        id: int
        username: str
        email: str
        is_active: bool
    
    # 嵌套TypedDict
    class Address(TypedDict):
        """地址信息类型"""
        street: str
        city: str
        zip_code: str
        country: str
    
    class UserProfile(TypedDict):
        """用户档案类型"""
        user: User
        addresses: List[Address]
        preferences: Dict[str, Any]
        created_at: str
        last_login: Optional[str]
    
    
    # 单继承测试
    class AdminUser(User):
        """管理员用户类型"""
        is_admin: bool
    
    # 多继承测试
    class SuperAdminUser(User, AdminUser):
        """超级管理员用户类型"""
        is_super_admin: bool
    
    
    
    
    # 转换TypedDict
    convert_to_ts(User)
    convert_to_ts(AdminUser)
    convert_to_ts(SuperAdminUser)
    convert_to_ts(Address)
    convert_to_ts(UserProfile)
    
    print("TypedDict类型已转换完成")
    res = get_output_ts_str(None)
    print(res)
    reset_store()


def new_type_demo():
    """NewType转换演示"""
    print("\n=== NewType转换演示 ===")
    
    # 定义NewType
    UserId = NewType("UserId", int)
    Email = NewType("Email", str)
    Timestamp = NewType("Timestamp", int)
    
    # 基于NewType的复杂类型
    ApiKey = NewType("ApiKey", str)
    SecretToken = NewType("SecretToken", str)
    
    # 转换NewType
    convert_to_ts(UserId)
    convert_to_ts(Email)
    convert_to_ts(Timestamp)
    convert_to_ts(ApiKey)
    convert_to_ts(SecretToken)
    
    res = get_output_ts_str(None)
    
    print("NewType类型已转换完成")
    print(res)
    reset_store()


def type_var_demo():
    """TypeVar转换演示"""
    print("\n=== TypeVar转换演示 ===")
    
    # 基础TypeVar
    T = TypeVar("T")
    U = TypeVar("U")
    
    # 有约束的TypeVar
    Numeric = TypeVar("Numeric", int, float)
    StringLike = TypeVar("StringLike", str, bytes)
    
    # 有边界的TypeVar
    Comparable = TypeVar("Comparable", bound=int)
    Serializable = TypeVar("Serializable", bound=Dict[str, Any])
    
    # 转换TypeVar
    convert_to_ts(T)
    convert_to_ts(U)
    convert_to_ts(Numeric)
    convert_to_ts(StringLike)
    convert_to_ts(Comparable)
    convert_to_ts(Serializable)
    res = get_output_ts_str(None)
    print("TypeVar类型已转换完成")
    print(res)
    reset_store()


def dataclass_demo():
    """dataclass转换演示"""
    print("\n=== dataclass转换演示 ===")
    
    @dataclass
    class Point:
        """坐标点"""
        x: int
        y: int
        z: Optional[int] = None
    
    @dataclass
    class Rectangle:
        """矩形"""
        top_left: Point
        bottom_right: Point
        color: str = "black"
    
    @dataclass
    class UserData:
        """用户数据"""
        user_id: int
        username: str
        email: str
        points: List[Point]
        metadata: Dict[str, Any]
        created_at: str
        
    # 转换dataclass
    convert_to_ts(Point)
    convert_to_ts(Rectangle)
    convert_to_ts(UserData)
    res = get_output_ts_str(None)
    print("dataclass类型已转换完成")
    print(res)
    reset_store()


def function_demo():
    """函数类型转换演示"""
    print("\n=== 函数类型转换演示 ===")
    
    def simple_function(name: str, age: int) -> str:
        ...
    
    def complex_function(
        data: Dict[str, Any],
        callback: Callable[[str], int],
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        ...
    
    def api_handler(
        endpoint: str,
        method: str,
        headers: Dict[str, str],
        body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
       ...
    
    # 转换函数
    convert_to_ts(simple_function)
    convert_to_ts(complex_function)
    convert_to_ts(api_handler)
    
    res = get_output_ts_str(None)
    print("函数类型已转换完成")
    print(res)
    reset_store()


def integration_demo():
    """集成演示 - 组合使用各种类型"""
    print("\n=== 集成演示 ===")
    
    # 定义集成类型
    UserId = NewType("UserId", int)
    
    class User(TypedDict):
        id: UserId
        username: str
        email: str
    
    @dataclass
    class ApiResponse:
        success: bool
        data: Optional[User]
        error: Optional[str]
        timestamp: int
    
    def process_user(
        user_id: UserId,
        callback: Callable[[User], bool]
    ) -> ApiResponse:
        """处理用户数据的函数"""
        return ApiResponse(success=True, data=None, error=None, timestamp=1234567890)
    
    # 转换所有类型
    convert_to_ts(UserId)
    convert_to_ts(User)
    convert_to_ts(ApiResponse)
    convert_to_ts(process_user)
    
    res = get_output_ts_str(None)
    print("集成类型已转换完成")
    print(res)
    reset_store()


def output_advanced_types():
    """输出高级类型转换结果"""
    print("\n=== 输出结果 ===")
    
    # 定义一些复杂类型，最后集成应用到dataclass和typedict
    UserId = NewType("UserId", int)
    
    class Address(TypedDict):
        """地址信息"""
        street: str
        city: str
        state: str
        zip: str
    
    class UserProfile(TypedDict):
        """用户个人信息"""
        name: str
        age: int
        address: Address
    
    class User(TypedDict):
        """用户信息"""
        id: UserId
        profile: UserProfile
        additional_info: Dict[str, Any] | None
    
    
    # 只转换User类型，其他类型会被自动转换
    convert_to_ts(User)
    # 获取所有转换结果
    ts_code = get_output_ts_str("AdvancedTypes")
    print("生成的TypeScript代码:")
    print(ts_code)
    
    # 输出到文件
    output_ts_file("advanced_types.ts", "AdvancedTypes")
    print("\nTypeScript代码已保存到: advanced_types.ts")


if __name__ == "__main__":
    """运行所有演示"""
    typed_dict_demo()
    new_type_demo()
    type_var_demo()
    dataclass_demo()
    function_demo()
    integration_demo()
    output_advanced_types()
    
    print("\n=== 高级类型演示完成 ===")
    print("请查看生成的文件: advanced_types.ts")