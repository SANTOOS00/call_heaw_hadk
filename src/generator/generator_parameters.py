from .dataschema import FunctionDefinition 
from ..model import Model
from typing import NewType, TypeAlias
import numpy as nu
from enum import Enum, auto

Parameters = NewType('PARAMETERS',
                     dict[str, int | float | str | bool])
TokenID: TypeAlias = int

Score: TypeAlias = float



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
        START = "Start Part"
        SIGN = "Sign Part"
        DECIMAL = "Decimal Part"
        FRACTIONAL = "Fractional Part"
        END = "End Part"

    class StateString(Enum):
        pass

    def __init__(self) -> None:
        ...

    def get_state_number(self, number: str) -> StateNumber:
        state: self.StateNumber = self.StateNumber.START
        for ch in number:
            match state:
                case self.StateNumber.START:
                    if ch in "-+":
                        state = self.StateNumber.SIGN
                    else:
                        state = self.StateNumber.DECIMAL
                case self.StateNumber.SIGN:
                    state = self.StateNumber.DECIMAL
                case self.StateNumber.DECIMAL:
                    if ch == '.':
                        state = self.StateNumber.FRACTIONAL
                    elif ch == ',':
                        state = self.StateNumber.END
                    else:
                        pass
                case self.StateNumber.FRACTIONAL:
                    if ch == ',':
                        state = self.StateNumber.END
                case self.StateNumber.END:
                    return state
        return state


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
            self._context_window += model.encode_string(f"\"{parameter}\": ")

            match typearg.type:
                case "number":
                    parameters['number'] = self._number()
                case "integer":
                    parameters['integer'] = int(self._number())
                case _:
                    pass
            print(model.decode(self._context_window))

    
    def _number(self) -> float:
        model: Model = self._model
        token_valid: list[TokenID] = []
        fsm: FSM = self._fsm
        while True:
            token_possible: list[int] = self._get_token_possible_for_number(
                    number=self._model.decode(token_valid)
                    )
            if len(token_possible) == 0:
               break 
            logits: list[Score] = model.mask_logits(
                    token_possible=token_possible,
                    window_context=self._context_window
                    )
            token: TokenID = nu.argmax(logits)
            self._add_token_in_window_context(
                    token_id=token
                    )
            token_valid.append(token)
            state_fsm: FSM.StateNumber = fsm.get_state_number(model.decode(token_valid))
            if FSM.StateNumber.END == state_fsm:
                break

        return float(model.decode(token_valid).rstrip(","))

    def _add_token_in_window_context(self, token_id: TokenID) -> None:
        self._context_window.append(token_id)

    def _get_token_possible_for_number(self, number: str) -> list[int]:
        fsm: FSM = self._fsm
        state: FSM.StateNumber = fsm.get_state_number(
                number=number
                )
        match state:
            case FSM.StateNumber.START:
                return self._model.encode_char_char("+-0123456789")
            case FSM.StateNumber.DECIMAL:
                return self._model.encode_char_char("0123456789.,")
            case FSM.StateNumber.FRACTIONAL:
                return self._model.encode_char_char("0123456789,")
            case FSM.StateNumber.SIGN:
                return self._mode.encode_char_char("0123456789")
            case FSM.StateNumber.END:
                return []
            case _:
                pass
        return []

__all__ = ["GeneratorParameters", "Paramters"]

