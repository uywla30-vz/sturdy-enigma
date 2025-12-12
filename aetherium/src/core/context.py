from typing import Any, Dict, List, Optional
import sys

class ExecutionError(Exception):
    pass

class Variable:
    def __init__(self, name: str, type_name: str, value: Any = None):
        self.name = name
        self.type_name = type_name
        self.value = value

class Context:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables: Dict[str, Variable] = {}
        self.functions: Dict[str, Any] = {}
        self.structures: Dict[str, Any] = {}
        self.output_buffer: List[str] = []
        self.return_value: Any = None
        self.is_returning: bool = False
        # Registry reference
        self._registry = None

    @property
    def registry(self):
        if self._registry:
            return self._registry
        if self.parent:
            return self.parent.registry
        return None
    
    @registry.setter
    def registry(self, value):
        self._registry = value

    def create_child(self):
        """Creates a new scope inheriting from this one."""
        child = Context(parent=self)
        # Functions and structures are looked up via parent, so no need to copy
        return child

    def declare_variable(self, name: str, type_name: str):
        if name in self.variables:
            raise ExecutionError(f"Variable '{name}' already declared in this scope.")
        self.variables[name] = Variable(name, type_name)

    def set_variable(self, name: str, value: Any):
        # Strict rule: Must exist (Consign used on existing Stockpile)
        scope = self
        while scope:
            if name in scope.variables:
                # Basic type checking could go here
                # Check strict type compatibility if desired
                # target_type = scope.variables[name].type_name
                # if target_type == 'Gauge' and not isinstance(value, int): ...
                scope.variables[name].value = value
                return
            scope = scope.parent
        raise ExecutionError(f"Variable '{name}' not declared. Use 'Stockpile' first.")

    def get_variable(self, name: str) -> Any:
        scope = self
        while scope:
            if name in scope.variables:
                return scope.variables[name].value
            scope = scope.parent
        raise ExecutionError(f"Variable '{name}' not found.")
    
    def get_variable_type(self, name: str) -> str:
        scope = self
        while scope:
            if name in scope.variables:
                return scope.variables[name].type_name
            scope = scope.parent
        raise ExecutionError(f"Variable '{name}' not found.")

    def declare_function(self, name: str, func_def: Any):
        self.functions[name] = func_def

    def get_function(self, name: str) -> Any:
        # Functions are typically global, but we can support local
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise ExecutionError(f"Function '{name}' not defined.")

    def declare_structure(self, name: str, struct_def: Any):
        self.structures[name] = struct_def
    
    def get_structure(self, name: str) -> Any:
        if name in self.structures:
            return self.structures[name]
        if self.parent:
            return self.parent.get_structure(name)
        raise ExecutionError(f"Structure '{name}' not defined.")

    def ponder(self, message: Any):
        """Standard output for the machine."""
        print(message)
        self.output_buffer.append(str(message))
