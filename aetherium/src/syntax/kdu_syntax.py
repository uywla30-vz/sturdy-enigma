from typing import List, Any
import time
import uuid
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError, Variable
from src.core.kdu_manager import DisplayClient, KineticLogicObject, get_active_kinetics

# --- Syntax Modules ---

class OpenDisplaySyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_OPEN_DISPLAY'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_OPEN_DISPLAY']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        pass
        return index

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

    # Canvas
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
        # Assume expression resolving to string could work, but sticking to basic tokens
        raise ExecutionError("Expected Color Constant")
    index += 1

    # 4. Dimensions
    dims = {}

    # Dimension 1
    val1, index = evaluate_expression(context, tokens, index)
    if index >= len(tokens): raise ExecutionError("Expected Dimension Keyword")

    if tokens[index].type_id == 'TOKEN_WIDE':
        dims['width'] = val1
    elif tokens[index].type_id == 'TOKEN_TALL':
        dims['height'] = val1
    index += 1

    # Dimension 2
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

        idx = index + 1
        from src.core.expression import evaluate_expression

        canvas, idx = evaluate_expression(context, tokens, idx)

        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")

        # Collect updates from shared list in kdu_manager
        _active_kinetics = get_active_kinetics()

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
