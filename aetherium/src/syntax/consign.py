from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError
from src.core.expression import evaluate_expression

class ConsignSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_CONSIGN'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_CONSIGN']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Consign <Name>[.Member] = <Expression>;
        
        idx = index + 1
        
        # 1. Name
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Variable Name after Consign")
        
        target_name = tokens[idx].value
        idx += 1
        
        # Handle Struct Members: Name.Member = Value
        member_chain = []
        while idx < len(tokens) and tokens[idx].type_id == 'TOKEN_DOT':
            idx += 1
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
                raise ExecutionError("Expected Member Name after '.'")
            member_chain.append(tokens[idx].value)
            idx += 1
            
        # 2. Assign Op
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_ASSIGN':
            raise ExecutionError("Expected '='")
        idx += 1
        
        # 3. Expression
        val, idx = evaluate_expression(context, tokens, idx)
        
        # 4. Semicolon
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        # Perform Assignment
        if not member_chain:
            context.set_variable(target_name, val)
        else:
            # Struct assignment
            obj = context.get_variable(target_name)
            
            # Navigate to the last container
            current = obj
            for i, member in enumerate(member_chain[:-1]):
                if isinstance(current, dict) and member in current:
                    current = current[member]
                else:
                    raise ExecutionError(f"Cannot access member '{member}'")
            
            last_member = member_chain[-1]
            if isinstance(current, dict) and last_member in current:
                current[last_member] = val
                # No need to set_variable back because dicts are mutable references
            else:
                 raise ExecutionError(f"Cannot access member '{last_member}'")

        return idx + 1
