from typing import NewType
from .dataschema import FunctionDefinition 

Parameters = NewType('PARAMETERS',
                     dict[str, int | float | str | bool])




class FSM:
    def __init__(self) -> None:
        pass

    def number(self) -> float | int:
        pass

    def string(self) -> str:
        pass


    def boolean(self) -> bool:
        pass

class GeneratorParameters:
    def __init__(self)-> None:
        self._fsm: FSM = FSM()

    def generator(self, function_definition: FunctionDefinition) -> str:
        parameters: Paramerts = dict()
        fsm: FSM = self._fsm
        for parameter in function_definition.parameters:
            print(parameter)

__all__ = ["GeneratorParameters", "Paramters"]
