"""
SQLModel 类型转换示例
展示 py-ts 对 SQLModel 类型的 TypeScript 转换支持
"""

from datetime import datetime
from typing import Optional, List
from pytots import convert_to_ts, get_output_ts_str, reset_store

# 插件注册
from pytots.plugin import use_plugin
from pytots.plugin.plus.sqlmodel_plugin import SqlModelPlugin

use_plugin(SqlModelPlugin())

import os
current_dir = os.path.dirname(os.path.abspath(__file__))

def sqlmodel_types_demo():
    """SQLModel 类型转换演示"""
    print("=== SQLModel 类型转换演示 ===")

    # 导入 SQLModel 类型
    from sqlmodel import SQLModel, Field

    # 定义 SQLModel 模型
    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        email: str = Field(unique=True)
        age: Optional[int] = None
        is_active: bool = Field(default=True)

    print("\n1. SQLModel 基础模型转换:")
    print(f"User 模型 -> {convert_to_ts(User)}")

    # SQLModel 字段类型
    print("\n2. SQLModel 字段类型:")
    print(f"AutoString -> {convert_to_ts(str)}")  # string
    print(f"BigInteger -> {convert_to_ts(int)}")  # number
    print(f"Boolean -> {convert_to_ts(bool)}")  # boolean

    # 复杂 SQLModel 类型
    class Product(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        price: float
        description: Optional[str] = None
        in_stock: bool = Field(default=True)
        category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    print("\n3. 复杂 SQLModel 模型:")
    print(f"Product 模型 -> {convert_to_ts(Product)}")

    # 关系模型
    class Category(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(unique=True)
        description: Optional[str] = None

    class Order(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: int = Field(foreign_key="user.id")
        product_id: int = Field(foreign_key="product.id")
        quantity: int = Field(default=1, ge=1)
        total_price: float

    print("\n4. 关系模型:")
    print(f"Category 模型 -> {convert_to_ts(Category)}")
    print(f"Order 模型 -> {convert_to_ts(Order)}")
    res = get_output_ts_str()
    print(res)
    reset_store()


def advanced_sqlmodel_demo():
    """高级 SQLModel 功能演示"""
    print("\n=== 高级 SQLModel 功能演示 ===")

    from sqlmodel import SQLModel, Field, Relationship
    from typing import Optional

    # 一对多关系
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        headquarters: str

        # 关系字段
        heroes: List["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        secret_name: str
        age: Optional[int] = None

        # 外键关系
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

    print("\n1. 一对多关系模型:")
    print(f"Team 模型 -> {convert_to_ts(Team)}")
    print(f"Hero 模型 -> {convert_to_ts(Hero)}")

    # 多对多关系
    class HeroPowerLink(SQLModel, table=True):
        hero_id: int = Field(foreign_key="hero.id", primary_key=True)
        power_id: int = Field(foreign_key="power.id", primary_key=True)
        level: int = Field(default=1, ge=1, le=10)

    class Power(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(unique=True)
        description: str

        # 多对多关系
        heroes: List[Hero] = Relationship(
            back_populates="powers", link_model=HeroPowerLink
        )

    # 更新 Hero 模型添加多对多关系
    class HeroWithPowers(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        secret_name: str
        age: Optional[int] = None
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        powers: List[Power] = Relationship(
            back_populates="heroes", link_model=HeroPowerLink
        )

    print("\n2. 多对多关系模型:")
    print(f"Power 模型 -> {convert_to_ts(Power)}")
    print(f"HeroWithPowers 模型 -> {convert_to_ts(HeroWithPowers)}")

    # 继承模型
    class SuperHero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        secret_name: str
        age: Optional[int] = None
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        super_power: str
        weakness: Optional[str] = None

    print("\n3. 继承模型:")
    print(f"SuperHero 模型 -> {convert_to_ts(SuperHero)}")

    res = get_output_ts_str()
    print(res)
    reset_store()


def generate_sqlmodel_ts_file():
    """生成 SQLModel TypeScript 接口文件"""
    print("\n=== 生成 SQLModel TypeScript 接口文件 ===")

    from sqlmodel import SQLModel, Field
    from typing import Optional

    # 定义 SQLModel 模型（使用不同的表名避免冲突）
    class AppUser(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        username: str = Field(unique=True, index=True)
        email: str = Field(unique=True)
        age: Optional[int] = Field(default=None, ge=0, le=150)
        is_active: bool = Field(default=True)
        created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class AppProduct(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        description: str
        price: float = Field(ge=0)
        stock: int = Field(default=0, ge=0)
        category: str = Field(default="general")

    convert_to_ts(AppUser)
    convert_to_ts(AppProduct)

    res = get_output_ts_str()
    print(res)
    reset_store()


if __name__ == "__main__":
    """运行 SQLModel 演示"""
    sqlmodel_types_demo()
    advanced_sqlmodel_demo()
    generate_sqlmodel_ts_file()

    print("\n=== SQLModel 演示完成 ===")
