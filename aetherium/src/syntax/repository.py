from typing import List, Any
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError
from src.core.ailment import AetheriumAilment
from src.core.expression import evaluate_expression
import io

class TranscribeSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_TRANSCRIBE'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_TRANSCRIBE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Transcribe <Repo> <Data>;
        idx = index + 1
        
        # Repo
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Repository Identifier")
        repo_name = tokens[idx].value
        repo = context.get_variable(repo_name)
        
        # Verify it's a file object
        if not hasattr(repo, 'write'):
            raise AetheriumAilment(fault_code=3, message="Invalid Repository Handle")
        
        idx += 1
        
        # Data (Expression)
        val, idx = evaluate_expression(context, tokens, idx)
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
        
        try:
            repo.write(str(val))
            repo.flush() # Ensure written immediately for demo
        except Exception as e:
            raise AetheriumAilment(fault_code=4, message=f"Transcribe Failed: {e}")
            
        return idx + 1

class CatalogueSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_CATALOGUE'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_CATALOGUE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Catalogue <Repo> <Buffer>;
        idx = index + 1
        
        # Repo
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Repository Identifier")
        repo_name = tokens[idx].value
        repo = context.get_variable(repo_name)
        
        if not hasattr(repo, 'read'):
            raise AetheriumAilment(fault_code=3, message="Invalid Repository Handle")
            
        idx += 1
        
        # Buffer Variable
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
             raise ExecutionError("Expected Buffer Variable Identifier")
        buffer_name = tokens[idx].value
        idx += 1
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        try:
            # Simple read all for now
            # In a real system, might read lines or bytes.
            content = repo.read()
            context.set_variable(buffer_name, content)
        except Exception as e:
            raise AetheriumAilment(fault_code=5, message=f"Catalogue Failed: {e}")
            
        return idx + 1

class CloseLedgerSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_CLOSE_LEDGER'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_CLOSE_LEDGER']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Close_Ledger <Repo>;
        idx = index + 1
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Repository Identifier")
        repo_name = tokens[idx].value
        repo = context.get_variable(repo_name)
        
        if not hasattr(repo, 'close'):
             raise AetheriumAilment(fault_code=3, message="Invalid Repository Handle")
             
        idx += 1
        
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        try:
            repo.close()
            # Optional: set variable to None or indicate closed?
        except Exception as e:
            raise AetheriumAilment(fault_code=6, message=f"Close Failed: {e}")
            
        return idx + 1
