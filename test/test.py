from dataclasses import dataclass
from pytots import convert_to_ts,get_output_ts_str
from typing import Optional, List, Dict, Any, get_origin
from typing import TypedDict,Generic,TypeVar

T = TypeVar("T", bound='TicketType')
U = TypeVar("U")

@dataclass
class QueryResult(Generic[T]):
    """查询结果基类"""
    data: list[T]
    # total_count: int

class TicketType(TypedDict):
    """工单类型"""
    id: int
    # name: str
    # description: str
    
@dataclass
class TicketTypeQueryResult(QueryResult[TicketType]):
    """工单查询结果"""
    goods: List[TicketType]

# print("QueryResult",hasattr(QueryResult, "__orig_bases__"))
# print("TicketTypeQueryResult",hasattr(TicketTypeQueryResult, "__orig_bases__"))
# print("TicketType",hasattr(TicketType, "__orig_bases__"))
# print("QueryResult[TicketType]",hasattr(QueryResult[TicketType], "__orig_bases__"),	isinstance(QueryResult[TicketType], type))

# TicketTypeQueryResult = QueryResult[TicketType]
# print(convert_to_ts(Generic[T,U]))

# print(convert_to_ts(QueryResult))
# print(convert_to_ts(QueryResult[TicketType]))
# print(get_output_ts_str(None))
print(convert_to_ts(TicketTypeQueryResult))
print(get_output_ts_str(None,True))