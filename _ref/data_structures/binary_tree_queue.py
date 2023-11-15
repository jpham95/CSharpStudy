from typing import TypeVar, Generic, Callable
from binary_tree import BinaryTreeNode

T = TypeVar("T")


# class BinaryTreeNode(Generic[T]):
#     def __init__(self, item: T = None) -> None:
#         self.item = item
#         self.left = None
#         self.right = None

#     def __str__(self) -> str:
#         return str(self.item)


class BinaryTreeQueue(Generic[T]):
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
        def _preorder_aux(current: BinaryTreeNode[T], f: Callable) -> None:
            if current is not None:
                f(current)
                _preorder_aux(current.left, f)
                _preorder_aux(current.right, f)

        _preorder_aux(self.root, f)

    def inorder(self, f: Callable) -> None:
        def _inorder_aux(current: BinaryTreeNode[T], f: Callable) -> None:
            if current is not None:
                _inorder_aux(current.left, f)
                f(current)
                _inorder_aux(current.right, f)

        _inorder_aux(self.root, f)

    def postorder(self, f: Callable) -> None:
        def _postorder_aux(current: BinaryTreeNode[T], f: Callable) -> None:
            if current is not None:
                _postorder_aux(current.left, f)
                _postorder_aux(current.right, f)
                f(current)

        _postorder_aux(self.root, f)

    def __setitem__(self, key: int, value: T) -> None:
        def _setitem_aux(current: BinaryTreeNode[T], key: int, value: T) -> None:
            if current is not None:
                if current.item[0] == key:
                    current.item = (key, value)
                else:
                    _setitem_aux(current.left, key, value)
                    _setitem_aux(current.right, key, value)

        _setitem_aux(self.root, key, value)

    def __getitem__(self, key: int) -> T:
        def _getitem_aux(current: BinaryTreeNode[T], key: int) -> T:
            if current is not None:
                if current.item[0] == key:
                    return current.item[1]
                else:
                    return _getitem_aux(current.left, key) or _getitem_aux(
                        current.right, key
                    )

        return _getitem_aux(self.root, key)

    # def __delitem__(self, key: int) -> None:
    #     def _delitem_aux(current: BinaryTreeNode, key: int) -> None:
    #         if current is not None:
    #             if current.right.item[0] == key:
    #                 current

    def get_max(self) -> T:
        if self.root is None:
            raise ValueError("Priority queue is empty.")
        else:

            def _get_max_aux(current: BinaryTreeNode[T]) -> T:
                if current.right is None:  # base case: reached max
                    return current.item
                else:
                    return _get_max_aux(current.right)

            return _get_max_aux(self.root)

    def get_max_del(self) -> T:
        if self.root is None:
            raise ValueError("Priority queue is empty.")
        elif self.root.right is None:
            max_item = self.root.item
            self.root = self.root.left if self.root.left is not None else None
            return max_item
        else:

            def _get_max_aux(
                current: BinaryTreeNode[T], parent: BinaryTreeNode[T]
            ) -> T:
                if current.right is None:  # base case: reached max
                    parent.right = current.left
                    return current.item
                else:
                    return _get_max_aux(current.right, current)

            return _get_max_aux(self.root.right, self.root)


if __name__ == "__main__":
    import unittest

    class TestBinaryTree(unittest.TestCase):
        def setUp(self) -> None:
            self.tree = BinaryTreeQueue()
            self.tree.root = BinaryTreeNode((1, 3))
            self.tree.root.left = BinaryTreeNode((2, 6))
            self.tree.root.right = BinaryTreeNode((3, 5))
            self.tree.root.left.left = BinaryTreeNode((4, 4))
            self.tree.root.left.right = BinaryTreeNode((5, 10))
            self.tree.root.right.left = BinaryTreeNode((6, 1))
            self.tree.root.right.right = BinaryTreeNode((7, 3))

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
