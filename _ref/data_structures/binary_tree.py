from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class BinaryTreeNode(Generic[T]):
    def __init__(self, key: T = None, item: T = None) -> None:
        self.item = item
        self.key = key
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return str(self.item)


class BinaryTree(Generic[T]):
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
                if current.key == key:
                    current.key, current.item = key, value
                elif current.key > key:
                    current.left = _setitem_aux(current.left, key, value)
                elif current.key < key:
                    current.right = _setitem_aux(current.right, key, value)
            else:  # current is None
                current = BinaryTreeNode(key, value)

            return current

        self.root = _setitem_aux(self.root, key, value)

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


if __name__ == "__main__":
    tree = BinaryTree()
    tree[1] = 1
    tree[2] = 2
    tree[3] = 3
    # tree[4] = 4
    tree[5] = 5
    tree[6] = 6
    tree[7] = 7
    tree[8] = 8
    tree[9] = 9
    tree[10] = 10

    tree.postorder(print)
