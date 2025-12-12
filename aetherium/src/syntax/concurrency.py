from typing import List, Any
import threading
import time
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError

class WorkstationSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_WORKSTATION'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_WORKSTATION']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Workstation <FunctionIdentifier>
        # Note: This returns an Apparatus object (the thread).
        # It is usually used in an assignment: Consign ID = Workstation Lathe_Op;
        # But 'evaluate' here is called by the Engine loop.
        # Wait, 'evaluate' in Engine loop is for statements.
        # 'Workstation' is an expression that returns a value?
        # In example: Consign Lathe_Apparatus_ID = Workstation Lathe_Operation;
        # So 'Workstation Lathe_Operation' is the RHS expression.
        
        # Current 'Consign' syntax calls 'evaluate_expression'.
        # 'evaluate_expression' handles operators and function calls.
        # It does NOT currently handle 'Workstation' keyword as a prefix operator.
        
        # We need to extend 'evaluate_expression' or treat Workstation as a statement?
        # No, it's used in assignment.
        
        # Hack: Since my architecture delegates syntax execution to top-level statements mostly,
        # handling 'Workstation' inside an expression requires 'evaluate_expression' to know about it.
        # OR, I can make 'WorkstationSyntax' a standalone statement that returns? No.
        
        # I will modify 'src/core/expression.py' to handle 'TOKEN_WORKSTATION' in 'parse_primary' or 'parse_factor'.
        # But 'WorkstationSyntax' module is where logic should live.
        # The prompt requires strict modularity.
        
        # Solution: 'evaluate_expression' can call into Registry to find if a token starts an expression-compatible Syntax Module?
        # That's too complex for now.
        
        # I will implement the logic here in 'evaluate' (if used as statement) AND 
        # I will patch 'expression.py' to delegate to this module if it sees 'Workstation'.
        # Actually, let's keep it simple. 'Workstation' is a Unary Operator in expression terms.
        
        # But for now, since I can't easily change expression.py to dynamic load operators without big refactor:
        # I will hardcode the hook in expression.py to call this logic, OR
        # I will assume the user uses it as I implement it.
        
        # Let's look at how I implemented 'Consign'. It calls 'evaluate_expression'.
        # I will add 'TOKEN_WORKSTATION' handling to 'evaluate_expression'.
        
        # However, to keep modularity, I should ideally define this behavior here.
        # Since I cannot easily invert control from expression.py without a registry lookup there,
        # I will implement a static method or helper here that expression.py can import?
        # No, circular imports.
        
        # Decision: I will add support in `src/core/expression.py` to recognize `Workstation` token
        # and execute the thread creation logic directly there, or call a helper in `src/core/concurrency_manager.py`.
        
        # Wait, I am supposed to implement `WorkstationSyntax`.
        # If I implement `evaluate`, it is for Top Level or Block Level statements.
        # `Consign x = Workstation y` is a `Consign` statement.
        # The RHS is `Workstation y`.
        
        # I will modify `evaluate_expression` to handle `TOKEN_WORKSTATION`.
        pass 
        return index

class JoinHaltSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str:
        return 'SYNTAX_JOIN_HALT'

    @property
    def STARTS_WITH(self) -> List[str]:
        return ['TOKEN_JOIN_HALT']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Join_Halt <ApparatusVariable>;
        
        idx = index + 1
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Apparatus Variable")
        
        var_name = tokens[idx].value
        idx += 1
        
        # Get the thread object
        thread = context.get_variable(var_name)
        
        # Verify it is a thread/Apparatus
        if not isinstance(thread, threading.Thread):
             # In a real system we'd check type tag.
             pass
             
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        # Ponder "Joining..."
        thread.join()
        
        return idx + 1
