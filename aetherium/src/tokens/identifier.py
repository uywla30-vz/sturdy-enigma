from typing import Dict, Any
from src.core.interfaces import TokenModule

class IdentifierToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'TOKEN_IDENTIFIER'

    @property
    def REGEX(self) -> str:
        return r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    
    @property
    def PRIORITY(self) -> int:
        return 0 # Low priority so keywords match first

    def create_instance(self, value: str, line: int, col: int) -> Dict[str, Any]:
        return {'type': self.COMPONENT_ID, 'value': value}
