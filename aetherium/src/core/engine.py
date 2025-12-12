import re
from typing import List, Any, Dict
from src.core.interfaces import TokenModule, SyntaxModule
from src.core.context import Context, ExecutionError

class Token:
    def __init__(self, type_id: str, value: Any, line: int, col: int):
        self.type_id = type_id
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type_id}, '{self.value}')"

class Engine:
    def __init__(self, registry):
        self.registry = registry
        self.context = Context()

    def tokenize(self, source_code: str) -> List[Token]:
        tokens = []
        pos = 0
        line = 1
        col = 1
        
        # Sort tokens by priority (descending)
        sorted_tokens = sorted(self.registry.tokens.values(), key=lambda t: t.PRIORITY, reverse=True)
        
        while pos < len(source_code):
            match = None
            matched_module = None
            
            # Skip whitespace
            if source_code[pos].isspace():
                if source_code[pos] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                pos += 1
                continue
            
            # Skip comments // ...
            if source_code.startswith("//", pos):
                while pos < len(source_code) and source_code[pos] != '\n':
                    pos += 1
                continue

            for token_module in sorted_tokens:
                regex = re.compile(token_module.REGEX)
                m = regex.match(source_code, pos)
                if m:
                    match = m
                    matched_module = token_module
                    break
            
            if match:
                value = match.group(0)
                # Allow token module to process the value (e.g., strip quotes)
                token_data = matched_module.create_instance(value, line, col)
                # If create_instance returns None, it might be a skip token (though we handle whitespace manually)
                if token_data:
                    tokens.append(Token(token_data['type'], token_data['value'], line, col))
                
                # Update position
                consumed = len(value)
                pos += consumed
                col += consumed
            else:
                raise ExecutionError(f"Unexpected character at line {line}, col {col}: '{source_code[pos]}'")
        
        return tokens

    def execute(self, tokens: List[Token]):
        index = 0
        while index < len(tokens):
            token = tokens[index]
            
            # Look up syntax handler
            if token.type_id in self.registry.syntax_map:
                handler = self.registry.syntax_map[token.type_id]
                try:
                    index = handler.evaluate(self.context, tokens, index)
                except ExecutionError as e:
                    print(f"Runtime Error: {e}")
                    return
            else:
                # If no specific handler, maybe it's an expression or unexpected
                # For now, we assume top-level statements start with keywords handled by syntax modules
                print(f"Error: Unexpected token at top level: {token}")
                index += 1
