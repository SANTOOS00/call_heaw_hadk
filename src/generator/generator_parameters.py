from .dataschema import FunctionDefinition 
from ..model import Model
from typing import NewType, TypeAlias
from enum import Enum

Parameters = NewType('PARAMETERS',
                     dict[str, int | float | str | bool])
TokenID: TypeAlias = int




class Prompt(str, Enum):
    Prompt = """you are a strict function-parameter extractor.
    example:
    {
        "prototype": "fn_add_numbers("a": number, "b", number)",
        "user_prompt": "What is the sum of 2 and 3?"
        "description": "Add two numbers together and return their sum.",
        "parameters": {
            "a": 2.0,
            "b": 3.0
            }
    }
    output:
    {
        "prototype": "{PROTOTYPE}",
        "user_prompt": "{USER_PROMPT}"
        "description": "{DESCRIPTION}",
        "parameters": {{PARAMETERS}"""

    @staticmethod
    def builder_prompt(user_prompt: str) -> str:
        return Prompt.Prompt.value.replace(
                "{USER_PROMPT}", user_prompt
        )

class FSM:
    def __init__(self) -> None:
        ...

    def get_step_number(self) -> float | int:
        pass 

    def get_step_string(self) -> str:
        pass


    def get_step_boolean(self) -> bool:
        pass

class GeneratorParameters:
    def __init__(self, model: Model)-> None:
        self._model = model
        self._fsm: FSM = FSM()
        self._context_window: list[ToeknID]

    def generator(self,
                  function_definition: FunctionDefinition,
                  user_prompt: str) -> str:
        parameters: Paramerts = dict()
        model = self._model
        prompt: str = Prompt.builder_prompt(user_prompt=user_prompt)
        self._context_window = model.encode_string(
                string=prompt
                )
        for parameter, typearg in function_definition.parameters.items():
            match typearg:
                case "number":
                    parameters['number'] = self._number()
                case "integer":
                    parameters['integer'] = int(self._number())
                case _:
                    pass

    def _number(self) -> float:
        pass

__all__ = ["GeneratorParameters", "Paramters"]

