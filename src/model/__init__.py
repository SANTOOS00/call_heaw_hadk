from llm_sdk import Small_LLM_Model


class Model(Small_LLM_Model):
    def encode(self, string: str) -> list[int]:
        return [int(token_id) for token_id in super().encode(string)[0]]
