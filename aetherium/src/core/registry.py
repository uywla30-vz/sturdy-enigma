from typing import Dict
from src.core.interfaces import TokenModule, SyntaxModule

class Registry:
    def __init__(self):
        self.tokens: Dict[str, TokenModule] = {}
        self.syntax: Dict[str, SyntaxModule] = {}
        # Map syntax start tokens to the module for fast lookup
        self.syntax_map: Dict[str, SyntaxModule] = {} 

    def register_token(self, module: TokenModule):
        # print(f"[Loader] Registering Token: {module.COMPONENT_ID}")
        self.tokens[module.COMPONENT_ID] = module

    def register_syntax(self, module: SyntaxModule):
        # print(f"[Loader] Registering Syntax: {module.COMPONENT_ID}")
        self.syntax[module.COMPONENT_ID] = module
        for start_token in module.STARTS_WITH:
            if start_token in self.syntax_map:
                print(f"[Warning] Overwriting syntax handler for token {start_token}")
            self.syntax_map[start_token] = module
