from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError

class StockpileSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_STOCKPILE'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_STOCKPILE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Stockpile <Type> <Name> [= <Value>];
        # index points to Stockpile
        
        idx = index + 1
        
        # 1. Type
        if idx >= len(tokens): raise ExecutionError("Expected Type after Stockpile")
        # Type can be TypeGauge, TypeManometer, or Identifier (Structure Name)
        type_token = tokens[idx]
        type_name = type_token.value
        # Check if type is valid (builtin or struct)
        # For simplicity, we assume if it's a keyword or identifier it's a type name.
        idx += 1
        
        # 2. Name
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Variable Name")
        var_name = tokens[idx].value
        idx += 1
        
        # Handle Array Dimension [N] (Ignore for now in terms of logic, but consume tokens)
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_LBRACKET':
            idx += 1 # [
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_NUMBER':
                 raise ExecutionError("Expected array size")
            idx += 1 # Size
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_RBRACKET':
                 raise ExecutionError("Expected ']'")
            idx += 1 # ]
        
        # Declare
        # Check for Structure instantiation (implicit or explicit)
        # If type is a structure, we might need to initialize fields to None or default.
        context.declare_variable(var_name, type_name)
        
        # 3. Optional Assignment
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_ASSIGN':
            idx += 1
            # Evaluate expression
            from src.core.expression import evaluate_expression
            val, idx = evaluate_expression(context, tokens, idx)
            context.set_variable(var_name, val)
        elif context.get_structure(type_name) if type_name not in ['Gauge', 'Manometer', 'Coffer', 'Apparatus', 'Repository', 'Canvas', 'Kinetic', 'int', 'float'] else False:
             # Initialize structure with default dict
             # Check if it is a structure
             try:
                 struct_def = context.get_structure(type_name)
                 # Create instance (dict for now)
                 instance = {member: None for member, _ in struct_def['members']}
                 context.set_variable(var_name, instance)
             except ExecutionError:
                 pass # Not a struct

        # 4. Semicolon
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
        
        return idx + 1
