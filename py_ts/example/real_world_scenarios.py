"""
实际应用场景示例
展示py-ts在真实项目中的使用，包括API类型定义、数据库模型、前端类型等
"""

from typing import TypedDict, NewType, Optional, List, Dict, Any, Union, Callable
from dataclasses import dataclass
from datetime import datetime
from py_ts import convert_to_ts, get_output_ts_str, output_ts_file


def api_client_scenario():
    """API客户端场景 - 完整的API类型定义"""
    print("=== API客户端场景 ===")
    
    # API基础类型
    ApiKey = NewType("ApiKey", str)
    UserId = NewType("UserId", int)
    Timestamp = NewType("Timestamp", int)
    
    # API请求/响应类型
    class ApiRequest(TypedDict):
        """API请求基础类型"""
        method: str  # GET, POST, PUT, DELETE
        endpoint: str
        headers: Dict[str, str]
        data: Optional[Dict[str, Any]]
        params: Optional[Dict[str, Any]]
    
    class ApiResponse(TypedDict):
        """API响应基础类型"""
        success: bool
        status_code: int
        data: Optional[Any]
        error: Optional[str]
        timestamp: Timestamp
    
    # 用户相关类型
    class User(TypedDict):
        """用户信息"""
        id: UserId
        username: str
        email: str
        first_name: str
        last_name: str
        avatar: Optional[str]
        is_active: bool
        created_at: Timestamp
        updated_at: Timestamp
    
    class CreateUserRequest(TypedDict):
        """创建用户请求"""
        username: str
        email: str
        password: str
        first_name: str
        last_name: str
    
    class UpdateUserRequest(TypedDict):
        """更新用户请求"""
        username: Optional[str]
        email: Optional[str]
        first_name: Optional[str]
        last_name: Optional[str]
        avatar: Optional[str]
    
    # API函数
    def authenticate(api_key: ApiKey) -> ApiResponse:
        """认证函数"""
        return {
            "success": True,
            "status_code": 200,
            "data": {"token": "abc123"},
            "error": None,
            "timestamp": 1234567890
        }
    
    def get_user(user_id: UserId) -> ApiResponse:
        """获取用户函数"""
        return {
            "success": True,
            "status_code": 200,
            "data": {"id": user_id, "username": "john_doe"},
            "error": None,
            "timestamp": 1234567890
        }
    
    def create_user(user_data: CreateUserRequest) -> ApiResponse:
        """创建用户函数"""
        return {
            "success": True,
            "status_code": 201,
            "data": {"id": 1, **user_data},
            "error": None,
            "timestamp": 1234567890
        }
    
    # 转换API类型
    convert_to_ts(ApiKey)
    convert_to_ts(UserId)
    convert_to_ts(Timestamp)
    convert_to_ts(ApiRequest)
    convert_to_ts(ApiResponse)
    convert_to_ts(User)
    convert_to_ts(CreateUserRequest)
    convert_to_ts(UpdateUserRequest)
    convert_to_ts(authenticate)
    convert_to_ts(get_user)
    convert_to_ts(create_user)
    
    print("API客户端类型转换完成")


def database_models_scenario():
    """数据库模型场景 - 数据库表结构定义"""
    print("\n=== 数据库模型场景 ===")
    
    @dataclass
    class BaseModel:
        """基础模型"""
        id: int
        created_at: str
        updated_at: str
    
    @dataclass
    class UserModel(BaseModel):
        """用户模型"""
        username: str
        email: str
        password_hash: str
        is_active: bool
        last_login: Optional[str]
        profile_data: Dict[str, Any]
    
    @dataclass
    class PostModel(BaseModel):
        """文章模型"""
        title: str
        content: str
        author_id: int
        category: str
        tags: List[str]
        is_published: bool
        published_at: Optional[str]
        view_count: int
        like_count: int
    
    @dataclass
    class CommentModel(BaseModel):
        """评论模型"""
        post_id: int
        user_id: int
        content: str
        parent_id: Optional[int]  # 父评论ID，支持嵌套评论
        is_approved: bool
    
    @dataclass
    class CategoryModel(BaseModel):
        """分类模型"""
        name: str
        slug: str
        description: Optional[str]
        parent_id: Optional[int]  # 父分类ID，支持分类层级
        sort_order: int
    
    # 转换数据库模型
    convert_to_ts(BaseModel)
    convert_to_ts(UserModel)
    convert_to_ts(PostModel)
    convert_to_ts(CommentModel)
    convert_to_ts(CategoryModel)
    
    print("数据库模型类型转换完成")


def frontend_types_scenario():
    """前端类型场景 - React/Vue组件props和状态类型"""
    print("\n=== 前端类型场景 ===")
    
    # React组件Props类型
    class ButtonProps(TypedDict):
        """按钮组件Props"""
        text: str
        onClick: Callable[[], None]
        variant: str  # "primary", "secondary", "danger"
        size: str     # "small", "medium", "large"
        disabled: bool
        loading: bool
        className: Optional[str]
    
    class UserCardProps(TypedDict):
        """用户卡片组件Props"""
        user: User
        showEmail: bool
        showActions: bool
        onEdit: Callable[[UserId], None]
        onDelete: Callable[[UserId], None]
        className: Optional[str]
    
    class PaginationProps(TypedDict):
        """分页组件Props"""
        currentPage: int
        totalPages: int
        onPageChange: Callable[[int], None]
        showSizeChanger: bool
        pageSize: int
        onSizeChange: Optional[Callable[[int], None]]
    
    # 前端状态类型
    class AppState(TypedDict):
        """应用状态"""
        user: Optional[User]
        isLoading: bool
        error: Optional[str]
        theme: str  # "light", "dark"
        language: str
    
    class UserListState(TypedDict):
        """用户列表状态"""
        users: List[User]
        loading: bool
        error: Optional[str]
        searchQuery: str
        currentPage: int
        totalCount: int
        selectedUsers: List[UserId]
    
    # 事件处理器类型
    EventHandler = Callable[[Dict[str, Any]], None]
    FormSubmitHandler = Callable[[Dict[str, Any]], bool]
    
    # 转换前端类型
    convert_to_ts(ButtonProps)
    convert_to_ts(UserCardProps)
    convert_to_ts(PaginationProps)
    convert_to_ts(AppState)
    convert_to_ts(UserListState)
    
    print("前端类型转换完成")


def ecommerce_scenario():
    """电商场景 - 电商平台类型定义"""
    print("\n=== 电商场景 ===")
    
    # 电商基础类型
    ProductId = NewType("ProductId", int)
    OrderId = NewType("OrderId", int)
    Price = NewType("Price", float)
    
    # 商品相关类型
    class Product(TypedDict):
        """商品信息"""
        id: ProductId
        name: str
        description: str
        price: Price
        original_price: Price
        stock: int
        images: List[str]
        category: str
        tags: List[str]
        is_available: bool
        rating: float
        review_count: int
        created_at: str
    
    class ProductVariant(TypedDict):
        """商品变体"""
        id: int
        product_id: ProductId
        sku: str
        price: Price
        stock: int
        attributes: Dict[str, str]  # {"color": "red", "size": "M"}
    
    # 购物车相关类型
    class CartItem(TypedDict):
        """购物车项"""
        product_id: ProductId
        variant_id: Optional[int]
        quantity: int
        price: Price
    
    class ShoppingCart(TypedDict):
        """购物车"""
        items: List[CartItem]
        total_price: Price
        item_count: int
    
    # 订单相关类型
    class Order(TypedDict):
        """订单信息"""
        id: OrderId
        user_id: int
        items: List[CartItem]
        total_price: Price
        status: str  # "pending", "paid", "shipped", "delivered", "cancelled"
        shipping_address: Dict[str, Any]
        payment_method: str
        created_at: str
        updated_at: str
    
    # 电商函数
    def add_to_cart(product_id: ProductId, quantity: int = 1) -> bool:
        """添加到购物车"""
        return True
    
    def checkout(cart: ShoppingCart, payment_info: Dict[str, Any]) -> OrderId:
        """结账"""
        return OrderId(123)
    
    def get_product_recommendations(product_id: ProductId) -> List[Product]:
        """获取商品推荐"""
        return []
    
    # 转换电商类型
    convert_to_ts(ProductId)
    convert_to_ts(OrderId)
    convert_to_ts(Price)
    convert_to_ts(Product)
    convert_to_ts(ProductVariant)
    convert_to_ts(CartItem)
    convert_to_ts(ShoppingCart)
    convert_to_ts(Order)
    convert_to_ts(add_to_cart)
    convert_to_ts(checkout)
    convert_to_ts(get_product_recommendations)
    
    print("电商类型转换完成")


def configuration_scenario():
    """配置管理场景 - 应用配置类型定义"""
    print("\n=== 配置管理场景 ===")
    
    # 应用配置类型
    class DatabaseConfig(TypedDict):
        """数据库配置"""
        host: str
        port: int
        username: str
        password: str
        database: str
        pool_size: int
        timeout: int
    
    class RedisConfig(TypedDict):
        """Redis配置"""
        host: str
        port: int
        password: Optional[str]
        db: int
        key_prefix: str
    
    class EmailConfig(TypedDict):
        """邮件配置"""
        smtp_host: str
        smtp_port: int
        username: str
        password: str
        from_email: str
        use_tls: bool
    
    class LoggingConfig(TypedDict):
        """日志配置"""
        level: str  # "DEBUG", "INFO", "WARNING", "ERROR"
        format: str
        file_path: Optional[str]
        max_size: int  # MB
        backup_count: int
    
    class AppConfig(TypedDict):
        """应用配置"""
        debug: bool
        secret_key: str
        allowed_hosts: List[str]
        database: DatabaseConfig
        redis: RedisConfig
        email: EmailConfig
        logging: LoggingConfig
    
    # 配置验证函数
    def validate_config(config: AppConfig) -> bool:
        """验证配置"""
        return True
    
    def load_config(file_path: str) -> AppConfig:
        """加载配置"""
        return {
            "debug": True,
            "secret_key": "secret",
            "allowed_hosts": ["localhost"],
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "user",
                "password": "pass",
                "database": "app",
                "pool_size": 10,
                "timeout": 30
            },
            "redis": {
                "host": "localhost",
                "port": 6379,
                "password": None,
                "db": 0,
                "key_prefix": "app:"
            },
            "email": {
                "smtp_host": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "user@gmail.com",
                "password": "pass",
                "from_email": "noreply@example.com",
                "use_tls": True
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file_path": "/var/log/app.log",
                "max_size": 100,
                "backup_count": 5
            }
        }
    
    # 转换配置类型
    convert_to_ts(DatabaseConfig)
    convert_to_ts(RedisConfig)
    convert_to_ts(EmailConfig)
    convert_to_ts(LoggingConfig)
    convert_to_ts(AppConfig)
    convert_to_ts(validate_config)
    convert_to_ts(load_config)
    
    print("配置管理类型转换完成")


def output_real_world_scenarios():
    """输出实际应用场景转换结果"""
    print("\n=== 输出结果 ===")
    
    # 获取所有转换结果
    ts_code = get_output_ts_str("RealWorldScenarios")
    print("生成的TypeScript代码:")
    print(ts_code)
    
    # 输出到文件
    output_ts_file("real_world_scenarios.ts", "RealWorldScenarios")
    print("\nTypeScript代码已保存到: real_world_scenarios.ts")


if __name__ == "__main__":
    """运行所有场景演示"""
    api_client_scenario()
    database_models_scenario()
    frontend_types_scenario()
    ecommerce_scenario()
    configuration_scenario()
    output_real_world_scenarios()
    
    print("\n=== 实际应用场景演示完成 ===")
    print("请查看生成的文件: real_world_scenarios.ts")
    print("\n这个文件包含了:")
    print("1. API客户端类型定义")
    print("2. 数据库模型类型定义")
    print("3. 前端组件Props和状态类型")
    print("4. 电商平台类型定义")
    print("5. 配置管理类型定义")