from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context

class TypeDefSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_TYPEDEF'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_TYPE_GAUGE', 'TOKEN_TYPE_MANOMETER']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: TypeGauge Gauge OR TypeManometer Manometer
        # This seems to be defining an alias or just declaring usage.
        # Since 'Stockpile Gauge x' uses 'Gauge' as type.
        # I will treat this as a typedef: TypeGauge <Alias>
        
        base_type = tokens[index].value # TypeGauge or TypeManometer
        idx = index + 1
        
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_IDENTIFIER':
            alias_name = tokens[idx].value
            # We could store this in context as a type alias.
            # For now, I'll just ignore it or register it as valid type.
            # In Context, I check valid types?
            # context.declare_type(alias_name, base_type)
            idx += 1
            
        return idx

class AppDefSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_APPDEF'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_TYPE_APP']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: TypeApp Name
        idx = index + 1
        # Allow Identifier or APPARATUS token (if lexed as keyword)
        if idx < len(tokens):
            if tokens[idx].type_id == 'TOKEN_IDENTIFIER' or tokens[idx].type_id == 'TOKEN_TYPE_APPARATUS':
                idx += 1
        return idx

class AetheriumSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_AETHERIUM'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_AETHERIUM']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Just the header
        return index + 1
