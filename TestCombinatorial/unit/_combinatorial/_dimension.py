"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from random import Random
from unittest import TestCase
from combinatorials import Dimension, Option


class _Dimension(TestCase):

    """Unit tests for Dimension class."""

    def test_select(self):
        """Test Select for default option."""
        random = Random()
        dimension = Dimension('a', (1, 2, 3))
        # In this case, the lists will be equal.
        self.assertEqual(dimension.select(random), dimension.features)

    def test_select_shuffle(self):
        """Test Select for default option."""
        random = Random()
        dimension = Dimension('a', (1, 2, 3))
        dimension.option = Option.FEATURE_RANDOM
        # These can still be equal!
        for _ in range(10):
            if dimension.select(random) != dimension.features:
                return
        # 10 perfect shuffles in a row is unlikely.
        self.fail()

    def test_select_count_minimum(self):
        """Test select ordered by minimum count."""
        random = Random()
        dimension = Dimension('a', (1, 2, 3))
        dimension.option = Option.FEATURE_COUNT_MINIMUM
        dimension.features[0].count = 2
        dimension.features[1].count = 3
        dimension.features[2].count = 1
        self.assertEqual(dimension.select(random), [dimension.features[2],
                                                    dimension.features[0],
                                                    dimension.features[1]])

    def test_select_count_maximum(self):
        """Test select ordered by maximum count."""
        random = Random()
        dimension = Dimension('a', (1, 2, 3))
        dimension.option = Option.FEATURE_COUNT_MAXIMUM
        dimension.features[0].count = 2
        dimension.features[1].count = 3
        dimension.features[2].count = 1
        self.assertEqual(dimension.select(random), [dimension.features[1],
                                                    dimension.features[0],
                                                    dimension.features[2]])
