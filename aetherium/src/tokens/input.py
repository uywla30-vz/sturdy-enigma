from typing import Dict, Any
from src.core.interfaces import TokenModule

class ConsultPanelToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_CONSULT_PANEL'
    @property
    def REGEX(self) -> str: return r'\bConsult_Panel\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
