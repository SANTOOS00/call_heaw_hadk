from typing import NewType


FunctionName = NewType('FunctionName', str)


class Node:
    def __init__(self) -> None:
        self.node: dict[int, Node] = dict()
        self.is_finished = False


class PrefixTrie:
    def __init__(self) -> None:
        self._root_node = Node()


    def set_trie(self, token_ids: list[int]) -> None:
        root_node: Node = self._root_node
        for id_token in token_ids:
            if id_token not in root_node.node.keys():
                root_node.node[id_token] = Node()
            root_node = root_node.node[id_token]
        root_node.is_finished = True


    def get_children(self, tokens: list[int]) -> list[int]:
        root_node = self._root_node
        for id_token in tokens:
            if id_token not in root_node.node.keys():
                return []
            root_node = root_node.node[id_token]
        return [root_node.node.keys()]






__all__ = ["PrefixTrie"]

