from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError

class PonderSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_PONDER'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_PONDER']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Ponder <Expression>;
        
        idx = index + 1
        
        from src.core.expression import evaluate_expression
        val, idx = evaluate_expression(context, tokens, idx)
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        context.ponder(val)
        
        return idx + 1

class DispatchSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_DISPATCH'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_DISPATCH']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Dispatch <Expression>;
        
        idx = index + 1
        
        from src.core.expression import evaluate_expression
        val, idx = evaluate_expression(context, tokens, idx)
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        context.return_value = val
        context.is_returning = True
        
        return idx + 1
