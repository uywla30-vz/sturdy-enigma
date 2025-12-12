import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.registry import Registry
from src.core.loader import Loader
from src.core.engine import Engine
from src.core.context import ExecutionError

def main(filepath):
    print(f"--- Aetherium Interpreter ---")
    print(f"Loading script: {filepath}")
    
    # 1. Initialize Registry and Loader
    registry = Registry()
    loader = Loader(registry)
    
    # 2. Load Modules
    # Assuming we are running from root or src/..
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tokens_dir = os.path.join(base_dir, 'tokens')
    syntax_dir = os.path.join(base_dir, 'syntax')
    
    print("Loading Tokens...")
    loader.load_directory(tokens_dir, 'token')
    print("Loading Syntax...")
    loader.load_directory(syntax_dir, 'syntax')
    
    # 3. Read Source
    try:
        with open(filepath, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return

    # 4. Initialize Engine
    engine = Engine(registry)
    # Inject registry into context (hack for recursive execution in modules)
    engine.context.registry = registry
    
    # 5. Tokenize
    try:
        tokens = engine.tokenize(source_code)
        # print(f"Tokens: {tokens}")
        # Debug: Print tokens to verify
        for t in tokens: print(t)
    except Exception as e:
        print(f"Tokenization Error: {e}")
        return

    # 6. Execute (First Pass - Declaration)
    # The script defines functions and then we need to run Main_Conduit.
    # The standard 'execute' loop runs top-level syntax.
    # In the scripts, top level items are: Aetherium, TypeApp, TypeGauge, Structure, Function.
    # All of these register things in Context.
    # EXCEPT: 'Aetherium' and 'TypeApp' are just headers.
    
    print("Parsing and Registering...")
    try:
        engine.execute(tokens)
    except Exception as e:
        print(f"Execution Error: {e}")
        import traceback
        traceback.print_exc()
        return

    # 7. Invoke Main_Conduit
    print("\n--- Invoking Main_Conduit ---")
    try:
        main_func = engine.context.get_function('Main_Conduit')
        # Execute Main_Conduit
        # It takes no args
        
        # Create a clean child context for execution? 
        # Or execute in a child of global.
        child_context = engine.context.create_child()
        
        # We need the executor
        if 'executor' in main_func:
            result = main_func['executor'](child_context)
            print(f"\n[Program Terminated] Return Code: {result}")
        else:
            print("Error: Main_Conduit has no executor.")
            
    except ExecutionError as e:
        print(f"Runtime Error during Main_Conduit: {e}")
    except Exception as e:
        print(f"System Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.iz>")
    else:
        main(sys.argv[1])
