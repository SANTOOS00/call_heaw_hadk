from typing import TypeAlias, Literal
from pydantic import BaseModel, TypeAdapter
from pathlib import Path
import os

TypeArgs = Literal["number", "boolean", "integer", "string"]
Value: TypeAlias = int | str | float | bool


class Type(BaseModel):
    """Describe the primitive type accepted by a
    function parameter or return value.

    Attributes:
        type: Name of the supported primitive type.
    """

    type: TypeArgs


class FunctionDefinition(BaseModel):
    """Define a callable function exposed to the generator.

    Attributes:
        name: Unique function name used for selection and invocation.
        description: Human-readable explanation of the function's purpose.
        parameters: Mapping of parameter names to their type descriptions.
        returns: Type description of the function's return value.
    """

    name: str
    description: str
    parameters: dict[str, Type]
    returns: Type


class Prompt(BaseModel):
    """Represent a user prompt to be resolved into a function call.

    Attributes:
        prompt: Natural-language request from the user.
    """

    prompt: str


class FunctionCalling(BaseModel):
    """Represent a generated function invocation.

    Attributes:
        prompt: User prompt that produced the invocation.
        name: Name of the selected function.
        parameters: Concrete argument values for the function call.
    """

    prompt: str
    name: str
    parameters: dict[str, Value]


AdapterFunctionDefinition = TypeAdapter(list[FunctionDefinition])
AdapterPrompt = TypeAdapter(list[Prompt])
AdapterFunctionCalling = TypeAdapter(list[FunctionCalling])


def product_json(
        path: Path,
        functions_calling: list[FunctionCalling]
        ) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with path.open('w', encoding='utf-8') as fb:
        json_data = AdapterFunctionCalling.dump_json(
                functions_calling,
                indent=2
                ).decode(
                        "utf-8"
                        )
        fb.write(json_data)


__all__ = [
        "FunctionDefinition",
        "Prompt",
        "FunctionCalling",
        "AdapterFunctionDefinition",
        "AdapterPrompt",
        "AdapterFunctionCalling",
        "product_json"
        ]
