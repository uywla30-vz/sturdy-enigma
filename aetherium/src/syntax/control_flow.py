from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError
from src.core.expression import evaluate_expression

class IfSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_IF'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_IF']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: If <Cond> { ... } [Else { ... }] [EndIf]
        # Note: Example says "Else { ... }", prompt also says "EndIf".
        # Prompt Table: "If <Cond> { ... } Else { ... } EndIf"
        # Examples: 
        #   If Final_Output Exceeds Target_Quota { ... } Else { ... }
        #   (No explicit EndIf in example A? Wait. The table says EndIf. Example A doesn't show EndIf after Else block closes '}')
        #   Let's check Script B:
        #   If Efficiency_Score Exceeds 0.7 { ... } Else { ... }
        #   It seems '}' closes the block. 'EndIf' might be optional or for non-brace style? 
        #   But the table says "If/Else/EndIf".
        #   I will implement looking for braces `{}`. If braces are present, they define scope.
        #   I will support optional EndIf keyword after the blocks if it appears.
        
        idx = index + 1
        
        # Condition
        # Condition ends at '{'
        # We can use evaluate_expression but it might consume '{' if not careful?
        # evaluate_expression stops at unknown tokens. '{' is unknown to it unless we define it as operator.
        # But wait, logic ops are part of expression.
        
        cond_val, idx = evaluate_expression(context, tokens, idx)
        
        # Then Block
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
            raise ExecutionError("Expected '{' after If condition")
        
        then_block_tokens, idx = self._extract_block(tokens, idx)
        
        # Else Block
        else_block_tokens = []
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_ELSE':
            idx += 1
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
                raise ExecutionError("Expected '{' after Else")
            else_block_tokens, idx = self._extract_block(tokens, idx)
            
        # Optional EndIf
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_ENDIF':
            idx += 1
            
        # Execute
        # We need to execute the block tokens.
        # We need access to the Engine/Registry to execute a list of tokens.
        # This is a recurring need (Function, Loop).
        # I will hack this by importing Engine locally or assuming context has a reference?
        # Better: pass 'engine' instance to evaluate? No, interface is fixed.
        # I will create a fresh Engine instance sharing the same Registry?
        # Or make `evaluate` take `engine`? I defined `evaluate(context, tokens, index)`.
        # I can add `registry` to `context`?
        
        # Let's add registry to context.
        
        if cond_val:
            self._execute_block(context, then_block_tokens)
        elif else_block_tokens:
            self._execute_block(context, else_block_tokens)
            
        return idx

    def _extract_block(self, tokens: List[Any], index: int) -> tuple[List[Any], int]:
        # index is at '{'
        stack = 1
        start = index + 1
        current = start
        while current < len(tokens):
            if tokens[current].type_id == 'TOKEN_LBRACE':
                stack += 1
            elif tokens[current].type_id == 'TOKEN_RBRACE':
                stack -= 1
                if stack == 0:
                    return tokens[start:current], current + 1
            current += 1
        raise ExecutionError("Unclosed block '{'")

    def _execute_block(self, context: Context, block_tokens: List[Any]):
        # To avoid circular import of Engine, we need a way to execute.
        # We can implement a simple loop here that calls the registry.
        # But we need the registry.
        
        # Assuming context has registry attached by Engine.
        if not hasattr(context, 'registry'):
             raise ExecutionError("Context missing registry reference")
             
        registry = context.registry
        idx = 0
        child_context = context.create_child()
        
        while idx < len(block_tokens):
            token = block_tokens[idx]
            if token.type_id in registry.syntax_map:
                handler = registry.syntax_map[token.type_id]
                idx = handler.evaluate(child_context, block_tokens, idx)
                if child_context.is_returning:
                    context.return_value = child_context.return_value
                    context.is_returning = True
                    break
            else:
                 # Ignore or Error?
                 # Could be a comment or noise?
                 idx += 1


class LoopSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_LOOP'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_LOOP']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Loop While <Cond> { ... }
        
        idx = index + 1
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_WHILE':
            raise ExecutionError("Expected 'While' after 'Loop'")
        idx += 1
        
        # Capture condition tokens to re-evaluate
        # Condition ends at '{'
        cond_start = idx
        # Scan until { to find length of condition
        while idx < len(tokens) and tokens[idx].type_id != 'TOKEN_LBRACE':
            idx += 1
        
        cond_tokens = tokens[cond_start:idx]
        
        if idx >= len(tokens): raise ExecutionError("Expected '{'")
        
        # Extract Block
        block_tokens, idx = IfSyntax()._extract_block(tokens, idx) # Reuse helper
        
        # Execute Loop
        registry = context.registry
        
        while True:
            # Evaluate Condition
            cond_val, _ = evaluate_expression(context, cond_tokens, 0)
            # evaluate_expression expects to parse something. 
            # We can just pass the cond_tokens.
            # But evaluate_expression might fail if it reaches end without consuming everything?
            # It returns (val, new_idx). We just care about val.
            
            if not cond_val:
                break
                
            # Execute Body
            child_context = context.create_child()
            b_idx = 0
            while b_idx < len(block_tokens):
                token = block_tokens[b_idx]
                if token.type_id in registry.syntax_map:
                    handler = registry.syntax_map[token.type_id]
                    b_idx = handler.evaluate(child_context, block_tokens, b_idx)
                    if child_context.is_returning:
                        context.return_value = child_context.return_value
                        context.is_returning = True
                        return idx
                else:
                    b_idx += 1
                    
        return idx
