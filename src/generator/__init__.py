from .dataschema import FunctionDefinition, Prompt
from ..prefixtrie import PrefixTrie
from .generator_function_name import FunctionName, FunctionNameStr, FunctionDoc
from .generator_parameters import GeneratorParameters, Parameters
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
        self._generator_function_name: FunctionName = FunctionName(
                model=model,
                trie=trie,
                functions_doc=self._get_doc(functions_definition)
                )
        self._generator_parameters: GeneratorParameters = GeneratorParameters()

    def run(self) -> None:
        generator_name: FunctionName= self._generator_function_name
        generator_parameters: GeneratorParameters= self._generator_parameters

        for prompt in self.prompts:
            fun_name: FunctionNameStr = generator_name.generator(
                    user_prompt=prompt.prompt
                    )
            fun_def: FunctionDefinition | None= self.get_function_definition(
                    function_name=fun_name)
            if fun_def is None:
                print(f"[ERROR]: No tool definition matches the "
                      f"user prompt '{prompt.prompt}'", file=sys.stderr)
                sys.exit(1)
            print(fun_name)
            parameters: Parameters = generator_parameters.generator(function_definition=fun_def)
            print(parameters)

    def _get_doc(self, functions_definition: list[FunctionDefinition]) -> FunctionDoc:
        return [{"name": fun.name, "description": fun.description} for fun in functions_definition]

    def get_function_definition(
            self,
            function_name: FunctionNameStr
            ) -> FunctionDefinition | None:
        for function in self.functions_definition:
            if function.name == function_name:
                return function
        return None


__all__ = ["Generator", "FunctionDefinition", "Prompt"]

