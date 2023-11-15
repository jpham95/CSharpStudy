# sorted list using arrays
## good for search O(logN)
## bad for insertion O(N)

# sorted list using linked nodes
## worse for search O(N)
## better for insertion and deletion O(1)

# binary search tree
## good for search O(logN)
## good for insertion and deletion O(logN)

from typing import TypeVar, Generic, Callable

K = TypeVar("K")
I = TypeVar("I")


class BinarySearchTreeNode(Generic[K, I]):
    def __init__(self, key: K, item: I = None) -> None:
        self.key = key
        self.item = item
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return " (" + str(self.key) + ", " + str(self.item) + ")"


class BinarySearchTree(Generic[K, I]):
    def __init__(self) -> None:
        self.root = None

    def is_empty(self) -> bool:
        return self.root is None

    def __contains__(self, key: K) -> bool:
        """
        :complexity: O(depth)*(comp== + comp<) where depth is the depth of the tree
        """

        def _contains_aux(current: BinarySearchTreeNode[K, I]) -> bool:
            if current is None:
                return False
            elif current.key > key:
                return _contains_aux(current.left, key)
            elif current.key < key:
                return _contains_aux(current.right, key)
            else:  # current.key == key
                return True

        return _contains_aux(self.root, key)

    def __getitem__(self, key: K) -> I:
        """
        :complexity: O(depth)*(comp== + comp<) where depth is the depth of the tree
        """

        def _getitem_aux(current: BinarySearchTreeNode[K, I]) -> I:
            if current is None:  # base case: empty
                raise KeyError(key)
            elif current.key > key:
                return _getitem_aux(current.left, key)
            elif current.key < key:
                return _getitem_aux(current.right, key)
            else:  # current.key == key
                return current.item

        return _getitem_aux(self.root, key)

    def __setitem__(self, key: K, item: I) -> None:
        """
        :complexity: O(depth)*(comp== + comp<) where depth is the depth of the tree
        """

        def _insert_aux(
            current: BinarySearchTreeNode[K, I]
        ) -> BinarySearchTreeNode[K, I]:
            if current is None:
                current = BinarySearchTreeNode(key, item)
            elif current.key > key:
                current.left = _insert_aux(current.left)
            elif current.key < key:
                current.right = _insert_aux(current.right)
            else:  # current.key == key
                raise ValueError("Inserting duplicate item")
            return current

        self.root = _insert_aux(self.root)

    def __len__(self) -> int:
        def _len_aux(current: BinarySearchTreeNode[T]) -> int:
            if current is None:
                return 0
            else:
                return 1 + _len_aux(current.left) + _len_aux(current.right)

        return _len_aux(self.root)

    def preorder(self, f: Callable) -> None:
        def _preorder_aux(current: BinarySearchTreeNode[T], f: Callable) -> None:
            if current is not None:
                f(current)
                _preorder_aux(current.left, f)
                _preorder_aux(current.right, f)

        _preorder_aux(self.root, f)

    def inorder(self, f: Callable) -> None:
        def _inorder_aux(current: BinarySearchTreeNode[T], f: Callable) -> None:
            if current is not None:
                _inorder_aux(current.left, f)
                f(current)
                _inorder_aux(current.right, f)

        _inorder_aux(self.root, f)

    def postorder(self, f: Callable) -> None:
        def _postorder_aux(current: BinarySearchTreeNode[T], f: Callable) -> None:
            if current is not None:
                _postorder_aux(current.left, f)
                _postorder_aux(current.right, f)
                f(current)

        _postorder_aux(self.root, f)

    def delete(self, key: K) -> None:
        def _delete_aux(
            current: BinarySearchTreeNode[K, I]
        ) -> BinarySearchTreeNode[K, I]:
            if current is None:
                raise KeyError(key)

            elif current.key > key:
                current.left = _delete_aux(current.left)
            elif current.key < key:
                current.right = _delete_aux(current.right)

            else:
                if current.left is None and current.right is None:
                    current = None

                elif current.left is None:
                    current = current.right

                elif current.right is None:
                    current = current.left

                else:
                    # find the minimum item to the right of successor
                    minimum = current.right

                    while minimum.left is not None:
                        minimum = minimum.left

                    # replace current with minimum
                    current.key = minimum.key
                    current.item = minimum.item

                    current.right = _delete_aux(
                        current.right, minimum.key
                    )  # delete minimum
            return current

        self.root = _delete_aux(self.root, key)
