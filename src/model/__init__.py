from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]


from typing import TypeAlias


TokenID: TypeAlias = int
ModelName: TypeAlias = str


class Model(Small_LLM_Model):
    """Adapt the underlying LLM SDK for constrained token generation."""

    def __init__(self,
                 model_name: ModelName,
                 ) -> None:
        """Initialize the underlying language model.

        Args:
            model_name: Identifier of the model to load from the LLM SDK.
        """
        super().__init__(model_name=str(model_name))

    def encode_string(self, string: str) -> list[int]:
        """Encode a string into integer token identifiers.

        Args:
            string: Text to tokenize.

        Returns:
            Token identifiers produced for the input string.
        """
        return [int(token_id) for token_id in super().encode(string)[0]]

    def mask_logits(
            self,
            token_possible: list[int],
            window_context: list[int]
            ) -> list[float]:
        """Mask scores for tokens that are not allowed in the current context.

        Args:
            token_possible: Token identifiers that may be selected.
            window_context: Token identifiers comprising the model context.

        Returns:
            Model logits with disallowed token scores set to negative infinity.
        """

        logits: list[float] = self.get_logits_from_input_ids(window_context)
        for token_id, _ in enumerate(logits):
            if token_id not in token_possible:
                logits[token_id] = float('-inf')
        return logits

    def encode_char_char(self, token_str: str) -> list[TokenID]:
        """Encode each character in a string independently.

        Args:
            token_str: Text whose characters will be encoded individually.

        Returns:
            Token identifier produced for each character.
        """
        tokens: list[TokenID] = []
        for char in token_str:
            tokens.append(TokenID(self.encode(char)[0]))
        return tokens


__all__ = ["Model"]
