"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Feature set in the context of a combinatorial.
"""

from collections.abc import Collection
from random import Random
from typing import Any, Optional, Union
from utility import check
from utility.defaults import NONE_TYPE
from .feature import Feature
from .featureset import FeatureSet


class Dimension(FeatureSet):

    """Dimension definition for combinatorial generation."""

    def __init__(self, identity: str, values: Collection[Any]):
        """Construct a Dimension object.

        :param identity: The identity of the Dimension.
        :param values: The values in the Dimension.
        """
        self._feature = None
        super().__init__(identity, values)
        self.initialise()

    def initialise(self, random: Optional[Random] = None):
        """ Initialise and randomise the feature set.

        :param random: Random generator.
        """
        assert isinstance(random, (Random, NONE_TYPE)), check()
        # ----------
        values = list(self._values)
        if random:
            random.shuffle(values)
        self._features = [Feature(n, v) for n, v in enumerate(values)]
        if len(self._features) == 1:
            self._feature = self._features[0]

    def get_features(self, order:
                     Union[int, Random, NONE_TYPE] = None) -> list[Feature]:
        """Return an ordered copy of the features. This can be:
        - ordered by usage, ascending
        - randomly ordered
        - forward, starting at a fixed point
        - backwards, starting at a fixed point

        :param order: Order method for iteration.
        """
        assert isinstance(order, (int, Random, NONE_TYPE)), check()
        # ----------
        features = list(self._features)
        if not features:
            return []
        elif order is None:
            features.sort(key=lambda f: f.count)
            return features
        elif isinstance(order, Random):
            order.shuffle(features)
            return features
        elif order < 0:
            features.reverse()
        order = order % len(features)
        return features[order:] + features[:order]

    def get_value(self) -> Any:
        """Return the feature value for the dimension. If the feature is not
        set, select the one with the lowest count and record it. This method
        is expected to be used to fill in unfilled dimensions when iterating
        the final result."""
        if self._features:
            if self._feature:
                return self._feature.value
            else:
                features = list(self._features)
                features.sort(key=lambda f: f.count)
                feature = features[0]
                feature.count += 1
                return feature.value
        else:
            return None

    @property
    def feature(self) -> Optional[Feature]:
        """Current feature value of the dimension."""
        return self._feature

    @feature.setter
    def feature(self, value: Optional[Feature]):
        assert isinstance(value, (Feature, NONE_TYPE)), check()
        # ----------
        self._feature = value

    @property
    def feature_index(self) -> Optional[int]:
        """Current feature index of the dimension."""
        if self._feature:
            return self._feature.index
        else:
            return None

    @feature_index.setter
    def feature_index(self, value: Optional[int]):
        assert isinstance(value, (int, NONE_TYPE)), check()
        # ----------
        if value is None:
            self._feature = None
        else:
            self._feature = self._features[value]
