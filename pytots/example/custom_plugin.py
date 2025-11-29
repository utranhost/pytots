from typing import Generic,TypeVar

T = TypeVar("T")

class MyUser:
    id: int
    name: str

class MyAdmin(MyUser):
    role: str

class MyTicket(Generic[T]):
    id: int
    name: str
    description: str|None
    exc: T|None


class MyTicketAdmin(MyTicket[MyAdmin]):
    pass

    
from pytots import Plugin
from pytots.plugin.tools import generic_feild_fill,assemble_interface_type
from typing import get_type_hints
from pytots.plugin.inner import DataclassPlugin


class MyCustomPlugin(Plugin):
    
    name = "MyCustomPlugin"
    type_prefix = "interface"
    
    def is_supported(self, python_type) -> bool:
        return python_type in [MyUser,MyTicket,MyAdmin,MyTicketAdmin]

    def converter(self, python_type, **extra) -> str:
        class_name = python_type.__name__
        
        fields = []
        for field, field_type in get_type_hints(python_type).items():
            ts_type = generic_feild_fill(self,field_type)
            
            # 过滤掉id字段
            if field == "id":
                continue
            
            # 处理可选字段
            if "undefined" in ts_type:
                fields.append(f"{field}?: {ts_type};")
            else:
                fields.append(f"{field}: {ts_type};")

        fields_str = "\n  ".join(fields)
        
        return assemble_interface_type(self, class_name, fields_str)


# class MyCustomPlugin(DataclassPlugin):
#     name = "MyCustomPlugin"
#     type_prefix = "interface"

#     def is_supported(self, python_type) -> bool:
#         return python_type in [MyUser,MyTicket,MyAdmin,MyTicketAdmin]



from pytots import convert_to_ts,use_plugin,get_output_ts_str

use_plugin(MyCustomPlugin())

# print(convert_to_ts(MyUser))
# print(convert_to_ts(MyTicket))
print(convert_to_ts(MyTicketAdmin))
print(get_output_ts_str(None,True))