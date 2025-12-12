from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError, Variable
from src.core.ailment import AetheriumAilment
from src.syntax.control_flow import IfSyntax # Reusing _extract_block and _execute_block logic if possible, or reimplementing.

class CatastropheSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_CATASTROPHE'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_CATASTROPHE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: 
        # Catastrophe { ... } 
        # [Bypass As Report <Name> { ... }]
        # [Resolution { ... }]
        
        idx = index + 1
        
        # 1. Catastrophe Block
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
            raise ExecutionError("Expected '{' after Catastrophe")
        
        # Helper to extract block
        catastrophe_tokens, idx = self._extract_block(tokens, idx)
        
        # 2. Check for Bypass
        bypass_tokens = []
        bypass_var_name = None
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_BYPASS':
            idx += 1
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_AS':
                raise ExecutionError("Expected 'As' after Bypass")
            idx += 1
            
            # Allow 'Report' keyword to specify type (optional or required?)
            # Prompt: "Bypass As Report <Name> { ... }" or "Bypass As <Name>"?
            # Prompt Example: "Bypass As Report Fault_Log { ... }"
            # So 'Report' is the type.
            
            if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_REPORT':
                idx += 1 # Consume type
            
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
                 raise ExecutionError("Expected Variable Name for Bypass Report")
            
            bypass_var_name = tokens[idx].value
            idx += 1
            
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
                raise ExecutionError("Expected '{' after Bypass declaration")
            
            bypass_tokens, idx = self._extract_block(tokens, idx)

        # 3. Check for Resolution
        resolution_tokens = []
        if idx < len(tokens) and tokens[idx].type_id == 'TOKEN_RESOLUTION':
            idx += 1
            if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_LBRACE':
                raise ExecutionError("Expected '{' after Resolution")
            resolution_tokens, idx = self._extract_block(tokens, idx)

        # Execution Logic
        try:
            self._execute_block(context, catastrophe_tokens)
        except AetheriumAilment as ailment:
            if bypass_tokens:
                # Execute Bypass
                child_context = context.create_child()
                # Inject Report Variable
                # We need to define the 'Report' structure if it doesn't exist?
                # The user might have defined it, or we assume it's built-in.
                # We just set the variable directly as a dictionary (structure instance).
                child_context.variables[bypass_var_name] = Variable(
                    name=bypass_var_name,
                    type_name='Report',
                    value=ailment.to_struct()
                )
                
                self._execute_block(child_context, bypass_tokens)
            else:
                # Re-raise if no bypass? Or suppress?
                # Usually panic/crash if not handled.
                raise ailment
        finally:
            if resolution_tokens:
                self._execute_block(context, resolution_tokens)
                
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
        if not hasattr(context, 'registry'):
             raise ExecutionError("Context missing registry reference")
             
        registry = context.registry
        idx = 0
        # Create child scope for the block execution? 
        # Usually blocks (like if) share scope or have new scope?
        # Aetherium blocks seem to share function scope or be new scopes.
        # Let's create a child scope to be safe for local vars.
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
                 idx += 1
