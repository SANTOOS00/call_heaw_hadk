from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]


from typing import TypeAlias


TokenID: TypeAlias = int
ModelName: TypeAlias = str


class Model(Small_LLM_Model):
    def __init__(self,
                 model_name: ModelName = "Qwen/Qwen3-0.6B",
                 ) -> None:
        super().__init__(model_name=model_name)

    def encode_string(self, string: str) -> list[int]:
        return [int(token_id) for token_id in super().encode(string)[0]]

    def mask_logits(
            self,
            token_possible: list[int],
            window_context: list[int]
            ) -> list[float]:

        logits: list[float] = self.get_logits_from_input_ids(window_context)
        for token_id, _ in enumerate(logits):
            if token_id not in token_possible:
                logits[token_id] = float('-inf')
        return logits

    def encode_char_char(self, token_str: str) -> list[TokenID]:
        tokens: list[TokenID] = []
        for char in token_str:
            tokens.append(TokenID(self.encode(char)[0]))
        return tokens


__all__ = ["Model"]
