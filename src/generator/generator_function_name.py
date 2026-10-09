from typing import TypeAlias, NewType
from ..prefixtrie import PrefixTrie
from enum import Enum
FunctionNameStr: NewType = NewType("FunctionNameStr", str)
FunctionDoc:  TypeAlias = dict[str, str]


class Prompt(str, Enum):
    Prompt_Function_Name = """
    user prompt: 
    {USER_PROMPT}
    functions defintions:
    {FUNCTION_DOC}
    function name:
"""
class FunctionName:
    def __init__(self, trie: PrefixTrie, function_doc: list[FunctionDoc] | None = None) -> None:
        self.trie: PrefixTrie = trie
        self.function_doc: list[FunctionDoc] | None = function_doc

    def generator(self, user_prompt: str) -> str:
        return user_prompt

    def builder_prompt(self, user_prompt: str) -> str:
        return Prompt.Prompt_Function_Name.value.replace(
                "{USER_PROMPT}", user_prompt
                )

__all__ = ["FunctionName", "FunctionNameStr"]

