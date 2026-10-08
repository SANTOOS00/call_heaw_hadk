from .error import CallError
from .generator import Generator, FunctionDefinition, Prompt
from .prefixtrie import PrefixTrie
from .model import Model

import json
import argparse

class Json():
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
                    prog='ProgramName')
        #self.__add_args()

    def __add_args(self) -> None:
        self.parser.add_argument(
                "--functions_definition"
                )
        self.parser.add_argument(
                "--input"
                )
        self.parser.add_argument(
                "--ouput"
                )

    def get_functions_definition(self) -> list[FunctionDefinition]:
        with open("data/input/functions_definition.json", 'r') as data:
            functions_definition: list[dict[str, str]] = json.load(data)
        return [FunctionDefinition(**fundefinition) for fundefinition in functions_definition]

    def get_prompts(self) -> list[Prompt]:
        with open("data/input/function_calling_tests.json", 'r') as data:
            prompts:  dict[str, str] = json.load(data)
        return [Prompt(**prompt) for prompt in prompts]


def create_prefixtrie(
        functions_name_ids: list[list[int]]
        ) -> PrefixTrie:
    trie = PrefixTrie()
    print(functions_name_ids)
    for token_ids in functions_name_ids:
        trie.set_trie(token_ids)
    return trie


def main() -> None:
    data = Json()
    model = Model() 
    functions_definition = data.get_functions_definition()
    Generator(
            trie=create_prefixtrie([model.encode(fun.name) for fun in functions_definition]),
            prompts=data.get_prompts(),
            functions_definition=data.get_functions_definition()
            ).run()

if __name__ == "__main__":
    try:
        main()
    except CallError as e:
        e.print()

