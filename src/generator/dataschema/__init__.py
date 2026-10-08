from typing import NewType
from pydantic import BaseModel


TypeArgs = NewType("TypeArgs", int | float | bool | str)


class Type(BaseModel):
    type: TypeArgs


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Type]
    returns: Type


class Prompt(BaseModel):
    prompt: str

__all__ = ["FunctionDefinition", "Prompt"]

