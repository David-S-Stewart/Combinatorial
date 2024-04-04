"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection, Generator
from math import ceil
from random import Random
from typing import Any, Optional, TypeVar, Union
from utility import bit_count, check


class BitArray(Collection):

    """Array that provides a mutable array of boolean values.

    The BitArray supports the same interface as list with the exception
    of remove and sort, which do not make sense in an array of bits.

    :var TYPE: Valid types for creation and extension.
    :var MARKER: Binary indicator for string representations.

    """

    TYPE = TypeVar('BITS', Collection, bytes, bytearray, str, int)
    MARKER: str = '0b'

    def __init__(self, data: TYPE = 0):
        """Construct a mutable BitArray object.

        :param data: Initialisation data.
        """
        self._data = bytearray()
        self._length = 0
        self.extend(data)

    def append(self, value: bool):
        """Append the value to the end of the BitArray."""
        assert isinstance(value, bool), check()
        # ----------
        if not self._length % 8:
            # Add a byte if there are no spare slots.
            self._data.append(0)
        if value:
            # If value is True, calculate a new byte value. If the value
            # is False, this is not needed as the pad will be correct.
            position, offset = divmod(self._length, 8)
            self._data[position] |= 2 ** offset
        self._length += 1

    def clear(self):
        """Remove all values from the BitArray."""
        self._length = 0
        self._data.clear()

    def copy(self) -> 'BitArray':
        """Return a shallow copy of the BitArray."""
        bit_array = BitArray(self._data)
        bit_array.length = self._length
        return bit_array

    def count(self, value: bool) -> int:
        """Number of values in the BitArray of the given value.

        :param value: Value to count.
        """
        assert isinstance(value, bool), check()
        # ----------
        # Relies on padded values being False.
        count = sum(bit_count(d) for d in self._data)
        return count if value else self._length - count

    def extend(self, data: TYPE):
        """Extend list by appending elements from the iterable.

        :param data: Extension data.

        Extend the BitArray from:
        - an iterable yielding bools
        - a bytes or bytearray containing bit data
        - a string formatted as 0's and 1's
        - an integer
        """
        # Extend the data set with the data provided.
        if isinstance(data, (bytes, bytearray)):
            length = self._length
            pad = self._length % 8
            self._length += len(data) * 8
            if pad:
                new_length = ceil(self._length / 8) - len(self._data)
                self._data += bytearray(new_length)
                for character in data:
                    for index in range(8):
                        value = bool(character & (2 ** index))
                        if value:
                            position, offset = divmod(length, 8)
                            self._data[position] |= 2 ** offset
                        length += 1
            else:
                self._data += bytearray(data)
        elif isinstance(data, str):
            if data.startswith(self.MARKER):
                data = data[len(self.MARKER):]
            for character in data:
                if character == '0':
                    self.append(False)
                elif character == '1':
                    self.append(True)
                else:
                    raise ValueError(f'Invalid data [{data}].')
        elif isinstance(data, Collection):
            for value in data:
                if value:
                    self.append(True)
                else:
                    self.append(False)
        elif isinstance(data, int):
            if data > 0:
                self._length += data
                new_length = ceil(self._length / 8) - len(self._data)
                self._data += bytearray(new_length)
            elif data < 0:
                # This could be implemented to extend all True values.
                raise ValueError(f'Invalid data [{data}].')
        else:
            raise ValueError(f'Invalid data [{data}].')

    def index(self, value: bool, start: Optional[int] = None,
              stop: Optional[int] = None) -> int:
        """Return first index of value.

        :param value: Value to find.
        :param start: Start of search in slice notation.
        :param stop: End of search in slice notation.

        Raises ValueError if the value is not present.
        """
        assert isinstance(value, bool), check()
        assert isinstance(start, (int, type(None))), check()
        assert isinstance(stop, (int, type(None))), check()
        # ----------
        start = self._get_index(start, None) if start else 0
        stop = self._get_index(stop, None) if stop else self._length
        for index in range(start, stop):
            if self._get_value(index) == value:
                return index
        raise ValueError(f'{value} is not in list.')

    def index_of(self, value: bool, count: int) -> int:
        """Return nth index of value.

        :param value: Value to find.
        :param count: Count of position to find.
        """
        assert isinstance(value, bool), check()
        assert isinstance(count, int), check()
        # ----------
        for index, value_ in enumerate(self):
            if value == value_:
                if count == 0:
                    return index
                else:
                    count -= 1
        raise ValueError(f'Insufficient {value} values in list.')

    def random_index(self, value: bool, random: Random) -> int:
        """Return the index of any random value within the BitArray.

        :param value: Value to find.
        :param random: Random generator.
        """
        assert isinstance(value, bool), check()
        assert isinstance(random, Random), check()
        # ----------
        count = self.count(value)
        if count == 0:
            raise ValueError(f'{value} is not in list.')
        elif count == 1:
            return self.index(value)
        else:
            return self.index_of(value, random.randint(0, count - 1))

    def insert(self, index: int, value: bool):
        """Insert object before index.

        :param index: Index of value to insert.
        :param value: Value to insert.
        """
        assert isinstance(index, (int, type(None))), check()
        assert isinstance(value, bool), check()
        # ----------
        bit_array = self[:index]
        bit_array.append(value)
        bit_array += self[index:]
        self._data = bit_array.data
        self._length = bit_array.length

    def pop(self, index: int = -1) -> bool:
        """"Remove and return item at index (default last).

        :param index: Index of value to pop.

        Raises IndexError if BitArray is empty or index is out of range.
        """
        assert isinstance(index, int), check()
        # ----------
        index = self._get_index(index, 'pop')
        value = self[index]
        bit_array = self[:index] + self[index + 1:]
        self._data = bit_array.data
        self._length = bit_array.length
        return value

    def reverse(self):
        """Reverse the BitArray in place."""
        for index in range(self._length // 2):
            swap = self._length - index - 1
            left = self._get_value(index)
            right = self._get_value(swap)
            if left != right:
                self._set_value(index, right)
                self._set_value(swap, left)

    def invert(self):
        """Invert the BitArray in place."""
        for index in range(self._length):
            self[index] = not self[index]

    @property
    def length(self) -> int:
        """The length of the BitArray."""
        return self._length

    @length.setter
    def length(self, value: int):
        # Usual use case is for copy operations.
        assert isinstance(value, int), check()
        assert ceil(value / 8) == len(self._data), check()
        # ----------
        self._length = value

    @property
    def data(self) -> bytearray:
        """Data as a bytearray."""
        return self._data

    @property
    def values(self) -> tuple[bool]:
        """The array as a collection of boolean values."""
        return tuple(self[v] for v in range(self._length))

    def __str__(self) -> str:
        # Example: '0b000011010000'
        return self.MARKER + ''.join([str(int(v)) for v in self.values])

    def __eq__(self, other: Any) -> bool:
        # Check equality against another BitArray.
        if type(self) is type(other):
            if self._length == other.length:
                if self._data == other.data:
                    return True
        return False

    def __len__(self) -> int:
        # Return length of the BitArray.
        return self._length

    def __sizeof__(self) -> int:
        # Return memory consumption of the object.
        return (super().__sizeof__()
                + self._data.__sizeof__()
                + self.length.__sizeof__())

    def __contains__(self, value: Any) -> bool:
        # True if collection contains value, False otherwise. This can be
        # determined without examining each bit.
        if value is True:
            # Any non-zero value is indicative of at least one Truth value.
            return next((True for b in self._data if b), False)
        elif value is False:
            pad = self._length % 8
            if pad:
                # If there is padding, the final byte needs to be
                # evaluated separately.
                result = next((True for b in self._data[:-1]
                               if b != 255), False)
                if result:
                    return True
                else:
                    # If the value of all the in use bits is maximum then
                    # there are no False values.
                    return self._data[-1] != 2 ** pad - 1
            else:
                # Any non-full value is indicative of at least one False value.
                return next((True for b in self._data if b != 255), False)
        # Anything else cannot be in the collection.
        return False

    def __add__(self, value: TYPE) -> 'BitArray':
        # Support the concatenation operator.
        bit_array = self.copy()
        bit_array.extend(value)
        return bit_array

    def __getitem__(self, key: Union[int, slice]) -> Union[bool, 'BitArray']:
        # Slice getter.
        if isinstance(key, int):
            return self._get_value(key)
        else:
            bit_array = BitArray()
            if key.start is None:
                start = 0
            else:
                start = self._get_index(key.start, None)
            if key.stop is None:
                stop = self._length
            else:
                stop = self._get_index(key.stop, None)
            step = key.step if key.step else 1
            for index in range(start, stop, step):
                value = self[index]
                bit_array.append(value)
            return bit_array

    def __setitem__(self, key: Union[int, slice], value: bool):
        # Slice setter.
        if isinstance(key, int):
            self._set_value(key, value)
        else:
            if key.start is None:
                start = 0
            else:
                start = self._get_index(key.start, None)
            if key.stop is None:
                stop = self._length
            else:
                stop = self._get_index(key.stop, None)
            step = key.step if key.step else 1
            for index in range(start, stop, step):
                self._set_value(index, value)

    def __iter__(self) -> Generator[bool, None, None]:
        # Return an iterator through the BitArray.
        for index in range(self._length):
            yield self._get_value(index)

    def _get_index(self, index: int, name: Optional[str]):
        # Resolve index and check bounds.
        if index < 0:
            index = self._length + index
        if index < 0:
            if name is None:
                return 0
        elif index >= self._length:
            if name is None:
                return self._length
        else:
            return index
        raise IndexError(f'{name} index out of range.')

    def _get_value(self, index: int) -> bool:
        # Get the value at the index.
        position, offset = divmod(self._get_index(index, 'list'), 8)
        return bool(self._data[position] & (2 ** offset))

    def _set_value(self, index: int, value: bool):
        # Set the value at the index.
        position, offset = divmod(self._get_index(index, 'list'), 8)
        if value:
            self._data[position] |= 2 ** offset
        else:
            self._data[position] &= (255 - (2 ** offset))
