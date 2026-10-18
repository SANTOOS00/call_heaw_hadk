from .generator import Generator, FunctionDefinition, Prompt
from .prefixtrie import PrefixTrie
from .model import Model


from pydantic import TypeAdapter, ValidationError
from typing import TypeVar, cast
from pathlib import Path
from argparse import ArgumentParser, Namespace


T = TypeVar('T')

class ParserError(Exception):
    ...


def valid_path(arg_path: str) -> None:
    path: Path = Path(arg_path)
    if path.exists():
        raise ParserError(
                f"[ERROR]: path is not valid {arg_path}"
                )


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
            adapter: TypeAdapter[list[FunctionDefinition]] = TypeAdapter(list[FunctionDefinition])
            
            return adapter.validate_json(fp.read())

    except:
        pass


def get_prompts(
        path: Path
        ) -> list[Prompt]:
    try:  
        with path.open() as fp:
            adapter: TypeAdapter[list[Prompt]] = TypeAdapter(list[Prompt])
            return adapter.validate_json(fp.read())

    except ValidationError:
        pass


def main() -> None:
    model: Model = Model()
    args: Namespace = get_args()
    

    _ = Generator(
            model=model,
            trie=PrefixTrie(),
            functions_definition=get_functionsdefinition(
                path=Path(cast(str, args.functions_definition))),
            prompts=None
                ).run()


if __name__ == "__main__":
    main()

