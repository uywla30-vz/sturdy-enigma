from typing import List, Any
import os
from src.core.interfaces import SyntaxModule
from src.core.context import Context, ExecutionError
from src.core.ailment import AetheriumAilment

class IntegrateSyntax(SyntaxModule):
    @property
    def COMPONENT_ID(self) -> str: return 'SYNTAX_INTEGRATE'
    @property
    def STARTS_WITH(self) -> List[str]: return ['TOKEN_INTEGRATE']

    def evaluate(self, context: Context, tokens: List[Any], index: int) -> int:
        # Syntax: Integrate <Symbol> From "Filename";
        # Note: If <Symbol> is '*', import all? The prompt says "Integrate Lathe_Operation From..."
        # So we import a specific symbol.
        
        idx = index + 1
        
        # Symbol
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_IDENTIFIER':
            raise ExecutionError("Expected Symbol to Integrate")
        target_symbol = tokens[idx].value
        idx += 1
        
        # From
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_FROM':
             raise ExecutionError("Expected 'From'")
        idx += 1
        
        # Filename
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_STRING':
            raise ExecutionError("Expected Filename String")
        filename = tokens[idx].value
        idx += 1
        
        # Semi
        if idx >= len(tokens) or tokens[idx].type_id != 'TOKEN_SEMI':
            raise ExecutionError("Expected ';'")
            
        # Execution Logic: Import
        # We need to find the file. Assume relative to current working dir or src/examples/
        # Ideally relative to the running script, but for now absolute or CWD.
        
        if not os.path.exists(filename):
             # Try prefixing with src/examples/ for convenience in this environment
             potential_path = os.path.join('src/examples', filename)
             if os.path.exists(potential_path):
                 filename = potential_path
             else:
                 raise AetheriumAilment(fault_code=8, message=f"Integration Failed: File '{filename}' not found")

        # We need to parse this file.
        # Issue: We need access to the Engine's tokenize and execute methods.
        # context.registry is available. But 'tokenize' is in Engine.
        # We can reconstruct an Engine? Or assume we have a helper.
        
        # We can't easily import Engine due to circular imports if Engine imports Syntax.
        # But Syntax is loaded dynamically.
        
        # Strategy: Import Engine inside the method.
        try:
            from src.core.engine import Engine
            # We need the registry. Context has it.
            engine = Engine(context.registry)
            
            with open(filename, 'r') as f:
                code = f.read()
            
            imported_tokens = engine.tokenize(code)
            
            # Execute the imported script in a separate context to avoid pollution,
            # BUT we want to capture definitions.
            # Actually, we want definitions to end up in the CURRENT context (global).
            # So we pass 'context' (or the root context) to the new engine?
            
            # If we pass 'context', execution of 'Main_Conduit' in the library might trigger?
            # We only want definitions.
            # The library file has 'Main_Conduit' usually? 
            # The example `lathe_library.iz` does NOT have Main_Conduit, just definitions.
            # If it had, we should probably ignore it or not execute it.
            # Standard Aetherium execution (my implementation) simply defines functions/structs as it parses top-level tokens.
            # Only `Main_Conduit` is explicitly called by `main.py`.
            # So, executing the tokens *will* just register the functions into the context.
            
            # We should use the SAME context so definitions stick.
            engine.context = context 
            
            # Run
            engine.execute(imported_tokens)
            
            # Check if symbol exists now
            try:
                # Try getting function or structure
                found = False
                try:
                    context.get_function(target_symbol)
                    found = True
                except:
                    try:
                        context.get_structure(target_symbol)
                        found = True
                    except:
                        pass
                
                if not found:
                     raise AetheriumAilment(fault_code=9, message=f"Symbol '{target_symbol}' not found in '{filename}'")
                     
            except Exception as e:
                 raise e
                 
        except Exception as e:
            raise AetheriumAilment(fault_code=10, message=f"Integration Error: {e}")
            
        return idx + 1
