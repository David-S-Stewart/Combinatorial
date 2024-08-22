"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Representation of a sub-combination of a combination with a BitArray to track
coverage.
"""

from collections.abc import Collection
from itertools import product
from math import prod
from typing import Optional
from binary import BitArray
from utility import check
from .constraint import Constraint
from .dimension import Dimension


class SubCombination(BitArray):

    """SubCombination of combinatorial dimensions."""

    def __init__(self, dimensions: Collection[Dimension]):
        """Construct a SubCombination object.

        :param dimensions: Dimensions of the SubCombination.
        """
        assert isinstance(dimensions, Collection), check()
        # ----------
        self._dimensions = dimensions
        super().__init__(prod(len(v) for v in self.dimensions))

    def apply_constraint(self, constraint: Constraint):
        """Apply the constraint to this sub_combination.

        :param constraint: Constraint to apply.
        """
        if next((False for e in constraint.extents
                 if e.dimension not in self._dimensions), True):
            features_sets = []
            for dimension in self._dimensions:
                feature_set = next((e.features for e in constraint.extents
                                    if e.dimension is dimension),
                                   dimension.features)
                features_sets.append(feature_set)
            for features in product(*features_sets):
                for dimension, feature in zip(self._dimensions, features):
                    dimension.feature = feature
                self.cover()

    def cover(self):
        """Cover the SubCombination."""
        index = self.sub_combination_index
        if index is not None:
            self[index] = True

    @property
    def dimensions(self) -> Collection[Dimension]:
        """Dimensions of the SubCombination."""
        return self._dimensions

    @property
    def sub_combination_index(self) -> Optional[int]:
        """Index of the SubCombination."""
        result = 0
        shift = 1
        for dimension in self._dimensions:
            if dimension.feature_index is None:
                return None
            else:
                result += dimension.feature_index * shift
                shift *= len(dimension)
        return result

    @sub_combination_index.setter
    def sub_combination_index(self, value: Optional[int]):
        assert isinstance(value, (int, type(None))), check()
        # ----------
        if value is None:
            for dimension in self._dimensions:
                dimension.feature = None
        else:
            for dimension in self._dimensions:
                value, dimension.feature_index = divmod(value, len(dimension))

    @property
    def is_covered(self) -> Optional[bool]:
        """True if the SubCombination is covered, False otherwise."""
        index = self.sub_combination_index
        if index is None:
            return None
        else:
            return self[index]
