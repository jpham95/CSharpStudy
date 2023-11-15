from __future__ import annotations
from typing import Generic, TypeVar, Iterator

from data_structures.referential_array import ArrayR
from algorithms.mergesort import mergesort, merge

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTableIterator(Generic[K, V]):
    def __init__(self, table: InfiniteHashTable[K, V]) -> None:
        """
        Iterator for Infinite Hash Table, iterates through (key, value) pairs
        stored in the table.

        :table: Infinite Hash Table to iterate through.
        """
        self.table = table
        self.keys = table.sort_keys()
        self.index = 0

    def __iter__(self) -> "InfiniteHashTableIterator":
        return self

    def __next__(self) -> (K, V):
        if self.index < len(self.keys):
            key = self.keys[self.index]
            value = self.table[key]
            self.index += 1
            return (key, value)
        else:
            raise StopIteration


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type`.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """Initialise the Hash Table."""
        self.array = ArrayR(self.TABLE_SIZE)
        self.level = 0
        self.count = 0
        self.sort_order = [self.TABLE_SIZE - 1] + [
            index % (self.TABLE_SIZE - 1) for index in list(range(97, 122))
        ]  # store order of hashed alphabet

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        :complexity: O(n*comp==) worst case where n is the length of the key.
        :best case complexity: O(1) when key is at top level of table.
        """
        # get position of key for this level
        position = self.hash(key)

        if self.array[position] is None:
            raise KeyError("key does not exist")

        # item not on this level, go to next level of tables
        elif type(self.array[position][1]) == InfiniteHashTable:
            next_table = self.array[position][1]
            next_table.level = self.level + 1
            return next_table[key]

        # item is on this level
        else:  # if self.array[position][0] == key:
            return self.array[position][1]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: O(n*comp==) worst case where n is the length of the key.
        :best case complexity: O(1) when key is at top level of table.
        """
        # get position of key for this level
        position = self.hash(key)

        # if position in current array is empty
        if self.array[position] is None:
            # add (key, value) pair
            self.array[position] = (key, value)
            self.count += 1
            # reset level
            self.level = 0
            return
        else:  # position in current array is not empty
            # if key is already in position
            if self.array[position][0] == key:
                # overwrite value
                self.array[position] = (key, value)
                return
            # key not on this level
            elif self.array[position][0] == key[self.level]:
                next_table = self.array[position][1]
                # increment level of next table
                next_table.level = self.level + 1
                # call setitem on next table
                next_table[key] = value
                self.count += 1
                return
            else:  # collision detected
                if not type(self.array[position][1]) == InfiniteHashTable:
                    # increment count for top level table
                    self.count += 1
                    # assign current (key, value) pair to holding variables
                    existing_key, existing_value = self.array[position]
                    # overwrite position with new table
                    self.array[position] = (
                        key[self.level],
                        InfiniteHashTable(),
                    )
                    next_table = self.array[position][1]
                    # increment level of new table
                    next_table.level = self.level + 1
                    # add (key, value) pair to new table
                    next_table[key] = value
                    # increment level of new table again because adding a new (key, value) pair resets level to 0
                    next_table.level = self.level + 1
                    # add original (existing_key, existing_value) pair to new table
                    next_table[existing_key] = existing_value
                    return

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        :complexity: O(n*comp==) worst case where n is the length of the key.
        :best case complexity: O(1) when key is at top level of table.
        """
        # get position of key for this level
        position = self.hash(key)

        if self.array[position] is None:
            raise KeyError("key does not exist")
        # key not on this level
        elif type(self.array[position][1]) == InfiniteHashTable:
            next_table = self.array[position][1]
            # increment level of next table
            next_table.level = self.level + 1
            # call delitem on next table
            del next_table[key]
            # if next table has only one item left, collapse it
            if len(next_table) == 1:
                key = next_table.sort_keys()[0]
                value = next_table[key]
                self.level = next_table.level - 1
                position = self.hash(key)
                self.array[position] = (key, value)
            self.count -= 1
            return
        # item is on this level
        elif self.array[position][0] == key:
            # remove the item
            self.array[position] = None
            self.count -= 1
            return

    def __len__(self) -> int:
        """Returns the number of elements in the hash table."""
        return self.count

    def get_location(self, key: K) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        :complexity: O(n*comp==) worst case where n is the length of the key.
        :best case complexity: O(1) when key is at top level of table.
        """
        location_list = []
        # initialise current table to top level table and position to hash of key
        current_table = self.array
        position = self.hash(key)

        while current_table[position] is not None:
            # if key is on this level
            if current_table[position][0] == key:
                # add position to end of location list
                location_list.append(position)
                # reset level
                self.level = 0
                return location_list
            # key not on this level
            elif current_table[position][0] == key[self.level]:
                # add position to location list
                location_list.append(position)
                # increment level
                self.level += 1
                # set current table to next table
                current_table = current_table[position][1].array
                # hash key for next level
                position = self.hash(key)
            else:  # key not found
                raise KeyError("key does not exist")
        raise KeyError("key does not exist")

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See __getitem__.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted
        order by comparing the ord() of each character in each key

        :current: list of keys

        :complexity: O(N*A*L) where N is the number of keys in the table, A is
                the number of characters in the alphabet, and L is the length of the
                longest key.
        """
        # first time calling sort_keys
        if current is None:
            current = []

        # iterate through hashed alphabet (a-z)
        for index in self.sort_order:
            # if there is an item at current letter's index
            if self.array[index] is not None:
                # if item is a table, call sort_keys on table
                if type(self.array[index][1]) == InfiniteHashTable:
                    current = self.array[index][1].sort_keys(current)
                else:  # full key is in this position
                    current.append(self.array[index][0])

        return current

    def __iter__(self) -> Iterator[(K, V)]:
        """Returns an iterator of (key, value) pairs for the hash table."""
        return InfiniteHashTableIterator(self)

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = "["

        for i, item in enumerate(self.elements):
            if i < len(self.elements) - 1:
                result += "{" + f"{item[0]}: {item[1]}" + "}, "
            else:
                result += "{" + f"{item[0]}: {item[1]}" + "}"

        result += "]"
        return result

    @property
    def elements(self) -> list[(K, V)]:
        """Returns a list of (key, value) pairs for the hash table."""
        return [(key, value) for key, value in self]

    @property
    def keys(self) -> list[K]:
        """Returns a list of keys the hash table."""
        return [key for key, _ in self]

    @property
    def values(self) -> list[V]:
        """Returns a list of values the hash table."""
        return [value for _, value in self]


if __name__ == "__main__":
    table = InfiniteHashTable()
    table["aa"] = 1
    table["ab"] = 2
    table["ac"] = 3
    table["ad"] = 4
    table["ae"] = 5
    table["af"] = 6
    table["ag"] = 7
    table["ah"] = 8
    table["ai"] = 9
    table["aj"] = 10

    print(table)
