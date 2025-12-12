from typing import List, Any
import time
import uuid
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError, Variable
from src.core.kdu_manager import DisplayClient

# --- Helper Classes for Logic Thread ---

class KineticLogicObject:
    def __init__(self, shape, color, x, y, width=0, height=0, radius=0):
        self.id = str(uuid.uuid4())
        self.shape = shape
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        # Register immediately
        DisplayClient.register_kinetic(
            self.id, shape, color, x, y,
            width=width, height=height, radius=radius
        )

# --- Syntax Modules ---

class OpenDisplaySyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_OPEN_DISPLAY'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_OPEN_DISPLAY']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Open_Display <Width> By <Height> Title <String>
        # This is an EXPRESSION in the example: Consign X = Open_Display ...
        # But here 'evaluate' is for statements.
        # This must be handled in EXPRESSION parser or return a value here?
        # The engine logic: if execute() calls evaluate(), it expects index update.
        # If this is used in Consign, Consign calls evaluate_expression.
        # Evaluate_expression in src/core/expression.py needs to handle TOKEN_OPEN_DISPLAY.

        # HOWEVER, if I modify expression.py, I violate modularity if I hardcode it there.
        # But I have to, unless I change how Consign works.
        # I will return index (assuming standalone usage?)
        # Wait, the user example: Consign Main_Screen = Open_Display ...
        # So it IS an expression.
        # I will implement the logic here, but I must patch expression.py to call it.
        # Or I can make Open_Display a valid "Primary" in expression.py.
        # See my plan regarding expression.py.
        pass
        return index

# Since I cannot dynamically extend expression.py easily without patching it,
# I will implement the Logic in helper functions here, and then Patch expression.py
# to call these helpers when it encounters the tokens.

def execute_open_display(context: Context, tokens: List[Any], index: int):
    # Width
    from src.core.expression import evaluate_expression
    width, index = evaluate_expression(context, tokens, index)

    # By
    if index >= len(tokens) or tokens[index].type_id != 'TOKEN_BY':
        raise ExecutionError("Expected 'By'")
    index += 1

    # Height
    height, index = evaluate_expression(context, tokens, index)

    # Title (Optional? Example shows Title)
    title = "Aetherium"
    if index < len(tokens) and tokens[index].type_id == 'TOKEN_TITLE':
        index += 1
        title_val, index = evaluate_expression(context, tokens, index)
        title = str(title_val)

    DisplayClient.open_display(width, height, title)

    # Return a Canvas Handle (just a string or object)
    return "CANVAS_HANDLE", index

def execute_draw_shape(context: Context, tokens: List[Any], index: int):
    # Syntax: Draw_Shape <Canvas> <ShapeType> <Color> <D1> Wide <D2> Tall At <X>, <Y>
    # Note: Example: Draw_Shape Main_Screen Rectangle Gray 50 Wide 80 Tall At 100, 100;

    # Canvas
    # In expression, index points to first arg after Draw_Shape?
    # No, evaluate_expression calls this.

    from src.core.expression import evaluate_expression

    # 1. Canvas
    canvas, index = evaluate_expression(context, tokens, index)

    # 2. Shape Type (Rectangle/Circle)
    if index >= len(tokens): raise ExecutionError("Expected Shape Type")
    shape_token = tokens[index]
    shape_type = ""
    if shape_token.type_id == 'TOKEN_RECTANGLE': shape_type = "Rectangle"
    elif shape_token.type_id == 'TOKEN_CIRCLE': shape_type = "Circle"
    else: raise ExecutionError("Unknown Shape Type")
    index += 1

    # 3. Color
    if index >= len(tokens): raise ExecutionError("Expected Color")
    color_token = tokens[index]
    color_val = "White"
    if color_token.type_id == 'TOKEN_COLOR':
        color_val = color_token.value
    else:
        # Could be an expression? User example used constant.
        # Let's support expression if it resolves to string?
        # But strict syntax says "Color".
        # Let's assume Color Token for now.
        raise ExecutionError("Expected Color Constant")
    index += 1

    # 4. Dimensions
    # Syntax varies by shape?
    # Example: 50 Wide 80 Tall
    # Let's parse generic Dimensions: <Val> <DimKeyword>

    dims = {}

    # Dimension 1
    val1, index = evaluate_expression(context, tokens, index)
    if index >= len(tokens): raise ExecutionError("Expected Dimension Keyword")

    if tokens[index].type_id == 'TOKEN_WIDE':
        dims['width'] = val1
    elif tokens[index].type_id == 'TOKEN_TALL':
        dims['height'] = val1
    # elif tokens[index].type_id == 'TOKEN_RADIUS': ...
    index += 1

    # Dimension 2 (Optional?)
    # Example has both.
    val2, index = evaluate_expression(context, tokens, index)
    if index < len(tokens):
        if tokens[index].type_id == 'TOKEN_TALL':
            dims['height'] = val2
            index += 1
        elif tokens[index].type_id == 'TOKEN_WIDE':
            dims['width'] = val2
            index += 1

    # At
    if index >= len(tokens) or tokens[index].type_id != 'TOKEN_AT':
        raise ExecutionError("Expected 'At'")
    index += 1

    # X
    x_val, index = evaluate_expression(context, tokens, index)

    # Comma
    if index >= len(tokens) or tokens[index].type_id != 'TOKEN_COMMA':
        raise ExecutionError("Expected ','")
    index += 1

    # Y
    y_val, index = evaluate_expression(context, tokens, index)

    # Create Object
    # Determine Width/Height/Radius
    w = dims.get('width', 0)
    h = dims.get('height', 0)

    obj = KineticLogicObject(shape_type, color_val, x_val, y_val, width=w, height=h)

    return obj, index


class RelocateSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_RELOCATE'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_RELOCATE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Relocate <KineticObject> To <X>, <Y>;

        idx = index + 1
        from src.core.expression import evaluate_expression

        # Object
        obj, idx = evaluate_expression(context, tokens, idx)
        if not isinstance(obj, KineticLogicObject):
            # It might be None or wrong type
            # raise ExecutionError(f"Expected Kinetic Object, got {type(obj)}")
            # For robustness, we allow it but warn? No, strict.
            pass # In dynamic lang, we trust.

        # To
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_TO':
            raise ExecutionError("Expected 'To'")
        idx += 1

        # X
        x_val, idx = evaluate_expression(context, tokens, idx)

        # Comma
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_COMMA':
            raise ExecutionError("Expected ','")
        idx += 1

        # Y
        y_val, idx = evaluate_expression(context, tokens, idx)

        # Update Logic Object
        if isinstance(obj, KineticLogicObject):
            obj.x = x_val
            obj.y = y_val

        # Semi
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")

        return idx + 1

class RenderSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_RENDER'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_RENDER']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Render <Canvas>;
        # Currently we ignore Canvas arg as we use global list, but we should parse it.

        idx = index + 1
        from src.core.expression import evaluate_expression

        canvas, idx = evaluate_expression(context, tokens, idx)

        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")

        # Collect updates
        # In a real engine, we might track dirty flags.
        # Here we iterate all variables in context to find KineticObjects?
        # That's expensive and scope-limited.
        # BETTER: KineticLogicObject tracks itself in a global registry in this module?
        # Or we rely on the user passing the objects? No, Render takes Canvas.

        # Approach: When KineticLogicObject is created, it registers to a WeakSet or similar.
        # Or we iterate the context.
        # The user said: "Render Main_Screen".
        # This implies the Screen knows what to draw.
        # But Draw_Shape returned an object, it didn't explicitly attach it to Screen (other than via arg).

        # Let's use a global tracking list for this session in `kdu_manager` or here.
        # Since we only have one display, we can track all active KineticLogicObjects.

        # But we need to find them.
        # Hack: We use a global list `_active_kinetics`.

        updates = []
        for k_obj in _active_kinetics:
            updates.append({
                'id': k_obj.id,
                'x': k_obj.x,
                'y': k_obj.y
            })

        DisplayClient.render_updates(updates)

        return idx + 1

class DelayCycleSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_DELAY_CYCLE'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_DELAY_CYCLE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Delay_Cycle <Milliseconds>;

        idx = index + 1
        from src.core.expression import evaluate_expression
        ms, idx = evaluate_expression(context, tokens, idx)

        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")

        time.sleep(ms / 1000.0)
        return idx + 1

# Global registry for active objects (simple version)
_active_kinetics = []

# Monkey-patch KineticLogicObject init to register itself
original_init = KineticLogicObject.__init__
def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    _active_kinetics.append(self)

KineticLogicObject.__init__ = new_init
