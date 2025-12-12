from typing import Dict, Any
from src.core.interfaces import TokenModule

# List of simple keywords to auto-generate classes for if needed, 
# but I will stick to explicit class definitions for clarity and strictness.

class FunctionToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_FUNCTION'
    @property
    def REGEX(self) -> str: return r'\bFunction\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class MainConduitToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_MAIN_CONDUIT'
    @property
    def REGEX(self) -> str: return r'\bMain_Conduit\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class LoopToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_LOOP'
    @property
    def REGEX(self) -> str: return r'\bLoop\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class WhileToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_WHILE'
    @property
    def REGEX(self) -> str: return r'\bWhile\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class IfToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_IF'
    @property
    def REGEX(self) -> str: return r'\bIf\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ElseToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_ELSE'
    @property
    def REGEX(self) -> str: return r'\bElse\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class EndIfToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_ENDIF'
    @property
    def REGEX(self) -> str: return r'\bEndIf\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class DispatchToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_DISPATCH'
    @property
    def REGEX(self) -> str: return r'\bDispatch\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class PonderToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_PONDER'
    @property
    def REGEX(self) -> str: return r'\bPonder\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class TypeAppToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TYPE_APP'
    @property
    def REGEX(self) -> str: return r'\bTypeApp\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class StructureToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_STRUCTURE'
    @property
    def REGEX(self) -> str: return r'\bStructure\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class AetheriumToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_AETHERIUM'
    @property
    def REGEX(self) -> str: return r'\bAetherium\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
