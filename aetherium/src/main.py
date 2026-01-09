import sys
import os
import threading
import time

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.registry import Registry
from src.core.loader import Loader
from src.core.engine import Engine
from src.core.context import ExecutionError
from src.core.kdu_manager import init_server, DisplayClient

def run_logic(engine, tokens):
    """
    Function to run the Interpreter Logic in a separate thread.
    """
    print("Parsing and Registering (Logic Thread)...")
    try:
        engine.execute(tokens)
    except Exception as e:
        print(f"Execution Error: {e}")
        import traceback
        traceback.print_exc()
        # Signal display to quit?
        DisplayClient.signal_quit()
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
    finally:
        # Signal Display to Quit when logic ends
        print("Logic Thread Finished. Signaling Display Shutdown...")
        DisplayClient.signal_quit()

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
        # Debug: Print tokens to verify
        # for t in tokens: print(t)
    except Exception as e:
        print(f"Tokenization Error: {e}")
        return

    # 6. Initialize Display Server (on Main Thread)
    print("Initializing Display Server...")
    display_server = init_server()
    
    # 7. Start Logic Thread
    print("Starting Logic Thread...")
    logic_thread = threading.Thread(target=run_logic, args=(engine, tokens), name="Logic-Thread")
    logic_thread.start()

    # 8. Start Display Loop (Blocking Main Thread)
    print("Starting Display Loop (Main Thread)...")
    try:
        display_server.start_loop()
    except KeyboardInterrupt:
        print("Interrupted.")
        # Logic thread might still be running.
        # Ideally we set a global flag or kill it (not safe).
        sys.exit(0)

    print("Display Loop Ended. Waiting for Logic Thread...")
    logic_thread.join(timeout=2.0)
    print("Exiting.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.iz>")
    else:
        main(sys.argv[1])
