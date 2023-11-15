from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar("K1")
K2 = TypeVar("K2")
V = TypeVar("V")


class DoubleKeyTableIterator(Generic[K1, K2, V]):
    def __init__(self, hash_table, returnKey: bool = False) -> None:
        """
        iterator for DoubleKeyTable, iterates over all keys or values in the table.

        :hash_table: the hash table to iterate over.
        :returnKey: True to iterate over keys, False to iterate over values.
        """
        self.index = 0
        self.hash_table = hash_table
        self.returnKey = returnKey

    def __iter__(self) -> "DoubleKeyTableIterator":
        return self

    def __next__(self) -> K1 | K2 | V:
        # get current list of either keys or values
        self.iterlist = (
            self.hash_table.keys() if self.returnKey else self.hash_table.values()
        )
        # if we haven't reached the end of the list, return the next item
        if self.index < len(self.iterlist):
            result = self.iterlist[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [
        5,
        13,
        29,
        53,
        97,
        193,
        389,
        769,
        1543,
        3079,
        6151,
        12289,
        24593,
        49157,
        98317,
        196613,
        393241,
        786433,
        1572869,
    ]

    HASH_BASE = 31

    def __init__(
        self, sizes: list | None = None, internal_sizes: list | None = None
    ) -> None:
        """
        initialise the Hash Table.

        :sizes: A list of sizes to use for the top-level hash table.
        :internal_sizes: A list of sizes to use for the bottom-level hash table.
        """
        self.count = 0
        self.size_index = 0

        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_table_sizes = internal_sizes
        else:
            self.internal_table_sizes = DoubleKeyTable.TABLE_SIZES

        self.array: ArrayR[tuple[K1, LinearProbeTable]] = ArrayR(
            self.TABLE_SIZES[self.size_index]
        )

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(
        self, key1: K1, key2: K2, is_insert: bool
    ) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear
        probing.

        :key1: The first key to search for.
        :key2: The second key to search for.
        :is_insert: True if we are inserting, False if we are searching.
        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        :complexity: O(hash(key1) + hash(key2) + N*comp(K)) when we've searched
                    the entire table, where N is the tablesize and K is the
                    length of the key.

        :best case complexity: O(hash(key1) + hash(key2)) when the key is at the
                            first position.
        """
        # get position of key1
        position1 = self.hash1(key1)

        for _ in range(self.table_size):
            # if position1 is empty
            if self.array[position1] is None:
                # if we are inserting, create a new sub-table
                if is_insert:
                    self.array[position1] = (
                        key1,
                        LinearProbeTable(self.internal_table_sizes),
                    )
                    sub_table = self.array[position1][1]
                    # set hash function for sub-table to hash2
                    sub_table.hash = lambda k: self.hash2(k, sub_table)
                    self.count += 1
                    if key2 is None:
                        # if rehashing top-level table, return position1
                        return position1
                    else:
                        position2 = self.hash2(key2, sub_table)
                        return position1, position2
                else:
                    raise KeyError(key1)

            # if position1 is not empty and key matches key1
            elif self.array[position1][0] == key1:
                # if finding sub-table only, return position1
                if key2 is None:
                    return position1

                else:  # if finding key2 in sub-table
                    internal_table = self.array[position1][1]
                    position2 = self.hash2(key2, internal_table)
                    # linear probe sub-table for key2
                    for _ in range(internal_table.table_size - 1):
                        # if position2 is empty
                        if internal_table.array[position2] is None:
                            if is_insert:
                                # if inserting, return position1, position2
                                return position1, position2
                            else:
                                raise KeyError(key2)

                        # if position2 is not empty and key matches key2
                        elif internal_table.array[position2][0] == key2:
                            return position1, position2

                        else:  # if position2 is not empty and key doesn't match key2
                            # step to next position of sub-table
                            position2 = (position2 + 1) % internal_table.table_size
                    raise FullError("Internal Table is full")

            else:
                # step to next position of top-level table
                position1 = (position1 + 1) % self.table_size

        raise FullError("Double Key Table is full")

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None: Returns an iterator of all top-level keys in hash table
        key = k: Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            return DoubleKeyTableIterator(self, returnKey=True)
        else:
            # use linear probe to find sub-table
            sub_table = self.array[self._linear_probe(key, None, False)][1]
            return DoubleKeyTableIterator(sub_table, returnKey=True)

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = k: returns all bottom-level keys for top-level key k.

        :complexity: O(N*comp==) where N is the number of keys in the table.
        """
        if key is None:
            # get all keys of top-level table
            return [entry[0] for entry in self.array if entry is not None]
        else:
            # get all keys of sub-table matching given key
            return [entry for entry in self.iter_keys(key)]

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None: Returns an iterator of all values in hash table
        key = k: Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None:
            return DoubleKeyTableIterator(self)
        else:
            # use linear probe to find sub-table
            sub_table = self.array[self._linear_probe(key, None, False)][1]
            return DoubleKeyTableIterator(sub_table)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        :complexity: O(N*comp==) where N is the number of values in the table.
        """
        if key is None:
            # get all values in all sub-tables
            return [
                value
                for entry in self.array
                if entry is not None
                for value in entry[1].values()
            ]
        else:
            # get all values in sub-table matching given key
            return [entry for entry in self.iter_values(key)]

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        :complexity: see linear probe.
        """
        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, False)
        return self.array[position1][1][position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: O(hash(key1) + hash(key2) + N*comp(K)) where N is len(self.array)
        :best case complexity: O(hash(key1) + hash(key2)) when the key is at the first position.

        :complexity if resizing top table: O(N*hash(K) + N^2*comp(K)) where N is len(self)
        :complexity if resizing sub table: O(N*hash(K) + N^2*comp(K)) where N is len(sub_table)
        """
        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]

        # deal with sub_table count manually due to the way we insert
        if sub_table.array[position2] is None:
            sub_table.count += 1

        # insert into sub_table
        sub_table.array[position2] = (key2, data)

        # rehash if sub_table is too full
        if len(sub_table) > sub_table.table_size / 2:
            sub_table._rehash()  # O(N*hash(K) + N^2*comp(K)) if lots of probing. Where N is len(sub_table)

        # rehash if top table is too full
        if len(self) > self.table_size / 2:
            self._rehash()  # O(N*hash(K) + N^2*comp(K)) if lots of probing. Where N is len(self)

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        :complexity: O(hash(key1) + hash(key2) + N*comp(K)) where N is len(self.array)
        :best case complexity: O(hash(key1) + hash(key2)) when the key is at the first position.
        """

        key1, key2 = key
        # use linear probe to find sub-table
        position1 = self._linear_probe(key1, None, False)
        sub_table = self.array[position1][1]

        # use the sub-table's delete method
        del sub_table[key2]
        self.count -= 1

        # delete top-level key if sub-table is empty
        if not len(sub_table.values()):
            self.array[position1] = None

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing. where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            # cannot be resized further
            return
        self.array: ArrayR[tuple[K1, ArrayR]] = ArrayR(
            self.TABLE_SIZES[self.size_index]
        )
        self.count = 0

        # iterate through old_array and reinsert all (key1, sub-table) pairs
        for item in old_array:
            if item is not None:
                key1, sub_table = item
                position1 = self._linear_probe(key1, None, True)
                self.array[position1] = (key1, sub_table)

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for key1 in self.keys():
            result += f"{key1}: "
            for key2, value, i in zip(
                self.keys(key1),
                self.values(key1),
                range(len(self.keys(key1))),
            ):
                result += f"({key2}, {value})"
                if i < len(self.keys(key1)) - 1:
                    result += ", "
                else:
                    result += "\n"
        return result
