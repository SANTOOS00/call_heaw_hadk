import sys


class CallError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = self.__formate_error(message)
    
    def print(self) -> None:    
        print(self.message, file=sys.stderr)

    def __formate_error(self, message) -> str:
        return f"[ERROR]: {message}"



__all__ = ["CallError"]

