from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError

class StructureSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_STRUCTURE'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_STRUCTURE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Structure Name { Type Member; ... }
        
        idx = index + 1
        if idx >= len(tokens):
             raise ExecutionError("Expected Structure Name")
        
        # Allow Identifier or Report as name
        if tokens[idx].type_id == 'TOKEN_IDENTIFIER' or tokens[idx].type_id == 'TOKEN_REPORT':
            struct_name = tokens[idx].value
        else:
            raise ExecutionError(f"Expected Structure Name, got {tokens[idx].type_id}")
        idx += 1
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
            raise ExecutionError("Expected '{'")
        idx += 1
        
        members = []
        while idx < len(tokens) and tokens[idx].type_id != 'TOKEN_RBRACE':
            # Type Name;
            m_type = tokens[idx].value
            idx += 1
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
                 raise ExecutionError("Expected Member Name")
            m_name = tokens[idx].value
            idx += 1
            
            # Handle Array Dimension [N]
            if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_LBRACKET':
                idx += 1 # [
                if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_NUMBER':
                     raise ExecutionError("Expected array size")
                idx += 1 # Size
                if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_RBRACKET':
                     raise ExecutionError("Expected ']'")
                idx += 1 # ]
            
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
                 raise ExecutionError("Expected ';'")
            idx += 1
            
            members.append((m_name, m_type))
            
        idx += 1 # Skip }
        
        # Semicolon optional after struct def? Usually yes in C, maybe not in Rust.
        # Example B: Structure Power_Reading { ... } (No semi shown in snippet, but standard C has it)
        # I will optional check.
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_SEMI':
            idx += 1
            
        struct_def = {
            'name': struct_name,
            'members': members
        }
        
        context.declare_structure(struct_name, struct_def)
        
        return idx
