from typing import TypeVar, Generic, Callable

# from binary_tree import BinaryTreeNode

T = TypeVar("T")


# heap ordered
## each child is small than or equal to parent
class BinaryTreeNode(Generic[T]):
    def __init__(self, key: T = None, item: T = None) -> None:
        self.key = key
        self.item = item
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return str(self.item)


class BinaryTreeHeap(Generic[T]):
    def __init__(self) -> None:
        self.root = None

    def is_empty(self) -> bool:
        return self.root is None

    def __len__(self) -> int:
        def _len_aux(current: BinaryTreeNode[T]) -> int:
            if current is None:
                return 0
            else:
                return 1 + _len_aux(current.left) + _len_aux(current.right)

        return _len_aux(self.root)

    def preorder(self, f: Callable) -> None:
        def _preorder_aux(current: BinaryTreeNode[T]) -> None:
            if current is not None:
                f(current)
                _preorder_aux(current.left)
                _preorder_aux(current.right)

        _preorder_aux(self.root)

    def inorder(self, f: Callable) -> None:
        def _inorder_aux(current: BinaryTreeNode[T]) -> None:
            if current is not None:
                _inorder_aux(current.left)
                f(current)
                _inorder_aux(current.right)

        _inorder_aux(self.root)

    def postorder(self, f: Callable) -> None:
        def _postorder_aux(current: BinaryTreeNode[T]) -> None:
            if current is not None:
                _postorder_aux(current.left)
                _postorder_aux(current.right)
                f(current)

        _postorder_aux(self.root)

    def __setitem__(self, key: int, value: T) -> None:
        def _setitem_aux(current: BinaryTreeNode[T]) -> None:
            if current is not None:
                if current.item.key == key:
                    current.key, current.item = key, value
                else:
                    _setitem_aux(current.left)
                    _setitem_aux(current.right)

        _setitem_aux(self.root)

    def __getitem__(self, key: int) -> T:
        def _getitem_aux(current: BinaryTreeNode[T]) -> T:
            if current is not None:
                if current.item.key == key:
                    return current.item
                else:
                    return _getitem_aux(current.left) or _getitem_aux(current.right)

        return _getitem_aux(self.root)

    def add(self, key: int) -> None:
        # rise operation
        def _add_aux() -> None:
            pass

    def get_max(self) -> T:
        # sink operation
        def _get_max_aux() -> T:
            pass


if __name__ == "__main__":
    import unittest

    class TestBinaryTree(unittest.TestCase):
        def setUp(self) -> None:
            pass  # TODO

        def test_is_empty(self) -> None:
            self.assertFalse(self.tree.is_empty())

        def test_len(self) -> None:
            self.assertEqual(len(self.tree), 7)

        def test_preorder(self) -> None:
            self.tree.preorder(print)

        def test_inorder(self) -> None:
            self.tree.inorder(print)

        def test_postorder(self) -> None:
            self.tree.postorder(print)

        def test_setitem(self) -> None:  # TODO fix this
            self.tree[4] = 10
            self.assertEqual(self.tree[4], 10)

        def test_getitem(self) -> None:  # TODO fix this
            self.assertEqual(self.tree[4], 4)

    unittest.main()
