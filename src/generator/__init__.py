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
                trie=self._init_trie(
                    model=model
                    ),
                functions_doc=self._get_doc(functions_definition)
                )
        self._generator_parameters: GeneratorParameters = GeneratorParameters(
                model=model
                )
        self._functions_calling: list[FunctionCalling] = []

    def run(self) -> None:
        generator_name: FunctionName = self._generator_function_name
        generator_parameters: GeneratorParameters = self._generator_parameters
        function_name: FunctionDefinition
        func_def: FunctionDefinition

        for prompt in self.prompts:
            function_name: FunctionNameStr = generator_name.generator(
                    user_prompt=prompt.prompt
                    )
            func_def: FunctionDefinition | None = self._get_func_def(
                    function_name=function_name
                    )
            if func_def is None:
                print("[ERROR]: No tool definition matches the " +
                      f"user prompt '{prompt.prompt}'", file=sys.stderr)
                sys.exit(1)

            parameters: Parameters = generator_parameters.generator(
                    function_definition=func_def,
                    user_prompt=prompt.prompt
                    )
            self._set_function_calling(
                    function_definition=func_def,
                    prompt=prompt,
                    parameters=parameters,
                    )
        return self._get_functions_calling()

    def _get_doc(
            self,
            functions_definition: list[FunctionDefinition]
            ) -> list[FunctionDoc]:
        return [{"name": fun.name, "description": fun.description}
                for fun in functions_definition]

    def _get_func_def(
            self,
            function_name: FunctionNameStr
            ) -> FunctionDefinition | None:
        for function in self.functions_definition:
            if function.name == function_name:
                return function
        return None

    def _set_function_calling(self,
                              function_definition: FunctionDefinition,
                              prompt: Prompt,
                              parameters: Parameters
                              ) -> None:
        function_calling: FunctionCalling = FunctionCalling(
                prompt=prompt.prompt,
                name=function_definition.name,
                parameters=parameters
                )
        _ = self._add_function_calling(
                function_calling=function_calling
                )

    def _add_function_calling(self, function_calling: FunctionCalling) -> None:
        self._functions_calling.append(function_calling)

    def _get_functions_calling(self) -> list[FunctionCalling]:
        return self._functions_calling

    def _init_trie(self, model: Model) -> PrefixTrie:
        return PrefixTrie.insert_many([
            model.encode_string(fun.name) + model.encode_string('"')
            for fun in self.functions_definition
                ])


__all__ = ["Generator", "FunctionDefinition", "Prompt"]
