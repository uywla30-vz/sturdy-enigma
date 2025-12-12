from typing import Dict, Any
from src.core.interfaces import TokenModule

class LParenToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_LPAREN'
    @property
    def REGEX(self) -> str: return r'\('
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class RParenToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RPAREN'
    @property
    def REGEX(self) -> str: return r'\)'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class LBraceToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_LBRACE'
    @property
    def REGEX(self) -> str: return r'\{'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class RBraceToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RBRACE'
    @property
    def REGEX(self) -> str: return r'\}'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class LBracketToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_LBRACKET'
    @property
    def REGEX(self) -> str: return r'\['
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class RBracketToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RBRACKET'
    @property
    def REGEX(self) -> str: return r'\]'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class SemiToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_SEMI'
    @property
    def REGEX(self) -> str: return r';'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class CommaToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_COMMA'
    @property
    def REGEX(self) -> str: return r','
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class DotToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_DOT'
    @property
    def REGEX(self) -> str: return r'\.'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ArrowToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_ARROW'
    @property
    def REGEX(self) -> str: return r'->'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class AssignToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_ASSIGN'
    @property
    def REGEX(self) -> str: return r'='
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

# Operators
class PlusToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_PLUS'
    @property
    def REGEX(self) -> str: return r'\+'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class MinusToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_MINUS'
    @property
    def REGEX(self) -> str: return r'-'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class StarToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_STAR'
    @property
    def REGEX(self) -> str: return r'\*'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class SlashToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_SLASH'
    @property
    def REGEX(self) -> str: return r'/'
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class LessThanToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_LESS_THAN'
    @property
    def REGEX(self) -> str: return r'\bLessThan\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ExceedsToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_EXCEEDS'
    @property
    def REGEX(self) -> str: return r'\bExceeds\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class EquatesToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_EQUATES'
    @property
    def REGEX(self) -> str: return r'\bEquates\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
