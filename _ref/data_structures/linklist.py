from abstract_list import List
from typing import Generic, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, item: T = None) -> None:
        self.item = item
        self.next = None


class LinkedListIterator(Generic[T]):
    def __init__(self, node: Node[T]) -> None:
        """initialises current as input node"""
        self.current = node

    def __iter__(self) -> "LinkedListIterator":
        """returns itself for iteration"""
        return self

    def __next__(self) -> T:  # TODO not sure about this implementation
        if self.current is not None:
            item = self.current.item
            self.current = self.current.next
            return item
        else:
            raise StopIteration


class LinkedList(List[T]):
    def __init__(self, dummy_capacity=1) -> None:
        """Linked list data structure."""
        List.__init__(self)
        self.head = None

    def clear(self) -> None:
        """Clears the list."""
        self.head = None
        List.clear(self)

    def __setitem__(self, index: int, item: T) -> None:
        """Dunder method, set node at given index."""
        node_at_index = self._get_node_at_index(index)
        node_at_index.item = item

    def __getitem__(self, index: int) -> T:
        """Dunder method, returns item at index."""
        node_at_index = self._get_node_at_index(index)
        return node_at_index.item

    def __iter__(self) -> LinkedListIterator[T]:
        return LinkedListIterator(self.head)

    def index(self, item: T) -> int:
        """Returns index of item."""
        current = self.head
        index = 0
        while current is not None:
            if current.item == item:
                return index
            else:
                current = current.next
                index += 1

        raise ValueError("Item not in list.")

    def _get_node_at_index(self, index: int) -> Node[T]:
        """Internal method. Return node at given index."""
        if 0 <= index and index < len(self):
            current = self.head
            for _ in range(index):
                current = current.next
            return current

        else:
            raise ValueError("Index out of bounds.")

    def delete_at_index(self, index: int) -> T:
        """Returns and removes item at index."""
        if not self.is_empty():
            if index > 0:
                prev_node = self._get_node_at_index(index - 1)
                item = prev_node.next.item
                prev_node.next = prev_node.next.next
            elif index == 0:
                item = self.head.item
                self.head = self.head.next
            else:
                raise ValueError("Index out of bounds.")
            self.length -= 1
            return item
        else:
            raise ValueError("List is empty.")

    def insert(self, index: int, item: T) -> None:
        """Inserts item at index."""
        node = Node(item)

        if index == 0:
            node.next = self.head
            self.head = node
        else:
            prev_node = self._get_node_at_index(index - 1)
            node.next = prev_node.next
            prev_node.next = node

        self.length += 1

    def append(self, item: T, *args) -> None:
        """Append a new item or items to the end of the list."""
        self.insert(len(self), item)
        if args is not None:
            for item in args:
                self.append(item)


if __name__ == "__main__":
    listy = LinkedList()
    listy.append(5, 6, 7, 1)

    print(listy)
