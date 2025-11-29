"""
TypeScript 格式化输出模块

提供 TypeScript 代码的格式化功能，包括缩进、换行、注释等格式化选项。
支持与 pytots 转换器集成，提供自动格式化的 TypeScript 输出。
"""



class TypeScriptFormatter:
    def __init__(self, indent_size=4):
        self.indent_char = " "
        self.indent_size = indent_size
        
        # 核心状态
        self.indent_level = 0
        self.paren_level = 0        # 追踪 () 深度，用于 for 循环保护
        self.quote_char = None      # 当前是否在字符串中: None, ', ", `
        self.in_line_comment = False
        self.in_block_comment = False
        
        # 缓冲区管理
        self.result = []            # 最终结果列表
        self.whitespace_buffer = [] # 暂存遇到的空格/换行
        
        # 标记是否需要换行
        self.wants_newline = False  
        
        # 上一个写入的有效字符（非空格），用于判断上下文（如正则 vs 除号）
        self.last_token = '' 

    def format(self, code: str) -> str:
        self.result = []
        i = 0
        n = len(code)
        
        while i < n:
            char = code[i]
            next_char = code[i+1] if i + 1 < n else ''
            
            # -------------------------------------------------
            # 1. 优先处理：特殊状态（字符串、注释）
            # -------------------------------------------------
            
            # A. 处理字符串内容 (忽略字符串内的 {} ; 等)
            if self.quote_char:
                if char == '\\': # 转义字符，连同下一个字符一起吞掉
                    self._emit(char)
                    if next_char:
                        self._emit(next_char)
                        i += 1
                else:
                    self._emit(char)
                    if char == self.quote_char: # 字符串结束
                        self.quote_char = None
                i += 1
                continue
                
            # B. 处理行注释 // ...
            if self.in_line_comment:
                if char == '\n':
                    self.in_line_comment = False
                    self.wants_newline = True # 注释结束必须换行
                else:
                    self._emit(char)
                i += 1
                continue
                
            # C. 处理块注释 /* ... */
            if self.in_block_comment:
                self._emit(char)
                if char == '*' and next_char == '/':
                    self._emit('/')
                    self.in_block_comment = False
                    self.wants_newline = True # 块注释结束后通常换行
                    i += 1
                i += 1
                continue

            # -------------------------------------------------
            # 2. 检测状态进入
            # -------------------------------------------------
            
            # 进入行注释
            if char == '/' and next_char == '/':
                self._flush_whitespace_as_space() # 注释前加个空格
                self._emit("//")
                self.in_line_comment = True
                i += 2
                continue
                
            # 进入块注释
            if char == '/' and next_char == '*':
                if self.wants_newline: # 如果之前要求换行，先执行
                     self._flush_newline()
                else:
                     self._flush_whitespace_as_space()
                self._emit("/*")
                self.in_block_comment = True
                i += 2
                continue
            
            # 进入字符串
            if char in ["'", '"', '`']:
                self._emit(char)
                self.quote_char = char
                i += 1
                continue

            # -------------------------------------------------
            # 3. 处理代码逻辑结构 (层级缩进的核心)
            # -------------------------------------------------
            
            # 忽略输入源中的原始空白（我们自己接管格式）
            if char.isspace():
                # 只是暂存，如果后面跟着有效字符，根据逻辑决定变成空格还是忽略
                self.whitespace_buffer.append(char)
                i += 1
                continue

            # --- 遇到有效字符了 ---
            
            # 左大括号 {: 开启新层级
            if char == '{':
                self._flush_whitespace_as_space() # { 前面补一个空格
                self._emit('{')
                self.indent_level += 1
                self.wants_newline = True # { 后面必须换行
                i += 1
                continue
                
            # 右大括号 }: 关闭层级
            if char == '}':
                # 回退缩进
                self.indent_level = max(0, self.indent_level - 1)
                self.wants_newline = True # } 必须另起一行
                # 立即强制执行换行（确保 } 独占一行）
                self._flush_newline() 
                self._emit('}')
                
                # } 后面通常也要换行，除非后面跟着 else, catch, ;
                # 这里为了简单，先标记换行，如果下一个词是 else，可以特殊处理消除换行
                self.wants_newline = True 
                i += 1
                continue

            # 分号 ;: 语句结束
            if char == ';':
                self._emit(';')
                # 在 for 循环 (..) 内部，分号不换行
                if self.paren_level == 0:
                    self.wants_newline = True
                else:
                    self._emit(' ') # for循环内分号后加空格
                i += 1
                continue
                
            # 左小括号 (:
            if char == '(':
                # if( -> if (
                if self.last_token_is_keyword_or_ident():
                     self._flush_whitespace_as_space()
                self._emit('(')
                self.paren_level += 1
                i += 1
                continue
            
            # 右小括号 ):
            if char == ')':
                self._emit(')')
                self.paren_level = max(0, self.paren_level - 1)
                i += 1
                continue

            # 逗号 ,:
            if char == ',':
                self._emit(',')
                self._emit(' ') # 逗号后强制加空格
                i += 1
                continue

            # 操作符处理 (简单处理，前后加空格)
            # 这里仅作示例，处理 = ? : 等符号
            if char in ['=', '?', ':', '+', '-', '*', '%'] and not self.paren_level:
                # 排除 ++, --, ==, => 等双字符情况的干扰（简化版未完美处理，但够用）
                is_double = (next_char == char or next_char == '=' or (char == '=' and next_char == '>'))
                
                if not is_double:
                    # 确保操作符两边有空格
                    if self.result and self.result[-1] != ' ':
                        self._emit(' ')
                    self._emit(char)
                    # 暂时不强制加后置空格，依赖下一次循环的 isspace 判定或 _flush_whitespace
                    self.whitespace_buffer.append(' ') 
                else:
                    self._emit(char)
                i += 1
                continue

            # -------------------------------------------------
            # 4. 普通字符 (变量名, 关键字, 数字)
            # -------------------------------------------------
            
            # 如果之前有标记需要换行，现在执行
            if self.wants_newline:
                self._flush_newline()
            elif self.whitespace_buffer:
                # 如果没换行，但原代码有空格，保留一个空格
                self._emit(' ')
                self.whitespace_buffer = []

            self._emit(char)
            i += 1
        
        return "".join(self.result)

    # --- 辅助方法 ---

    def _emit(self, text):
        """写入文本到结果，同时清空空白缓冲区"""
        self.result.append(text)
        self.whitespace_buffer = [] # 缓冲区已消费
        if text.strip():
            self.last_token = text

    def _flush_newline(self):
        """执行换行动作：写入 \n + 当前缩进"""
        # 避免连续空行
        if self.result and self.result[-1].strip() == '':
            # 如果最后一行全是空白，去掉它
            while self.result and self.result[-1].strip() == '':
                self.result.pop()
            # 如果已经是换行符，不要重复
            if self.result and self.result[-1].endswith('\n'):
                pass
            else:
                self.result.append('\n')
        else:
             self.result.append('\n')
        
        # 写入缩进
        indent_str = (self.indent_char * self.indent_size) * self.indent_level
        self.result.append(indent_str)
        
        self.wants_newline = False
        self.whitespace_buffer = [] # 换行意味着之前的空格都无效了

    def _flush_whitespace_as_space(self):
        """将暂存的空白变成一个普通空格"""
        if self.result and self.result[-1] != ' ' and self.result[-1] != '\n':
            self.result.append(' ')
        self.whitespace_buffer = []

    def last_token_is_keyword_or_ident(self):
        """简单判断上一个字符是不是字母（用于 if( 变 if (）"""
        if not self.result: return False
        c = self.result[-1]
        return c.isalnum() or c == '_'

# --- 运行测试 ---
if __name__ == "__main__":
    # 极度混乱的代码：包含嵌套对象、数组、函数、For循环、乱七八糟的缩进
    ugly_ts = """
    interface Config{host:string;port:number}
    const startServer  =  (  config : Config ) => {
    if(config.port>8000){
    console.log("Starting...");
    const server={status:"active", data:[1,2,{id:3,val:"text"}]};
    for(let i=0; i<10; i++){console.log(i);}
    }else{
    throw new Error( "Port blocked" );
    }
    return true;
    }
    """
    
    formatter = TypeScriptFormatter(indent_size=4)
    formatted = formatter.format(ugly_ts)
    
    print("====== 原始代码 ======")
    print(ugly_ts)
    print("\n====== 格式化结果 ======")
    print(formatted)