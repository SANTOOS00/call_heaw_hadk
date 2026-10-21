from typing import TypeAlias, Literal
from pydantic import BaseModel, TypeAdapter


TypeArgs = Literal["number", "boolean", "integer", "string"]
Value: TypeAlias = int | str | float | bool


class Type(BaseModel):
    type: TypeArgs


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Type]
    returns: Type


class Prompt(BaseModel):
    prompt: str


class FunctionCalling(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Value]


AdapterFunctionDefinition = TypeAdapter(list[FunctionDefinition])
AdapterPrompt = TypeAdapter(list[Prompt])
AdapterFunctionCalling = TypeAdapter(list[FunctionCalling])


__all__ = [
        "FunctionDefinition",
        "Prompt",
        "FunctionCalling",
        "AdapterFunctionDefinition",
        "AdapterPrompt",
        "AdapterFunctionCalling"
        ]
