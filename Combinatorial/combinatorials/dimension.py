"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection
from random import Random
from typing import Any, Optional
from utility import check
from .feature import Feature
from .option import Option


class Dimension:

    """Dimension definition for combinatorial generation."""

    def __init__(self, identity: str, values: Collection[Any]):
        """Construct a Dimension object.

        :param identity: The identity of the Dimension.
        :param values: The values in the Dimension.
        """
        assert isinstance(identity, str), check()
        assert isinstance(values, Collection), check()
        # ----------
        self._index = -1
        self._identity = identity
        self._values = values
        self._option = Option.NONE
        self._features = [Feature(n, v) for n, v in enumerate(self._values)]
        self._feature = self._features[0] if len(self._features) == 1 else None

    def select(self, random: Random) -> list[Feature]:
        """
        Select the features and return ordered based on the set option.

        :param random: Random generator.
        """
        assert isinstance(random, Random), check()
        # ----------
        features = list(self._features)
        # Note that the random shuffle can still change the count sorts.
        if self._option & Option.FEATURE_RANDOM:
            random.shuffle(features)
        if self._option & Option.FEATURE_COUNT_MINIMUM:
            features.sort(key=lambda f: f.count)
        elif self._option & Option.FEATURE_COUNT_MAXIMUM:
            features.sort(key=lambda f: f.count, reverse=True)
        return features

    @property
    def index(self) -> int:
        """Indexed position of the Dimension."""
        return self._index

    @index.setter
    def index(self, value: int):
        assert isinstance(value, int), check()
        # ----------
        self._index = value

    @property
    def identity(self) -> str:
        """The identity of the Dimension."""
        return self._identity

    @property
    def values(self) -> Collection[Any]:
        """The values in the Dimension."""
        return self._values

    @property
    def option(self) -> Option:
        """Generation option set for the Dimension."""
        return self._option

    @option.setter
    def option(self, value: Option):
        assert isinstance(value, Option), check()
        # ----------
        self._option = value

    @property
    def features(self) -> list[Feature]:
        """Indexed features of the dimension."""
        return self._features

    @property
    def feature(self) -> Optional[Feature]:
        """Current feature value of the dimension."""
        return self._feature

    @feature.setter
    def feature(self, value: Optional[Feature]):
        assert isinstance(value, (Feature, type(None))), check()
        # ----------
        self._feature = value

    def __str__(self) -> str:
        # Example: 'Dimension'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Dimension.
        if type(self) is type(other):
            if self._index == other.index:
                if self._identity == other.identity:
                    if self._values == other.values:
                        return True
        return False

    def __len__(self) -> int:
        # Return length of the Dimension.
        return len(self._values)
