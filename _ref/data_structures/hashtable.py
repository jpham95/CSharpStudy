from typing import TypeVar, Generic
from linklist import LinkedList
from referential_array import ArrayR

T = TypeVar("T")


class HashTable(Generic[T]):
    MIN_CAPACITY = 1
    DEFAULT_TABLE_SIZE = 17
    DEFAULT_HASH_BASE = 112909

    def __init__(
        self, table_size: int = DEFAULT_TABLE_SIZE, hash_base: int = DEFAULT_HASH_BASE
    ) -> None:
        self.count = 0

        assert isprime(table_size), "table_size must be prime"

        self.table = ArrayR(max(self.MIN_CAPACITY, table_size))

        self.hash_base = hash_base

    def __len__(self):
        return self.count

    def __setitem__(self, key: str, data: T) -> None:
        """
        Set a (key, data) pair in the hash table.

        :complexity:    O(nk) where n is the len(linkedlist) at position and k is len(key)
        """
        position = self._hash(key)  # save hash to variable
        if self.table[position] == None:
            self.table[
                position
            ] = LinkedList()  # new entry creates linkedlist at position

        for i, item in enumerate(self.table[position]):  # enumerate linked list
            if (
                item[0] == key
            ):  # if UNHASHED key of data (data[0]) matches current UNHASHED key
                self.table[position][i] = data  # replace data
                return

        self.table[position].insert(0, (key, data))  # else insert at key 0 of linklist
        self.count += 1  # increment count

    def __getitem__(self, key: str) -> T:
        """
        Get the item at a certain key
        :raises KeyError: when the item doesn't exist
        :complexity: O(nk) where n is len(linkedlist) at position and k is len(key)
        """
        position = self._hash(key)

        if self.table[position] == None:
            raise KeyError(key)

        for data in self.table[position]:
            if data[0] == key:
                return data[1]

    def __delitem__(self, key: str) -> None:
        """
        Deletes item from hash table.
        :raises KeyError: when key doesn't exist

        :complexity: O(nk) where n is len(linkedlist) at position and k is len(key)
        """
        position = self._hash(key)

        if self.table[position] is None:
            raise KeyError(key)

        for item in self.table[position]:
            if item[0] == key:
                index = self.table[position].index(item)
                self.table[position].delete_at_index(index)
                self.count -= 1
                return

        raise KeyError(key)

    def _hash(self, key: str) -> int:
        """hash function for the hash table."""
        value = 0
        prime = 409
        salt = 7919

        for char in key:
            value = (self.hash_base * ord(char) + prime * value) % len(self.table)
            prime = prime * salt % (len(self.table) - 1)

        # print(f"{key} hashed to {value}")
        assert value <= len(self.table)
        return value

    def is_empty(self) -> bool:
        """Returns True if hash table is empty."""
        return self.count == 0

    def insert(self, key: str, data: T) -> None:
        """utility method to call __setitem__"""
        self[key] = data

    def __str__(self) -> str:
        """returns all key/value pairs in the hash table"""
        result = ""
        for list in self.table:
            if list is not None:
                first = True
                for item in list:
                    if not first:
                        result += " -> "
                    (key, value) = item
                    result += f"({key}, {value})"
                    first = False
                result += "\n"

        return result


def isprime(n: int, i=2) -> bool:
    """returns True if n is prime"""
    if n**0.5 < i:  # if i reaches sqrt(n) return true
        return True
    elif n % i == 0:  # if factor found return false
        return False

    return isprime(n, i + 1)  # increment i


if __name__ == "__main__":
    # dictionary = HashTable(11)
    # words = ["taro", "oyatsu", "bento", "sourwalrus", "pastel", "cookie", "yoda"]
    # for word in words:
    #     dictionary[word] = word
    # print([key[0] for key in dictionary.table if key is not None])
    from icecream import ic

    ic(isprime(16807))
