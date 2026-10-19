from .generator import Generator, FunctionDefinition, Prompt
from .model import Model


from pydantic import TypeAdapter, ValidationError
from typing import cast
from pathlib import Path
from argparse import ArgumentParser, Namespace


AdapterFunctionDefinition = TypeAdapter(list[FunctionDefinition])
AdapterPrompt = TypeAdapter(list[Prompt])


class ParserError(Exception):
    ...


def valid_path(arg_path: str) -> None:
    path: Path = Path(arg_path)
    if path.exists():
        raise ParserError(
                f"[ERROR]: path is not valid {arg_path}"
                )
    return path

def get_args() -> Namespace:
    parser = ArgumentParser()

    _ = parser.add_argument(
            "--functions_definition",
            type=valid_path,
            )
    _ = parser.add_argument(
            "--input",
            type=valid_path,
            )
    _ = parser.add_argument(
            "--output",
            type=valid_path,
            )
    return parser.parse_args()


def get_functionsdefinition(
        path: Path,
        ) -> list[FunctionDefinition]:
    try:
        with path.open() as fp:   
            return AdapterFunctionDefinition.validate_json(fp.read())
    except:
        raise ParserError(
                ""
                )


def get_prompts(
        path: Path
        ) -> list[Prompt]:
    try: 
        with path.open() as fp:
            adapter: TypeAdapter[list[Prompt]] = TypeAdapter(list[Prompt])
            return adapter.validate_json(fp.read())

    except ValidationError:
        raise ParserError(
                ""
                )


def main() -> None:
    model: Model = Model()
    args: Namespace = get_args()

    _ = Generator(
            model=model,
            prompts=get_prompts(
                path=Path(args.output)
                ),
            functions_definition= get_functionsdefinition(
                path=Path(args.functions_definition)
                )
            ).run()


if __name__ == "__main__":
    main()

