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
        "parameters": {
            """

    @staticmethod
    def builder_prompt(user_prompt: str, function_definition: FunctionDefinition) -> str:
        prototype: str = '('
        for conut, (parameter, typearg) in enumerate(function_definition.parameters.items()):
            prototype += f"\"{parameter}\": {typearg.type}"
            if len(function_definition.parameters) > conut:
                prototype += ','
        prototype += ')'
        return Prompt.Prompt.value.replace(
                "{USER_PROMPT}", user_prompt
        ).replace(
                "{DESCRIPTION}", function_definition.description
        ).replace(
                "{PROTOTYPE}", function_definition.name + prototype
        )

class FSM:
    class StateNumber(Enum):
        START
        DECIMAL
        INTEGER
        SIGN
        END

    class StateString(Enum):
        pass

    def __init__(self) -> None:
        ...

    def get_state_number(self, number: str) -> float | int:
        state: FSM.StateNumber = FSM.StateNumber.START
        states: FSM.StateNumber = FSM.StateNumber
        for ch in number:
            match state:
                case states.START:
                    if ch in "-+":
                        state = states.SING
                    else:
                        state = states.DECIMAL
                case states.SING:
                        state = states.DECIMAL
                case states.DECIMAL:
                    if ch == '.':
                        state = states.
                    else ch == ',':
                        return states.END
                case 
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
        prompt: str = Prompt.builder_prompt(
                user_prompt=user_prompt,
                function_definition=function_definition)
        self._context_window = model.encode_string(
                string=prompt
                )
        for count, (parameter, typearg) in enumerate(function_definition.parameters.items()):
            if count == 0:
                self._context_window += model.encode_string(f"\"{parameter}\": ")
            else:
                self._context_window += model.encode_string(f", \"{parameter}\": ")

            match typearg.type:
                case "number":
                    parameters['number'] = self._number()
                case "integer":
                    parameters['integer'] = int(self._number())
                case _:
                    pass

    
    def _number(self) -> float:
        model: Model = self._model
        token_valid: list[TokenID] = []
        while True:
            token_possible: list[int] = self._get_token_possible_for_numbers(
                    token_valid=token_valid
                    )
            if len(token_possible) == 0:
                break

    def _get_token_possible_for_numbers(self, number: str) -> list[int]:
        fsm: FSM = self._fsm
        state: FSM.StateNumber = fsm.get_state_numbers(
                number=number
                )
        match state:
            case FSM.StateNumber.START:
                return self._model.encode_byt_byt("+-0123456789")
            case FSM.StateNumber.DEACIMAL:
                return self._model.encode_byt_byt("0123456789")
            case FSM.StateNumber.INTEGER:
                return self._model.encode_byt_byt("0123456789,.")
            case FSM.StateNumber.END:
                return []
__all__ = ["GeneratorParameters", "Paramters"]

