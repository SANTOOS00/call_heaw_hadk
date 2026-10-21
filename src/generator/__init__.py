from .dataschema import FunctionDefinition, Prompt, FunctionCalling
from ..prefixtrie import PrefixTrie
from .generator_function_name import FunctionName, FunctionNameStr, FunctionDoc
from .generator_parameters import GeneratorParameters, Parameters
from ..model import Model


import sys


class Generator:
    def __init__(
        self,
        model: Model,
        prompts: list[Prompt],
        functions_definition: list[FunctionDefinition]
    ) -> None:

        self.prompts: list[Prompt] = prompts
        self.functions_definition: list[
                FunctionDefinition
                ] = functions_definition
        self._generator_function_name: FunctionName = FunctionName(
                model=model,
                trie=PrefixTrie.insert_many(
                    [
                        model.encode_string(fun.name)
                        for fun in functions_definition
                        ]
                    ),
                functions_doc=self._get_doc(functions_definition)
                )
        self._generator_parameters: GeneratorParameters = GeneratorParameters(
                model=model
                )
        self._function_calling: list[FunctionCalling] = []

    def run(self) -> None:
        generator_name: FunctionName = self._generator_function_name
        generator_parameters: GeneratorParameters = self._generator_parameters

        for prompt in self.prompts:
            fun_name: FunctionNameStr = generator_name.generator(
                    user_prompt=prompt.prompt
                    )
            fun_def: FunctionDefinition | None = self._get_function_definition(
                    function_name=fun_name)
            if fun_def is None:
                print("[ERROR]: No tool definition matches the " +
                      f"user prompt '{prompt.prompt}'", file=sys.stderr)
                sys.exit(1)
            parameters: Parameters = generator_parameters.generator(
                    function_definition=fun_def,
                    user_prompt=prompt.prompt)

    def _get_doc(
            self,
            functions_definition: list[FunctionDefinition]
            ) -> list[FunctionDoc]:
        return [{"name": fun.name, "description": fun.description}
                for fun in functions_definition]

    def _get_function_definition(
            self,
            function_name: FunctionNameStr
            ) -> FunctionDefinition | None:
        for function in self.functions_definition:
            if function.name == function_name:
                return function
        return None

    def _add_function_calling(self, function_calling: FunctionCalling) -> None:
        self._function_calling.append(function_calling)


__all__ = ["Generator", "FunctionDefinition", "Prompt"]
