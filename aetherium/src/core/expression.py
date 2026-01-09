from typing import List, Any, Tuple
from src.core.context import Context, ExecutionError
from src.core.ailment import AetheriumAilment
import threading

def evaluate_expression(context: Context, tokens: List[Any], index: int) -> Tuple[Any, int]:
    """
    Evaluates an expression starting at 'index'.
    Returns (value, new_index).
    Handles basic arithmetic (+, -, *, /) and comparisons.
    Simple precedence parsing.
    """
    # Parse Logical/Comparison (Low Precedence)
    lhs, index = parse_term(context, tokens, index)
    
    while index < len(tokens):
        token = tokens[index]
        if token.type_id == 'TOKEN_LESS_THAN':
            rhs, index = parse_term(context, tokens, index + 1)
            lhs = lhs < rhs
        elif token.type_id == 'TOKEN_EXCEEDS':
            rhs, index = parse_term(context, tokens, index + 1)
            lhs = lhs > rhs
        elif token.type_id == 'TOKEN_EQUATES':
            rhs, index = parse_term(context, tokens, index + 1)
            lhs = lhs == rhs
        else:
            break
            
    return lhs, index

def parse_term(context: Context, tokens: List[Any], index: int) -> Tuple[Any, int]:
    # Parse Add/Sub
    lhs, index = parse_factor(context, tokens, index)
    
    while index < len(tokens):
        token = tokens[index]
        if token.type_id == 'TOKEN_PLUS':
            rhs, index = parse_factor(context, tokens, index + 1)
            lhs = lhs + rhs
        elif token.type_id == 'TOKEN_MINUS':
            rhs, index = parse_factor(context, tokens, index + 1)
            lhs = lhs - rhs
        else:
            break
    return lhs, index

def parse_factor(context: Context, tokens: List[Any], index: int) -> Tuple[Any, int]:
    # Parse Mul/Div
    lhs, index = parse_primary(context, tokens, index)
    
    while index < len(tokens):
        token = tokens[index]
        if token.type_id == 'TOKEN_STAR':
            rhs, index = parse_primary(context, tokens, index + 1)
            lhs = lhs * rhs
        elif token.type_id == 'TOKEN_SLASH':
            rhs, index = parse_primary(context, tokens, index + 1)
            if rhs == 0:
                 raise AetheriumAilment(fault_code=1, message="Division by Zero")
            lhs = lhs / rhs
        else:
            break
    return lhs, index

def parse_primary(context: Context, tokens: List[Any], index: int) -> Tuple[Any, int]:
    if index >= len(tokens):
        raise ExecutionError("Unexpected end of expression")
        
    token = tokens[index]
    
    if token.type_id == 'TOKEN_NUMBER' or token.type_id == 'TOKEN_FLOAT' or token.type_id == 'TOKEN_STRING':
        return token.value, index + 1
        
    # --- REPOSITORY: Open_Ledger ---
    if token.type_id == 'TOKEN_OPEN_LEDGER':
        # Syntax: Open_Ledger "Filename" Mode_Write
        idx = index + 1
        
        # Filename (Expression, likely string literal)
        # Using evaluate_expression recursive might be overkill if we just expect a string, but safer.
        # But wait, evaluate_expression might consume 'Mode_Write' if it's an identifier?
        # Mode_Write is a keyword.
        # Let's just expect a String Token for simplicity or parse simple primary.
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_STRING':
            raise ExecutionError("Expected Filename String after Open_Ledger")
        filename = tokens[idx].value
        idx += 1
        
        # Mode
        if idx >= len(tokens):
             raise ExecutionError("Expected Mode after Filename")
        
        mode_token = tokens[idx]
        mode = 'r'
        if mode_token.type_id == 'TOKEN_MODE_READ': mode = 'r'
        elif mode_token.type_id == 'TOKEN_MODE_WRITE': mode = 'w'
        elif mode_token.type_id == 'TOKEN_MODE_APPEND': mode = 'a'
        else:
            raise ExecutionError("Expected Mode_Read, Mode_Write, or Mode_Append")
        idx += 1
        
        try:
            f = open(filename, mode)
            return f, idx
        except Exception as e:
            # Raise Ailment (Catastrophe)
            raise AetheriumAilment(fault_code=7, message=f"Ledger Access Failed: {e}")

    # --- CONCURRENCY: Workstation ---
    if token.type_id == 'TOKEN_WORKSTATION':
        # Syntax: Workstation <FuncName>
        idx = index + 1
        if idx >= len(tokens) or (tokens[idx].type_id != 'TOKEN_IDENTIFIER' and tokens[idx].type_id != 'TOKEN_MAIN_CONDUIT'):
            raise ExecutionError("Expected Function Name after Workstation")
        
        func_name = tokens[idx].value
        func_def = context.get_function(func_name)
        idx += 1
        
        # Create Thread
        # We need to run func_def['executor'] in a new context.
        # Issue: Context needs to be thread-safe or isolated.
        # We create a child of the GLOBAL context (to share funcs) but detached from current stack?
        # Actually, sharing Global variables in threads is tricky (race conditions).
        # For this sim, we assume isolated stack, shared globals (read-only mostly).
        # We create a new root context that inherits from current context's root?
        
        # Find root
        root = context
        while root.parent: root = root.parent
        
        thread_context = root.create_child()
        # IMPORTANT: We need to inject the registry if it's not in root properties (it is via property).
        
        def thread_target():
            try:
                func_def['executor'](thread_context)
            except Exception as e:
                print(f"Workstation Error: {e}")

        t = threading.Thread(target=thread_target, name=f"Workstation-{func_name}")
        t.start()
        
        return t, idx

    # --- INPUT: Consult_Panel ---
    if token.type_id == 'TOKEN_CONSULT_PANEL':
        # Syntax: Consult_Panel As <Type>
        idx = index + 1
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_AS':
            raise ExecutionError("Expected 'As' after Consult_Panel")
        idx += 1
        
        if idx >= len(tokens): raise ExecutionError("Expected Type after As")
        target_type_token = tokens[idx]
        target_type = target_type_token.value # "Gauge" or "Manometer"
        idx += 1
        
        # Perform Input
        try:
            raw_input = input("") # Prompt is usually printed before via Ponder
        except EOFError:
            raw_input = ""
            
        # Convert
        try:
            if target_type == 'Gauge' or target_type_token.type_id == 'TOKEN_TYPE_GAUGE':
                return int(raw_input), idx
            elif target_type == 'Manometer' or target_type_token.type_id == 'TOKEN_TYPE_MANOMETER':
                return float(raw_input), idx
            else:
                 raise ValueError("Unknown Type")
        except ValueError:
             raise AetheriumAilment(fault_code=2, message="Input Malfunction")

    # --- KDU: Open_Display ---
    if token.type_id == 'TOKEN_OPEN_DISPLAY':
        from src.syntax.kdu_syntax import execute_open_display
        return execute_open_display(context, tokens, index + 1)

    # --- KDU: Draw_Shape ---
    if token.type_id == 'TOKEN_DRAW_SHAPE':
        from src.syntax.kdu_syntax import execute_draw_shape
        return execute_draw_shape(context, tokens, index + 1)

    if token.type_id == 'TOKEN_IDENTIFIER':
        # Could be a variable or a function call
        # Check if next token is '('
        if index + 1 < len(tokens) and tokens[index + 1].type_id == 'TOKEN_LPAREN':
            return parse_function_call(context, tokens, index)
        
        # Variable access or Struct member access (e.g. Data.Val)
        val = context.get_variable(token.value)
        idx = index + 1
        
        # Handle dot notation for structs
        while idx < len(tokens) and tokens[idx].type_id == 'TOKEN_DOT':
            idx += 1 # Skip dot
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
                raise ExecutionError("Expected identifier after dot")
            member_name = tokens[idx].value
            if isinstance(val, dict) and member_name in val:
                val = val[member_name]
            else:
                 raise ExecutionError(f"Cannot access member '{member_name}'")
            idx += 1
            
        return val, idx
        
    if token.type_id == 'TOKEN_LPAREN':
        val, idx = evaluate_expression(context, tokens, index + 1)
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_RPAREN':
            raise ExecutionError("Expected ')'")
        return val, idx + 1
        
    raise ExecutionError(f"Unexpected token in expression: {token}")

def parse_function_call(context: Context, tokens: List[Any], index: int) -> Tuple[Any, int]:
    func_name = tokens[index].value
    func_def = context.get_function(func_name) 
    
    index += 2 # Skip Name and (
    args = []
    
    if tokens[index].type_id != 'TOKEN_RPAREN':
        while True:
            arg_val, index = evaluate_expression(context, tokens, index)
            args.append(arg_val)
            if tokens[index].type_id == 'TOKEN_COMMA':
                index += 1
            elif tokens[index].type_id == 'TOKEN_RPAREN':
                break
            else:
                raise ExecutionError("Expected ',' or ')' in function arguments")
    
    index += 1 # Skip )
    
    child_context = context.create_child()
    
    if len(args) != len(func_def['params']):
        raise ExecutionError(f"Function '{func_name}' expects {len(func_def['params'])} arguments, got {len(args)}")
        
    for i, (param_name, param_type) in enumerate(func_def['params']):
        child_context.declare_variable(param_name, param_type)
        child_context.set_variable(param_name, args[i])
        
    return func_def['executor'](child_context), index
