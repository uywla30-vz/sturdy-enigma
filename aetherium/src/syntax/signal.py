from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError
from src.core.ailment import AetheriumAilment
from src.core.expression import evaluate_expression

class SignalAilmentSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_SIGNAL_AILMENT'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_SIGNAL_AILMENT']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Signal_Ailment "Message";
        
        idx = index + 1
        
        # We expect a string or expression evaluating to string?
        # Example: Signal_Ailment "Pressure Valve Burst";
        
        val, idx = evaluate_expression(context, tokens, idx)
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        # Raise the ailment
        raise AetheriumAilment(fault_code=999, message=str(val))
        
        return idx + 1
