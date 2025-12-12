from typing import Dict, Any
from src.core.interfaces import TokenModule

class RepositoryToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TYPE_REPOSITORY'
    @property
    def REGEX(self) -> str: return r'\bRepository\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class OpenLedgerToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_OPEN_LEDGER'
    @property
    def REGEX(self) -> str: return r'\bOpen_Ledger\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class TranscribeToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TRANSCRIBE'
    @property
    def REGEX(self) -> str: return r'\bTranscribe\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class CatalogueToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_CATALOGUE'
    @property
    def REGEX(self) -> str: return r'\bCatalogue\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class CloseLedgerToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_CLOSE_LEDGER'
    @property
    def REGEX(self) -> str: return r'\bClose_Ledger\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ModeReadToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_MODE_READ'
    @property
    def REGEX(self) -> str: return r'\bMode_Read\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ModeWriteToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_MODE_WRITE'
    @property
    def REGEX(self) -> str: return r'\bMode_Write\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ModeAppendToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_MODE_APPEND'
    @property
    def REGEX(self) -> str: return r'\bMode_Append\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
