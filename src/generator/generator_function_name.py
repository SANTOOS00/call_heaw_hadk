from ..prefixtrie import PrefixTrie
from ..model import Model


from typing import TypeAlias, NewType
from enum import Enum
import numpy as nu


FunctionNameStr: NewType = NewType("FunctionNameStr", str)
TokenID: NewType = NewType("TokenID", int)

FunctionDoc:  TypeAlias = dict[str, str]
Score: TypeAlias = float


class Prompt(str, Enum):
    Prompt_Function_Name = """You are a precise function router.
FUNCTIONS DEFINITIONS:
{FUNCTION_DOC}
USER PROMPT:
{USER_PROMPT}

FUNCTION NAME:"""

    @staticmethod
    def builder_prompt(
            user_prompt: str,
            functions_doc: list[FunctionDoc]
            ) -> str:
        docs = {}
        return Prompt.Prompt_Function_Name\
                .value.replace(
                "{USER_PROMPT}", user_prompt
                ).replace(
                        "{FUNCTION_DOC}","\n".join([f"{fun}" for fun in functions_doc])
                )

class FunctionName:
    def __init__(self,
                 model: Model,
                 trie: PrefixTrie,
                 functions_doc: list[FunctionDoc]
                 ) -> None:
        self._model: Model = model
        self._trie: PrefixTrie = trie
        self._function_doc: list[FunctionDoc] = functions_doc

    def generator(self, user_prompt: str) -> str:
        model: Model = self._model

        prompt: str = Prompt.builder_prompt(
                user_prompt,
                functions_doc=self._function_doc)
        context_window: list[TokenID] = model.encode_string(prompt)
        token_valid: list[TokenID] = []
        while True:
            tokens_possible: list[TokenID] = self._trie.git_childrens(token_valid)
            if len(tokens_possible) == 0:
                break
            logits: list[Score] = model.mask_logits(
                    tokens_possible, context_window
                    )
            token: TokenID = nu.argmax(logits)
            token_valid.append(token)
            context_window.append(token)

        return model.decode(token_valid)

__all__ = ["FunctionName", "FunctionNameStr", "FunctionDoc"]

