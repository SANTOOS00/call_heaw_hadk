from ..prefixtrie import PrefixTrie
from ..model import Model


from typing import TypeAlias
from enum import Enum
import numpy as nu


FunctionNameStr: TypeAlias = str
TokenID: TypeAlias = int


FunctionDoc:  TypeAlias = dict[str, str]
Score: TypeAlias = float


class Prompt(str, Enum):
    """Store templates used to ask the model to select a function name."""

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
        """Build a routing prompt from a user request and function
        documentation.

        Args:
            user_prompt: Natural-language request to route to a function.
            functions_doc: Name and description
            records for available functions.

        Returns:
            Prompt text with the request and function documentation inserted.
        """
        return Prompt.Prompt_Function_Name.value.replace(
                        "{USER_PROMPT}", user_prompt
                ).replace(
                        "{FUNCTION_DOC}", "\n".join([
                            f"{fun}" for
                            fun in functions_doc
                            ])
                )


class FunctionName:
    """Generate a valid function name using model scores and a prefix trie."""

    def __init__(self,
                 model: Model,
                 trie: PrefixTrie,
                 functions_doc: list[FunctionDoc]
                 ) -> None:
        """Initialize the constrained function-name generator.

        Args:
            model: Model used to encode prompts, score tokens, and decode
            results.
            trie: Trie that constrains generated tokens to valid function
            names.
            functions_doc: Documentation for functions available to the router.
        """
        self._model: Model = model
        self._trie: PrefixTrie = trie
        self._function_doc: list[FunctionDoc] = functions_doc

    def generator(self, user_prompt: str) -> str:
        """Select the best matching function name for a user prompt.

        Args:
            user_prompt: Natural-language request to route.

        Returns:
            Decoded name of the highest-scoring valid function.
        """
        model: Model = self._model

        prompt: str = Prompt.builder_prompt(
                user_prompt=user_prompt,
                functions_doc=self._function_doc)
        context_window: list[TokenID] = model.encode_string(prompt)
        tokens: list[TokenID] = []
        while True:
            tokens_possible: list[TokenID] = self._trie.get_childrens(
                    tokens=tokens
                    )
            if len(tokens_possible) == 0:
                break
            logits: list[Score] = model.mask_logits(
                    tokens_possible, context_window
                    )
            token: TokenID = TokenID(nu.argmax(logits))
            tokens.append(token)
            context_window.append(token)
            if self._trie.search(
                    token_ids=tokens
                    ):
                break
        return str(model.decode(tokens[:-1]))


__all__ = ["FunctionName", "FunctionNameStr", "FunctionDoc"]
