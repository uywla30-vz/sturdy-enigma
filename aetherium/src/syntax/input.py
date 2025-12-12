from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError
from src.core.ailment import AetheriumAilment
import sys

class ConsultPanelSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_CONSULT_PANEL'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_CONSULT_PANEL']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Used as expression typically? "Consign x = Consult_Panel As Gauge"
        # Similar issue to Workstation. It's an expression term.
        pass
        return index
