from llm_sdk import Small_LLM_Model


from typing import NewType


TokenID: NewType = NewType("TokenID", int)

class Model(Small_LLM_Model):
    def encode_string(self, string: str) -> list[int]:
        return [int(token_id) for token_id in super().encode(string)[0]]

    def mask_logits(self, token_possible: list[int], window_context: list[int]) -> list[float]:
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
