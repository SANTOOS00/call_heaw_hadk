from .dataschema import FunctionDefinition, Prompt
from ..prefixtrie import PrefixTrie
from  

class Generator:
    def __init__(self,
                 trie: PrefixTrie,
                 prompts: list[Prompt],
                 functions_definition: list[FunctionDefinition]) -> None:
        self.prompts: list[Prompt] = prompts
        self.functions_definition: list[FunctionDefinition] = functions_definition
        self.trie: PrefixTrie = trie

    def run(self) -> None:
        for prompt in self.prompts:
           pass
            # fun_def: FunctionDefinition = 





__all__ = ["Generator", "FunctionDefinition", "Prompt"]
