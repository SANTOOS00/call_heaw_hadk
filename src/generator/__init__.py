from .dataschema import FunctionDefinition, Prompt
from ..prefixtrie import PrefixTrie
from .generator_function_name import FunctionName, FunctionNameStr
from .generator_parameters import GeneratorParameters


class Generator:
    def __init__(
        self,
        trie: PrefixTrie,
        prompts: list[Prompt],
        functions_definition: list[FunctionDefinition]
    ) -> None:
        self.prompts: list[Prompt] = prompts
        self.functions_definition: list[FunctionDefinition] = functions_definition
        self.trie: PrefixTrie = trie
        self.function_name_generator: FunctionName = FunctionName(
                trie=trie)

    def run(self) -> None:
        for prompt in self.prompts:
            fun_name: FunctionNameStr = self.function_name_generator.generator(user_prompt=prompt)
            print(fun_name)




__all__ = ["Generator", "FunctionDefinition", "Prompt"]
