from typing import NewType


PARAMETERS = NewType('PARAMETERS',
                     dict[str, int | float | str | bool])


class GeneratorParameters:
    def __init__(self)-> None:
        pass

    def generator(self) -> str:
        pass
