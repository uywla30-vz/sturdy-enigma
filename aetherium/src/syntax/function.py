from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError

class FunctionSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_FUNCTION'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_FUNCTION']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Function Name (Params) -> Type { Body }
        
        idx = index + 1
        
        if idx >= len(tokens):
             raise ExecutionError("Expected Function Name")
        
        # Allow Identifier or Main_Conduit as name
        if tokens[idx].type_id == 'TOKEN_IDENTIFIER' or tokens[idx].type_id == 'TOKEN_MAIN_CONDUIT':
            func_name = tokens[idx].value
        else:
            raise ExecutionError(f"Expected Function Name, got {tokens[idx].type_id}")
        idx += 1
        
        # Params
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LPAREN':
            raise ExecutionError("Expected '('")
        idx += 1
        
        params = []
        while idx < len(tokens) and tokens[idx].type_id != 'TOKEN_RPAREN':
            # Param: Type Name
            # Type can be TypeGauge, Identifier, etc.
            # Assuming strictly typed: Type Name
            p_type = tokens[idx].value
            idx += 1
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
                 raise ExecutionError("Expected Parameter Name")
            p_name = tokens[idx].value
            params.append((p_name, p_type))
            idx += 1
            
            if tokens[idx].type_id == 'TOKEN_COMMA':
                idx += 1
        
        idx += 1 # Skip )
        
        # Return Type
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_ARROW':
            idx += 1
            ret_type = tokens[idx].value
            idx += 1
        else:
            ret_type = None # Void?
            
        # Body
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
            raise ExecutionError("Expected '{'")
            
        # Extract Block (reuse helper logic, but duplicated for now to avoid mess)
        stack = 1
        start = idx + 1
        current = start
        while current < len(tokens):
            if tokens[current].type_id == 'TOKEN_LBRACE':
                stack += 1
            elif tokens[current].type_id == 'TOKEN_RBRACE':
                stack -= 1
                if stack == 0:
                    break
            current += 1
        
        if current >= len(tokens): raise ExecutionError("Unclosed function body")
        
        body_tokens = tokens[start:current]
        idx = current + 1
        
        # Define Executor
        def executor(ctx):
            # Ctx is the function scope, already has params populated
            # We need to execute body_tokens
            registry = ctx.parent.registry if ctx.parent and hasattr(ctx.parent, 'registry') else context.registry
            if not hasattr(ctx, 'registry'):
                ctx.registry = registry # Propagate registry
            
            b_idx = 0
            while b_idx < len(body_tokens):
                token = body_tokens[b_idx]
                if token.type_id in registry.syntax_map:
                    handler = registry.syntax_map[token.type_id]
                    b_idx = handler.evaluate(ctx, body_tokens, b_idx)
                    if ctx.is_returning:
                        return ctx.return_value
                else:
                    b_idx += 1
            return None # Void return

        func_def = {
            'params': params,
            'ret_type': ret_type,
            'executor': executor
        }
        
        context.declare_function(func_name, func_def)
        
        return idx
