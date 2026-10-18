
from pathlib import Path
from argparse import ArgumentParser, Namespace


class ParserError(Exception):
    ...


def valid_path(arg_path: str) -> Path:
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
            help="hello in not valid for valu"
            )
    return parser.parse_args()

__all__ = ["get_args"]
