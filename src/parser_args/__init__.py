from pathlib import Path


class _ParserError(Exception):
    ...


class Parser:
    def __init__(self, args: list[str]) -> None:
        self.functions_definition: Path = Path(
                "data/input/functions_definition.json"
                )
        self.output: Path = Path(
                "data/output/function_calls.json"
                )
        self.input: Path = Path(
                "data/input/function_calling_tests.json"
                )
        _ = self._set_paths(
                args=args
                )

    def _set_paths(self, args: list[str]) -> None:
        for i, arg in enumerate(args, start=1):
            if len(args) > i and i % 2 != 0:
                match arg:
                    case "--functions_definition":
                        self.functions_definition = self._set_path(
                                path_arg=args[args.index(arg) + 1]
                                )
                    case "--input":
                        self.input = self._set_path(
                                path_arg=args[args.index(arg) + 1]
                                )
                    case "--output":
                        self.output = self._set_path(
                                path_arg=args[args.index(arg) + 1]
                                )
                    case _:
                        raise _ParserError(
                                "[Error]: Unknown argument: {arg}"
                                )

    def _set_path(self, path_arg: str) -> Path:
        return Path(path_arg)


__all__ = ["Parser"]
