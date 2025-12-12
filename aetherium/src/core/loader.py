import os
import importlib.util
import sys
from typing import Dict, Type
from src.core.interfaces import TokenModule, SyntaxModule
from src.core.registry import Registry

class Loader:
    def __init__(self, registry: Registry):
        self.registry = registry

    def load_directory(self, path: str, module_type: str):
        if not os.path.exists(path):
            print(f"[Loader] Directory not found: {path}")
            return

        for filename in os.listdir(path):
            if filename.endswith(".py") and filename != "__init__.py":
                self._load_file(os.path.join(path, filename), module_type)

    def _load_file(self, filepath: str, module_type: str):
        module_name = os.path.basename(filepath).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if not spec or not spec.loader:
            return
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Inspect classes in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type):
                # Check for strict compliance
                if module_type == 'token' and issubclass(attr, TokenModule) and attr is not TokenModule:
                    self._validate_and_register(attr, 'token')
                elif module_type == 'syntax' and issubclass(attr, SyntaxModule) and attr is not SyntaxModule:
                    self._validate_and_register(attr, 'syntax')

    def _validate_and_register(self, cls: Type, kind: str):
        try:
            instance = cls()
            # Strict validation happens here by instantiation and property access
            # If abstract methods are not implemented, instantiation fails.
            if kind == 'token':
                if not hasattr(instance, 'COMPONENT_ID') or not hasattr(instance, 'REGEX'):
                    raise ValueError("Missing required properties")
                self.registry.register_token(instance)
            elif kind == 'syntax':
                if not hasattr(instance, 'COMPONENT_ID') or not hasattr(instance, 'STARTS_WITH'):
                    raise ValueError("Missing required properties")
                self.registry.register_syntax(instance)
        except Exception as e:
            print(f"[Loader] Failed to load {kind} from {cls.__name__}: {e}")
