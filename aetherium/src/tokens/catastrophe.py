from typing import Dict, Any
from src.core.interfaces import TokenModule

class CatastropheToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_CATASTROPHE'
    @property
    def REGEX(self) -> str: return r'\bCatastrophe\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class BypassToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_BYPASS'
    @property
    def REGEX(self) -> str: return r'\bBypass\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ResolutionToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RESOLUTION'
    @property
    def REGEX(self) -> str: return r'\bResolution\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class SignalAilmentToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_SIGNAL_AILMENT'
    @property
    def REGEX(self) -> str: return r'\bSignal_Ailment\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ReportToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_REPORT'
    @property
    def REGEX(self) -> str: return r'\bReport\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class AsToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_AS'
    @property
    def REGEX(self) -> str: return r'\bAs\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
