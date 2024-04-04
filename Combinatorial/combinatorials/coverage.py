"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection
from math import prod
from random import Random
from typing import Any, Optional
from binary import BitArray
from utility import check
from .dimension import Dimension
from .option import Option


class Coverage(BitArray):

    """Coverage of a subset of combinatorial dimensions.

    Within the scope of a Coverage, there are three equivalent representations
    of a combination:
    - combination: The sub-combination of features.
    - indexes: The indexes of the values in their dimensions.
    - index: The bitarray index.
    """

    def __init__(self, dimensions: Collection[Dimension],
                 option: Option = Option.NONE):
        """Construct a Coverage object.

        :param dimensions: Dimensions of the Coverage.
        """
        assert isinstance(dimensions, Collection), check()
        assert isinstance(option, Option), check()
        # ----------
        self._dimensions = dimensions
        self._option = option
        super().__init__(prod(len(v) for v in self.dimensions))

    # index <> indexes <> combination conversions.
    # Note that the parameter lists are not checked in these cases as the
    # methods are called a very large number of times.

    def index_to_indexes(self, index: int) -> list[int]:
        """Get the indexes equivalent of an index.

        :param index: The bitarray index.
        """
        indexes = []
        for dimension in self._dimensions:
            index, value = divmod(index, len(dimension))
            indexes.append(value)
        return indexes

    def index_to_combination(self, index: int) -> list[Any]:
        """Get the combination equivalent of an index.

        :param index: The bitarray index.
        """
        return self.indexes_to_combination(self.index_to_indexes(index))

    def indexes_to_index(self, indexes: list[int]) -> int:
        """Get the index equivalent of an indexes list.

        :param indexes: The indexes of the values in their dimensions.
        """
        result = 0
        shift = 1
        for dimension, index in zip(self._dimensions, indexes):
            result += index * shift
            shift *= len(dimension)
        return result

    def indexes_to_combination(self, indexes: list[int]) -> list[int]:
        """Get the combination equivalent of an indexes list.

        :param indexes: The indexes of the values in their dimensions.
        """
        return [d.values[n] for d, n in zip(self._dimensions, indexes)]

    def combination_to_index(self, combination: list[Any]) -> int:
        """Get the index equivalent of a combination.

        :param combinations: The sub-combination of features.
        """
        return self.indexes_to_index(self.combination_to_indexes(combination))

    def combination_to_indexes(self, combination: list[Any]) -> list[int]:
        """Get the indexes equivalent of a combination.

        :param combinations: The sub-combination of features.
        """
        return [d.values.index(c) for d, c
                in zip(self._dimensions, combination)]

    # Combinatorial operation.

    def clear(self):
        """Clear the coverage data."""
        # This is different to clearing the BitArray base as that removes
        # the data.
        self._data = bytearray(len(self._data))

    def select(self, random: Optional[Random] = None):
        """Select an available coverage combination.

        :param random: Random generator.
        """
        if self._option & Option.RETIRE_RANDOM:
            # If the random option is set, select a random index.
            index = self.random_index(False, random)
        else:
            # Otherwise select the first available index.
            index = self.index(False)
        indexes = self.index_to_indexes(index)
        for index, dimension in zip(indexes, self._dimensions):
            dimension.feature = dimension.features[index]

    def is_covered(self) -> bool:
        """True if the coverage combination is covered, False otherwise."""
        indexes = [d.feature.index for d in self._dimensions]
        return self[self.indexes_to_index(indexes)]

    def cover(self):
        """Cover the current coverage combination."""
        indexes = [d.feature.index for d in self._dimensions]
        self[self.indexes_to_index(indexes)] = True

    def uncover(self):
        """Uncover the current coverage combination."""
        indexes = [d.feature.index for d in self._dimensions]
        self[self.indexes_to_index(indexes)] = False

    @property
    def dimensions(self) -> Collection[Dimension]:
        """Dimensions of the Coverage."""
        return self._dimensions

    @property
    def option(self) -> Option:
        """Generation option set for the Coverage."""
        return self._option

    def __str__(self) -> str:
        # Example: 'Coverage'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Coverage.
        if type(self) is type(other):
            if self._dimensions == other.dimensions:
                if self._option == other.option:
                    return True
        return False
