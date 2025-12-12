from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
import re

class Context:
    """Placeholder for the execution context."""
    pass

class TokenModule(ABC):
    """
    Interface strict for Token Modules.
    Atomic definition of a lexical unit.
    """
    @property
    @abstractmethod
    def COMPONENT_ID(self) -> str:
        """Unique ID for the component (e.g., 'TOKEN_GAUGE')."""
        pass

    @property
    @abstractmethod
    def REGEX(self) -> str:
        """Regular expression to identify this token."""
        pass
        
    @property
    def PRIORITY(self) -> int:
        """Priority for lexing (higher checks first). Default 0."""
        return 0

    @abstractmethod
    def create_instance(self, value: str, line: int, col: int) -> Dict[str, Any]:
        """Creates a token instance dictionary/object."""
        pass

class SyntaxModule(ABC):
    """
    Interface strict for Syntax Modules.
    Atomic definition of a grammatical structure or execution unit.
    """
    @property
    @abstractmethod
    def COMPONENT_ID(self) -> str:
        """Unique ID for the component (e.g., 'SYNTAX_STOCKPILE')."""
        pass

    @property
    @abstractmethod
    def STARTS_WITH(self) -> List[str]:
        """List of Token IDs that trigger this syntax rule."""
        pass

    @abstractmethod
    def evaluate(self, context: Any, tokens: List[Any], index: int) -> int:
        """
        Parses and executes the logic starting at 'index'.
        Returns the new index after consuming tokens.
        """
        pass
