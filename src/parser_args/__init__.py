from pathlib import Path


class _ParserError(Exception):
    """Raise when command-line arguments contain an unsupported option."""

    ...


class Parser:
    """Parse command-line options for input files,
    output files, and model choice."""

    def __init__(self, args: list[str]) -> None:
        """Initialize parser defaults and apply
        supplied command-line arguments.

        Args:
            args: Alternating command-line option names and their values.

        Raises:
            _ParserError: If an option name is not recognized.
        """
        self.functions_definition: Path = Path(
                "data/input/functions_definition.json"
                )
        self.output: Path = Path(
                "data/output/function_calls.json"
                )
        self.input: Path = Path(
                "data/input/function_calling_tests.json"
                )
        self.model_name: str = "Qwen/Qwen3-0.6B"

        self._set_paths(
                args=args
                )

    def _set_paths(self, args: list[str]) -> None:
        """Update parser settings from alternating option names and values.

        Args:
            args: Alternating command-line option names and their values.

        Raises:
            _ParserError: If an option name is not recognized.
        """
        for i, arg in enumerate(args, start=1):
            if i % 2 != 0:
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
                    case "--model_name":
                        self.model_name = args[args.index(arg) + 1]
                    case _:
                        raise _ParserError(
                                f"[Error]: Unknown argument: {arg}"
                                )
        return None

    def _set_path(self, path_arg: str) -> Path:
        """Convert a command-line path value into a ``Path`` instance.

        Args:
            path_arg: Path value supplied on the command line.

        Returns:
            Path representation of the supplied value.
        """
        return Path(path_arg)


__all__ = ["Parser"]
