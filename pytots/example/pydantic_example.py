"""
Pydantic 类型转换示例
展示 py-ts 对 Pydantic 类型的 TypeScript 转换支持
"""

from typing import Optional, List, Dict, Any
from pytots import convert_to_ts, get_output_ts_str


# 插件注册
from pytots.plugin import use_plugin
from pytots.plugin.plus.pydantic_plugin import PydanticPlugin

use_plugin(PydanticPlugin())





def pydantic_types_demo():
    """Pydantic 类型转换演示"""
    print("=== Pydantic 类型转换演示 ===")
    
    # 导入 Pydantic 类型
    from pydantic import BaseModel, HttpUrl, IPvAnyAddress
    
    # 定义 Pydantic 模型
    class User(BaseModel):
        id: int
        name: str
        email: str
        age: Optional[int] = None
        website: Optional[HttpUrl] = None
        ip_address: Optional[IPvAnyAddress] = None
        tags: List[str] = []
        metadata: Dict[str, Any] = {}
    
    print("\n1. Pydantic BaseModel 转换:")
    print(f"User 模型 -> {convert_to_ts(User)}")
    
    # Pydantic 字段类型
    print("\n2. Pydantic 字段类型:")
    print(f"HttpUrl -> {convert_to_ts(HttpUrl)}")          # string
    print(f"IPvAnyAddress -> {convert_to_ts(IPvAnyAddress)}") # string
    
    # 复杂 Pydantic 类型
    class Product(BaseModel):
        id: int
        name: str
        price: float
        in_stock: bool
        categories: List[str]
        attributes: Dict[str, Any]
        owner: Optional[User] = None
        
    print("\n3. 复杂 Pydantic 模型:")
    print(f"Product 模型 -> {convert_to_ts(Product)}")
    
    # 嵌套 Pydantic 模型
    class Order(BaseModel):
        id: int
        user: User
        products: List[Product]
        total_price: float
        status: str
        
    print("\n4. 嵌套 Pydantic 模型:")
    print(f"Order 模型 -> {convert_to_ts(Order)}")


def advanced_pydantic_demo():
    """高级 Pydantic 功能演示"""
    print("\n=== 高级 Pydantic 功能演示 ===")
    
    from pydantic import BaseModel, Field
    from typing import Union
    
    # 使用 Field 的模型
    class AdvancedUser(BaseModel):
        id: int = Field(..., description="用户ID")
        username: str = Field(..., min_length=3, max_length=50)
        email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
        score: float = Field(default=0.0, ge=0.0, le=100.0)
        is_active: bool = Field(default=True)
        
    print("\n1. 使用 Field 的 Pydantic 模型:")
    print(f"AdvancedUser 模型 -> {convert_to_ts(AdvancedUser)}")
    
    # 联合类型与 Pydantic
    class Animal(BaseModel):
        name: str
        species: str
        
    class Plant(BaseModel):
        name: str
        type: str
        
    class Organism(BaseModel):
        entity: Union[Animal, Plant]
        
    print("\n2. 联合类型的 Pydantic 模型:")
    print(f"Organism 模型 -> {convert_to_ts(Organism)}")


def generate_pydantic_ts_file():
    """生成 Pydantic 类型的 TypeScript 文件"""
    from pydantic import BaseModel, HttpUrl, Field
    from typing import Optional, List, Dict
    
    # 定义 Pydantic 模型
    class BaseUser(BaseModel):
        id: int
        name: str
        email: str
        age: Optional[int] = None
        website: Optional[HttpUrl] = None
        
    class Member(BaseUser):
        group: str
        org_name: str | None = Field(default=None, description="组织名称",exclude=True)
    
    print(convert_to_ts(Member))
    # 生成 TypeScript 接口定义
    ts_content = get_output_ts_str()
    
    print("\n生成的 TypeScript 内容:")
    print(ts_content)
    


if __name__ == "__main__":
    """运行 Pydantic 演示"""
    pydantic_types_demo()
    advanced_pydantic_demo()
    generate_pydantic_ts_file()
    
    print("\n=== Pydantic 演示完成 ===")