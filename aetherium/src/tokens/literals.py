from typing import Dict, Any
from src.core.interfaces import TokenModule

class NumberToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'TOKEN_NUMBER'

    @property
    def REGEX(self) -> str:
        return r'\b\d+\b'

    def create_instance(self, value: str, line: int, col: int) -> Dict[str, Any]:
        return {'type': self.COMPONENT_ID, 'value': int(value)}

class FloatToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'TOKEN_FLOAT'

    @property
    def REGEX(self) -> str:
        return r'\b\d+\.\d+\b'
    
    @property
    def PRIORITY(self) -> int:
        return 5 # Higher than integer

    def create_instance(self, value: str, line: int, col: int) -> Dict[str, Any]:
        return {'type': self.COMPONENT_ID, 'value': float(value)}

class StringToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'TOKEN_STRING'

    @property
    def REGEX(self) -> str:
        return r'"[^"]*"'

    def create_instance(self, value: str, line: int, col: int) -> Dict[str, Any]:
        return {'type': self.COMPONENT_ID, 'value': value[1:-1]}
