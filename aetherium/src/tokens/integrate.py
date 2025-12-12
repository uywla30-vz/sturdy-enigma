from typing import Dict, Any
from src.core.interfaces import TokenModule

class IntegrateToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_INTEGRATE'
    @property
    def REGEX(self) -> str: return r'\bIntegrate\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class FromToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_FROM'
    @property
    def REGEX(self) -> str: return r'\bFrom\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
