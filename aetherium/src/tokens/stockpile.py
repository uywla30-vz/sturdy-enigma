from typing import Dict, Any
from src.core.interfaces import TokenModule

class StockpileToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'TOKEN_STOCKPILE'

    @property
    def REGEX(self) -> str:
        return r'\bStockpile\b'
    
    @property
    def PRIORITY(self) -> int:
        return 10

    def create_instance(self, value: str, line: int, col: int) -> Dict[str, Any]:
        return {'type': self.COMPONENT_ID, 'value': value}
