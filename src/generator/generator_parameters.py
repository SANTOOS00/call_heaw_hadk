from .dataschema import FunctionDefinition 
from ..model import Model
from typing import TypeAlias
import numpy as nu
from enum import Enum


Parameters: TypeAlias = dict[str, int | float | str | bool]
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
   example: {
        "prompt": "Greet john",
        "function_prototype": "fn_greet(name: string)",
        "function_description": "Generate a greeting message for a\
            person by name.",
        "parameters": {
            "name": "john",
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
        START = "Start Cell"
        SIGN = "Sign Cell"
        DECIMAL = "Decimal Cell"
        FRACTIONAL = "Fractional Cell"
        END = "End Part"

    class StateString(Enum):
        START = "Start Cell"
        ESCAPE = "Escape Cell"
        CONTEXT = "Context Cell"
        END = "End Cell"

    def get_state_number(self, number: str) -> StateNumber:
        state: FSM.StateNumber = self.StateNumber.START
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

    def get_state_string(self, string: str) -> StateString:
        state: FSM.StateString = self.StateString.START
        for ch in string:
            match state:
                case self.StateString.START:
                    if ch == '\\':
                        print('ssssss')
                        state = self.StateString.ESCAPE
                    elif ch == '"':
                        state = self.StateString.CONTEXT
                case self.StateString.CONTEXT:
                    if ch == '"':
                        return self.StateString.END
                case _:
                    ...
        return state


    def get_step_boolean(self) -> bool:
        pass

class GeneratorParameters:
    def __init__(self, model: Model)-> None:
        self._model: Model = model
        self._fsm: FSM = FSM()
        self._context_window: list[TokenID]

    def generator(self,
                  function_definition: FunctionDefinition,
                  user_prompt: str) -> Parameters:
        parameters: Parameters = dict()
        model = self._model
        prompt: str = Prompt.builder_prompt(
                user_prompt=user_prompt,
                function_definition=function_definition)
        self._context_window = model.encode_string(
                string=prompt
                )
        for parameter, typearg in function_definition.parameters.items():
            self._set_token_name_arg(
                    parameter=parameter,
                    number_parameters=len(function_definition.parameters)
                    )
            match typearg.type:
                case "number":
                    parameters[parameter] = self._number()
                case "integer":
                    parameters[parameter] = int(self._number())
                case "string":
                    parameters[parameter] = self._string()
                case "boolean":
                    parameters[parameter] = self._boolean()
                case _:
                    ...
            print(parameters)
        return parameters
    def _string(self) -> str:
        model: Model = self._model
        tokens_generator: list[TokenID] = []
        fsm: FSM = self._fsm
        while True:
            logits: list[Score] = model.get_logits_from_input_ids(self._context_window)
            token: TokenID = TokenID(nu.argmax(logits))
            tokens_generator.append(token)
            self._add_token_in_window_context(token)
            tokens_string: str = model.decode(tokens_generator)
            state: FSM.StateString = fsm.get_state_string(
                    string=tokens_string
                    )
            
            if FSM.StateString.END == state:
                if '"' in tokens_string:
                    index = tokens_string.index('"')
                    tokens_string = tokens_string[index + 1:]
                    index = tokens_string.index('"')
                    tokens_string = tokens_string[:index]
                break
        return tokens_string

    def boolean(self) -> bool:
       pass

    def _number(self) -> float:
        model: Model = self._model
        tokens_generator: list[TokenID] = []
        fsm: FSM = self._fsm
        while True:
            token_possible: list[int] | None = self._get_token_possible_for_number(
                    number=self._model.decode(tokens_generator)
                    )
            if token_possible is None:
               break 
            logits: list[Score] = model.mask_logits(
                    token_possible=token_possible,
                    window_context=self._context_window
                    )
            token: TokenID = TokenID(nu.argmax(logits))
            self._add_token_in_window_context(
                    token_id=token
                    )
            tokens_generator.append(token)

        return float(model.decode(tokens_generator).rstrip(","))

    def _add_token_in_window_context(
            self,
            token_id: TokenID
            ) -> None: 
        self._context_window.append(token_id)
    
    def _set_token_name_arg(
            self,    
            parameter: str,
            number_parameters: int
            ) -> None:
            if number_parameters == 0:
                self._context_window += self._model.encode_string( 
                        f"\"{parameter}\": "
                        )        
            else:
                self._context_window += self._model.encode_string(
                        f" \"{parameter}\": " 
                        )

    def _get_token_possible_for_number(self, number: str) -> list[int] | None:
        fsm: FSM = self._fsm
        state: FSM.StateNumber = fsm.get_state_number(
                number=number
                )
        match state:
            case FSM.StateNumber.START:
                return self._model.encode_char_char("+-")
            case FSM.StateNumber.DECIMAL:
                return self._model.encode_char_char("0123456789.,")
            case FSM.StateNumber.FRACTIONAL:
                return self._model.encode_char_char("0123456789,")
            case FSM.StateNumber.SIGN:
                return self._model.encode_char_char("0123456789")
            case FSM.StateNumber.END:
                return None

__all__ = ["GeneratorParameters", "Parameters"]

