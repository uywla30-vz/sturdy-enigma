from typing import Dict, Any
from src.core.interfaces import TokenModule

# --- Types ---
class CanvasToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TYPE_CANVAS'
    @property
    def REGEX(self) -> str: return r'\bCanvas\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class KineticToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TYPE_KINETIC'
    @property
    def REGEX(self) -> str: return r'\bKinetic\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

# --- Keywords (Actions) ---
class OpenDisplayToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_OPEN_DISPLAY'
    @property
    def REGEX(self) -> str: return r'\bOpen_Display\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class RenderToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RENDER'
    @property
    def REGEX(self) -> str: return r'\bRender\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class DrawShapeToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_DRAW_SHAPE'
    @property
    def REGEX(self) -> str: return r'\bDraw_Shape\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class RelocateToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RELOCATE'
    @property
    def REGEX(self) -> str: return r'\bRelocate\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class DelayCycleToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_DELAY_CYCLE'
    @property
    def REGEX(self) -> str: return r'\bDelay_Cycle\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

# --- Parameters / Noise Words ---
class WideToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_WIDE'
    @property
    def REGEX(self) -> str: return r'\bWide\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class TallToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TALL'
    @property
    def REGEX(self) -> str: return r'\bTall\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class AtToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_AT'
    @property
    def REGEX(self) -> str: return r'\bAt\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ToToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TO'
    @property
    def REGEX(self) -> str: return r'\bTo\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class TitleToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_TITLE'
    @property
    def REGEX(self) -> str: return r'\bTitle\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class ByToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_BY'
    @property
    def REGEX(self) -> str: return r'\bBy\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

# --- Shapes ---
# Usually identifiers, but if we want them reserved
class RectangleToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_RECTANGLE'
    @property
    def REGEX(self) -> str: return r'\bRectangle\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

class CircleToken(TokenModule):
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_CIRCLE'
    @property
    def REGEX(self) -> str: return r'\bCircle\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}

# --- Colors ---
class ColorToken(TokenModule):
    # Matches any of the defined colors
    # We could have separate tokens, but one Generic Color Token is easier if they behave similarly.
    # However, to be strict, let's make them separate or regex match all.
    @property
    def COMPONENT_ID(self) -> str: return 'TOKEN_COLOR'
    @property
    def REGEX(self) -> str: return r'\b(Black|White|Red|Green|Blue|Gray|Copper)\b'
    @property
    def PRIORITY(self) -> int: return 10
    def create_instance(self, value, l, c): return {'type': self.COMPONENT_ID, 'value': value}
