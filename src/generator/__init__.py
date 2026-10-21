from .dataschema import FunctionDefinition, Prompt, FunctionCalling
from ..prefixtrie import PrefixTrie
from .generator_function_name import FunctionName, FunctionNameStr, FunctionDoc
from .generator_parameters import GeneratorParameters, Parameters
from ..model import Model


import sys


class Generator:
    """Generate function calls from prompts and available function definitions.

    The generator selects a matching function name, produces its parameters,
    and accumulates the resulting function calls.
    """

    def __init__(
        self,
        model: Model,
        prompts: list[Prompt],
        functions_definition: list[FunctionDefinition]
    ) -> None:
        """Initialize the generator and its supporting generators.

        Args:
            model: Model used to encode function names and generate selections.
            prompts: User prompts for which to generate function calls.
            functions_definition: Definitions of the callable functions.
        """

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

    def run(self) -> list[FunctionCalling]:
        """Generate a function call for every configured prompt.

        Returns:
            Generated function calls in the same order as the prompts.

        Raises:
            SystemExit: If a generated function name has no matching
            definition.
        """
        generator_name: FunctionName = self._generator_function_name
        generator_parameters: GeneratorParameters = self._generator_parameters

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
        """Extract function names and descriptions from definitions.

        Args:
            functions_definition: Definitions from which to extract
            documentation.

        Returns:
            Documentation records containing each function
            name and description.
        """
        return [{"name": fun.name, "description": fun.description}
                for fun in functions_definition]

    def _get_func_def(
            self,
            function_name: FunctionNameStr
            ) -> FunctionDefinition | None:
        """Find the configured definition for a function name.

        Args:
            function_name: Name of the function to look up.

        Returns:
            The matching definition, or ``None`` when it is unavailable.
        """
        for function in self.functions_definition:
            if function.name == function_name:
                return function
        return None

    def _set_function_calling(self,
                              function_definition: FunctionDefinition,
                              prompt: Prompt,
                              parameters: Parameters
                              ) -> None:
        """Create and store a function call from generated values.

        Args:
            function_definition: Definition of the selected function.
            prompt: Prompt that resulted in the function call.
            parameters: Generated parameters for the selected function.
        """
        function_calling: FunctionCalling = FunctionCalling(
                prompt=prompt.prompt,
                name=function_definition.name,
                parameters=parameters
                )
        self._add_function_calling(
                function_calling=function_calling
                )

    def _add_function_calling(self, function_calling: FunctionCalling) -> None:
        """Append a generated function call to the accumulated results.

        Args:
            function_calling: Function call to store.
        """
        self._functions_calling.append(function_calling)

    def _get_functions_calling(self) -> list[FunctionCalling]:
        """Return all generated function calls accumulated so far.

        Returns:
            The mutable list of accumulated function calls.
        """
        return self._functions_calling

    def _init_trie(self, model: Model) -> PrefixTrie:
        """Build a prefix trie containing the configured function names.

        Args:
            model: Model used to encode each function name.

        Returns:
            A trie populated with encoded function-name prefixes.
        """
        return PrefixTrie.insert_many([
            model.encode_string(fun.name) + model.encode_string('"')
            for fun in self.functions_definition
                ])


__all__ = ["Generator", "FunctionDefinition", "Prompt"]
