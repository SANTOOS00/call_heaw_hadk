from typing import TypeAlias, NewType, cast
from ..prefixtrie import PrefixTrie
from enum import Enum
FunctionNameStr: NewType = NewType("FunctionNameStr", str)
FunctionDoc:  TypeAlias = dict[str, str]


class Prompt(Enum, str):
    Prompt = """
    user prompt: 
    {USER_PROMPT}
    functions defintions:
    {FUNCTION_DOC}
    function name:
"""
    
class FunctionName:
    def __init__(self, trie: PrefixTrie, function_doc: list[FunctionDoc] | None = None) -> None:
        self.trie: PrefixTrie = trie
        self.function_doc: list[FunctionDoc] = function_doc

    def generator(self, user_prompt: str) -> str:
        return user_prompt
        

__all__ = ["FunctionName", "FunctionNameStr"]

