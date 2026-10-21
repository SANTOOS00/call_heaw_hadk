from .generator import Generator, FunctionDefinition, Prompt
from .generator.dataschema import AdapterFunctionDefinition, AdapterPrompt
from .model import Model
from .parser_args import Parser


import sys
from pydantic import ValidationError
from pathlib import Path


class ParserError(Exception):
    ...


def get_functionsdefinition(
        path: Path,
        ) -> list[FunctionDefinition]:
    try:
        with path.open() as fp:
            return AdapterFunctionDefinition.validate_json(fp.read())
    except ValidationError:
        raise ParserError(
                "[ERROR]: Invalid JSON structure for functions definition."
                )
    except Exception:
        raise ParserError(
                "[ERROR]: Failed to read functions definition file."
                )


def get_prompts(
        path: Path
        ) -> list[Prompt]:
    try:
        with path.open() as fp:
            return AdapterPrompt.validate_json(fp.read())
    except ValidationError:
        raise ParserError(
                "[ERROR]: Invalid JSON structure for prompts."
                )
    except Exception:
        raise ParserError(
                "[ERROR]: Failed to read prompts file."
                )


def main() -> None:
    args: Parser = Parser(
            args=sys.argv[1:]
            )
    model: Model = Model()
    _ = Generator(
            model=model,
            prompts=get_prompts(
                path=args.input
                ),
            functions_definition=get_functionsdefinition(
                path=args.functions_definition
                ),
            ).run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
