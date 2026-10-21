from .generator import (
        Generator,
        FunctionDefinition,
        Prompt,
        )
from .generator.dataschema import (
        AdapterFunctionDefinition,
        AdapterPrompt,
        product_json,
        FunctionCalling
        )
from .model import Model
from .parser_args import Parser


import sys
from pydantic import ValidationError
from pathlib import Path


class _ParserError(Exception):
    """Raise when an input JSON file cannot be read or validated."""

    ...


def get_functionsdefinition(
        path: Path,
        ) -> list[FunctionDefinition]:
    """Load and validate function definitions from a JSON file.

    Args:
        path: Path to the JSON file containing function definitions.

    Returns:
        Validated function definitions from the input file.

    Raises:
        _ParserError: If the file cannot be read or has an invalid structure.
    """
    try:
        with path.open() as fp:
            return AdapterFunctionDefinition.validate_json(fp.read())
    except ValidationError:
        raise _ParserError(
                "[ERROR]: Invalid JSON structure for functions definition."
                )
    except Exception:
        raise _ParserError(
                "[ERROR]: Failed to read functions definition file."
                )


def get_prompts(
        path: Path
        ) -> list[Prompt]:
    """Load and validate prompts from a JSON file.

    Args:
        path: Path to the JSON file containing prompts.

    Returns:
        Validated prompts from the input file.

    Raises:
        _ParserError: If the file cannot be read or has an invalid structure.
    """
    try:
        with path.open() as fp:
            return AdapterPrompt.validate_json(fp.read())
    except ValidationError:
        raise _ParserError(
                "[ERROR]: Invalid JSON structure for prompts."
                )
    except Exception:
        raise _ParserError(
                "[ERROR]: Failed to read prompts file."
                )


def main() -> None:
    """Run the command-line function-call generation workflow.

    The workflow parses options, loads and validates input files,
    initializes the
    model, generates function calls, and writes the result to
    standard output.
    """
    try:
        args: Parser = Parser(
                args=sys.argv[1:]
                )
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    try:
        model: Model = Model(
                model_name=args.model_name
                )
    except Exception as e:
        print(
            f"[ERROR]: {e}",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        functions_calling: list[FunctionCalling] = Generator(
                model=model,
                prompts=get_prompts(
                    path=args.input
                    ),
                functions_definition=get_functionsdefinition(
                    path=args.functions_definition
                    )
                ).run()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    product_json(
            path=args.output,
            functions_calling=functions_calling
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("ok")
