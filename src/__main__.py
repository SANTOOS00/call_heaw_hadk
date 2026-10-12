from .error import CallError
from .generator import Generator, FunctionDefinition, Prompt
from .prefixtrie import PrefixTrie
from .model import Model

import json
from typing import Any



def paraser() -> None:
    pass

def get_functions_definition() -> list[FunctionDefinition]:
    with open("data/input/functions_definition.json", 'r') as data:
        functions_definition: list[dict[str, Any]] = json.load(data)
    return [FunctionDefinition(**fundefinition) for fundefinition in functions_definition]

def get_prompts() -> list[Prompt]:
    with open("data/input/function_calling_tests.json", 'r') as data:
        prompts: list[dict[str, str]] = json.load(data)
    return [Prompt(**prompt) for prompt in prompts]


def create_prefixtrie(functions_name_ids: list[list[int]]) -> PrefixTrie:
    trie = PrefixTrie()
    for token_ids in functions_name_ids:
        trie.set_trie(token_ids)
    return trie


def main() -> None:
    model = Model() 
    functions_definition = get_functions_definition()

    Generator(
            model=model,
            trie=create_prefixtrie([model.encode_string(fun.name)
                                    for fun in functions_definition]),
            prompts=get_prompts(),
            functions_definition=get_functions_definition()
            ).run()


if __name__ == "__main__":
    try:
        main()
    except CallError as e:
        e.print()

