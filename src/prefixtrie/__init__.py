from typing import TypeAlias


FunctionName: TypeAlias = str


class Node:
    """Represent a trie node and its token-indexed children."""

    def __init__(self) -> None:
        """Initialize an unfinished node with no children."""
        self.node: dict[int, Node] = dict()
        self.is_finished: bool = False


class PrefixTrie:
    """Store token sequences in a prefix tree for constrained lookup."""

    def __init__(self) -> None:
        """Initialize an empty trie with a root node."""
        self._root_node: Node = Node()

    def _insert(self, token_ids: list[int]) -> None:
        """Insert a token sequence into the trie.

        Args:
            token_ids: Ordered token identifiers that form one complete entry.
        """
        root_node: Node = self._root_node
        for id_token in token_ids:
            if id_token not in root_node.node.keys():
                root_node.node[id_token] = Node()
            root_node = root_node.node[id_token]
        root_node.is_finished = True
        return None

    def get_childrens(self, tokens: list[int]) -> list[int]:
        """Return token identifiers that can follow a prefix.

        Args:
            tokens: Token sequence forming the prefix to inspect.

        Returns:
            Child token identifiers, or an empty list if the prefix is absent.
        """
        root_node: Node = self._root_node
        for id_token in tokens:
            if id_token not in root_node.node.keys():
                return []
            root_node = root_node.node[id_token]
        return list(root_node.node.keys())

    @classmethod
    def insert_many(cls, tokens_ids: list[list[int]]) -> "PrefixTrie":
        """Create a trie populated with multiple token sequences.

        Args:
            tokens_ids: Complete token sequences to insert into the new trie.

        Returns:
            Trie containing every supplied token sequence.
        """
        instance: PrefixTrie = cls()
        for ids in tokens_ids:
            instance._insert(
                    token_ids=ids
                    )
        return instance

    def search(self, token_ids: list[int]) -> bool:
        """Check whether a token sequence is a complete trie entry.

        Args:
            token_ids: Token sequence to look up.

        Returns:
            ``True`` if the sequence exists and ends at a completed entry.
        """
        root_node: Node = self._root_node
        for id in token_ids:
            if id not in root_node.node.keys():
                return False
            root_node = root_node.node[id]
        return root_node.is_finished


__all__ = ["PrefixTrie"]
