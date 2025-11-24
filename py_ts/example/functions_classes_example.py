"""
函数和类转换示例
展示py-ts对Python函数和类的TypeScript转换支持
"""

from typing import TypedDict, Callable, Optional, List, Dict, Any, Union
from dataclasses import dataclass
from py_ts import convert_to_ts, get_output_ts_str, output_ts_file, reset_store


def function_signatures_demo():
    """函数签名转换演示"""
    print("=== 函数签名转换演示 ===")
    
    # 简单函数
    def greet(name: str) -> str:
        """问候函数"""
        return f"Hello, {name}!"
    
    # 带可选参数的函数
    def create_user(
        username: str,
        email: str,
        age: Optional[int] = None,
        is_active: bool = True
    ) -> Dict[str, Any]:
        """创建用户函数"""
        return {
            "username": username,
            "email": email,
            "age": age,
            "is_active": is_active
        }
    
    # 回调函数
    def process_data(
        data: List[Dict[str, Any]],
        callback: Callable[[Dict[str, Any]], bool],
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> List[Dict[str, Any]]:
        """处理数据函数"""
        return [item for item in data if callback(item)]
    
    # 异步函数（类型注解）
    async def fetch_api(
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """API请求函数"""
        return {"status": "success"}
    
    # 泛型风格函数
    def find_item(
        items: List[Any],
        predicate: Callable[[Any], bool]
    ) -> Optional[Any]:
        """查找项目函数"""
        for item in items:
            if predicate(item):
                return item
        return None
    
    # 转换函数
    convert_to_ts(greet)
    convert_to_ts(create_user)
    convert_to_ts(process_data)
    convert_to_ts(fetch_api)
    convert_to_ts(find_item)
    res = get_output_ts_str(None)
    print("函数签名转换完成")
    print(res)
    reset_store()


def class_structures_demo():
    """类结构转换演示"""
    print("\n=== 类结构转换演示 ===")
    
    # 基础数据类
    @dataclass
    class Person:
        """人员信息"""
        name: str
        age: int
        email: str
        phone: Optional[str] = None
    
    # 嵌套数据类
    @dataclass
    class Address:
        """地址信息"""
        street: str
        city: str
        state: str
        zip_code: str
        country: str = "USA"
    
    @dataclass
    class Employee:
        """员工信息"""
        person: Person
        employee_id: int
        department: str
        salary: float
        address: Address
        skills: List[str]
        manager: Optional['Employee'] = None
    
    # 复杂数据类
    @dataclass
    class Project:
        """项目信息"""
        id: int
        name: str
        description: str
        team: List[Employee]
        budget: float
        timeline: Dict[str, Any]
        status: str  # "planning", "active", "completed", "cancelled"
        
    # 转换类
    convert_to_ts(Person)
    convert_to_ts(Address)
    convert_to_ts(Employee)
    convert_to_ts(Project)
    
    res = get_output_ts_str(None)
    print("类结构转换完成")
    print(res)
    reset_store()

def method_signatures_demo():
    """方法签名转换演示"""
    print("\n=== 方法签名转换演示 ===")
    
    class UserService:
        """用户服务类"""
        
        def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
            """获取用户信息"""
            return {"id": user_id, "name": "John Doe"}
        
        def create_user(
            self,
            username: str,
            email: str,
            password: str
        ) -> Dict[str, Any]:
            """创建用户"""
            return {
                "id": 1,
                "username": username,
                "email": email,
                "status": "active"
            }
        
        def update_user(
            self,
            user_id: int,
            updates: Dict[str, Any]
        ) -> bool:
            """更新用户信息"""
            return True
        
        def delete_user(self, user_id: int) -> bool:
            """删除用户"""
            return True
        
        def search_users(
            self,
            filters: Dict[str, Any],
            page: int = 1,
            per_page: int = 20
        ) -> Dict[str, Any]:
            """搜索用户"""
            return {
                "users": [],
                "total": 0,
                "page": page,
                "per_page": per_page
            }
    
    # 转换类方法
    user_service = UserService()
    convert_to_ts(user_service.get_user)
    convert_to_ts(user_service.create_user)
    convert_to_ts(user_service.update_user)
    convert_to_ts(user_service.delete_user)
    convert_to_ts(user_service.search_users)
    
    res = get_output_ts_str(None)
    print("方法签名转换完成")
    print(res)
    reset_store()


def callback_patterns_demo():
    """回调模式转换演示"""
    print("\n=== 回调模式转换演示 ===")
    
    # 事件处理器类型
    EventHandler = Callable[[Dict[str, Any]], None]
    
    # 错误处理器
    ErrorHandler = Callable[[Exception, Optional[str]], bool]
    
    # 数据转换器
    DataTransformer = Callable[[Any], Any]
    
    # 验证器
    Validator = Callable[[Any], bool]
    
    # 带回调的函数
    def event_emitter(
        event_name: str,
        data: Dict[str, Any],
        handlers: List[EventHandler]
    ) -> None:
        """事件发射器"""
        for handler in handlers:
            handler(data)
    
    def data_pipeline(
        data: List[Any],
        transformers: List[DataTransformer],
        validator: Optional[Validator] = None
    ) -> List[Any]:
        """数据处理管道"""
        result = data
        for transformer in transformers:
            result = [transformer(item) for item in result]
        
        if validator:
            result = [item for item in result if validator(item)]
        
        return result
    
    def error_boundary(
        operation: Callable[[], Any],
        on_error: ErrorHandler
    ) -> Any:
        """错误边界"""
        try:
            return operation()
        except Exception as e:
            if on_error(e, "Operation failed"):
                return None
            else:
                raise
    
    # 转换回调模式
    convert_to_ts(event_emitter)
    convert_to_ts(data_pipeline)
    convert_to_ts(error_boundary)
    
    res = get_output_ts_str(None)
    print("回调模式转换完成")
    print(res)
    reset_store()


def utility_functions_demo():
    """工具函数转换演示"""
    print("\n=== 工具函数转换演示 ===")
    
    # 工具函数集合
    def format_date(date_str: str, format: str = "YYYY-MM-DD") -> str:
        """日期格式化"""
        return date_str
    
    def validate_email(email: str) -> bool:
        """邮箱验证"""
        return "@" in email
    
    def generate_id(prefix: str = "id_") -> str:
        """生成ID"""
        return f"{prefix}123456"
    
    def deep_copy(obj: Any) -> Any:
        """深拷贝"""
        return obj
    
    def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
        """合并字典"""
        result = {}
        for d in dicts:
            result.update(d)
        return result
    
    # 转换工具函数
    convert_to_ts(format_date)
    convert_to_ts(validate_email)
    convert_to_ts(generate_id)
    convert_to_ts(deep_copy)
    convert_to_ts(merge_dicts)
    
    res = get_output_ts_str(None)
    print("工具函数转换完成")
    print(res)
    reset_store()



if __name__ == "__main__":
    """运行所有演示"""
    function_signatures_demo()
    class_structures_demo()
    method_signatures_demo()
    callback_patterns_demo()
    utility_functions_demo()
    
    print("\n=== 函数和类转换演示完成 ===")