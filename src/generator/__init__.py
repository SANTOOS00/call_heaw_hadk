from .dataschema import FunctionDefinition, Prompt
from ..prefixtrie import PrefixTrie
from .generator_function_name import FunctionName, FunctionNameStr
from .generator_parameters import GeneratorParameters
from ..model import Model


import sys


class Generator:
    def __init__(
        self,
        model: Model,
        trie: PrefixTrie,
        prompts: list[Prompt],
        functions_definition: list[FunctionDefinition]
    ) -> None:
        self.prompts: list[Prompt] = prompts
        self.functions_definition: list[FunctionDefinition] = functions_definition
        self.trie: PrefixTrie = trie
        self.function_name_generator: FunctionName = FunctionName(
                model=model,
                trie=trie,
                functions_doc=[{"name": fun.name, "description": fun.description} for fun in functions_definition])
    def run(self) -> None:
        for prompt in self.prompts:
            fun_name: FunctionNameStr = self.function_name_generator.generator(user_prompt=prompt.prompt)
            fun_def: FunctionDefinition | None= self.get_function_definition(
                    function_name=fun_name)
            if fun_def is None:
                print(f"[ERROR]: No tool definition matches the user prompt '{prompt.prompt}'", file=sys.stderr)
                sys.exit(1)
            print(fun_def)

    def get_function_definition(
            self,
            function_name: FunctionNameStr
            ) -> FunctionDefinition | None:
        for function in self.functions_definition:
            if function.name == function_name:
                return function
        return None


__all__ = ["Generator", "FunctionDefinition", "Prompt"]

