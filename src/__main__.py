from .generator import Generator, FunctionDefinition, Prompt
from .model import Model
from .parser_args import Parser


import sys
from pydantic import TypeAdapter, ValidationError
from pathlib import Path


AdapterFunctionDefinition = TypeAdapter(list[FunctionDefinition])
AdapterPrompt = TypeAdapter(list[Prompt])


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
        with path.open("r") as fp:
            adapter: TypeAdapter[list[Prompt]] = TypeAdapter(list[Prompt])
            return adapter.validate_json(fp.read())

    except ValidationError:
        raise ParserError(
                "[ERROR]: Invalid JSON structure for prompts."
                )
    except Exception as s:
        print(s)
        raise ParserError(
                "[ERROR]: Failed to read prompts file."
                )

def main() -> None:
    args: Parser = Parser(
            args=sys.argv[1:]
            )
    print(args.input)
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
    main()

