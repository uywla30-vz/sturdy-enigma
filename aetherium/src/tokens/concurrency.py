from typing import Dict, Any
from src.core.interfaces import TokenModule

class WorkstationToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_WORKSTATION'
    @property
    def REGEX(self) -> str: return r'\bWorkstation\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class JoinHaltToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_JOIN_HALT'
    @property
    def REGEX(self) -> str: return r'\bJoin_Halt\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ApparatusToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TYPE_APPARATUS'
    @property
    def REGEX(self) -> str: return r'\bApparatus\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
