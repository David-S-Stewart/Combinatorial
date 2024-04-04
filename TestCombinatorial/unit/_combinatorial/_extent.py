"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from unittest import TestCase
from combinatorials import Dimension, Extent


class _Extent(TestCase):

    """Unit tests for Extent class."""

    def test_evaluate_dimension_not_set(self):
        """Evaluate an extent where the dimension is not set."""
        extent = Extent('a', (1,))
        try:
            # This will always fail. It is a design error if encountered.
            extent.evaluate()
        except Exception:
            pass
        else:
            self.fail()

    def test_evaluate_no_dimension_feature(self):
        """Evaluate an extent for truth where the feature is not set."""
        dimension = Dimension('a', (1, 2, 3))
        extent = Extent('a', (1,))
        extent.dimension = dimension
        self.assertFalse(extent.evaluate())

    def test_evaluate_true(self):
        """Evaluate an extent for truth."""
        dimension = Dimension('a', (1, 2, 3))
        extent = Extent('a', (1,))
        extent.dimension = dimension
        dimension.feature = dimension.features[0]
        self.assertTrue(extent.evaluate())

    def test_evaluate_false(self):
        """Evaluate an extent for truth."""
        dimension = Dimension('a', (1, 2, 3))
        extent = Extent('a', (1,))
        extent.dimension = dimension
        dimension.feature = dimension.features[1]
        self.assertFalse(extent.evaluate())

    def test_evaluate_out_of_range(self):
        """Evaluate an extent for truth where the extent is out of range."""
        dimension = Dimension('a', (1, 2, 3))
        extent = Extent('a', (4,))
        extent.dimension = dimension
        dimension.feature = dimension.features[1]
        self.assertFalse(extent.evaluate())
