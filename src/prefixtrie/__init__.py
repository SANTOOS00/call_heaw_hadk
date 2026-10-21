from typing import TypeAlias, Self


FunctionName: TypeAlias =  str


class Node:
    def __init__(self) -> None:
        self.node: dict[int, Node] = dict()
        self.is_finished: bool = False


class PrefixTrie:
    def __init__(self) -> None:
        self._root_node: Node = Node()

    def _insert(self, token_ids: list[int]) -> None:
        root_node: Node = self._root_node
        for id_token in token_ids:
            if id_token not in root_node.node.keys():
                root_node.node[id_token] = Node()
            root_node = root_node.node[id_token]
        root_node.is_finished = True

    def get_childrens(self, tokens: list[int]) -> list[int]:
        root_node: Node = self._root_node
        for id_token in tokens:
            if id_token not in root_node.node.keys():
                return []
            root_node = root_node.node[id_token]
        return list(root_node.node.keys())

    @classmethod
    def insert_many(cls, tokens_ids: list[list[int]]) -> Self:
        instance: PrefixTrie = cls()
        for ids in tokens_ids:
            instance._insert(
                    token_ids=ids
                    )
        return instance

    def search(self, token_ids: list[int]) -> bool:
        print(token_ids)
        root_node: Node = self._root_node
        for id in token_ids:
            if id not in root_node.node.keys():
                return False
            root_node = root_node.node[id]
        return root_node.is_finished


__all__ = ["PrefixTrie"]
