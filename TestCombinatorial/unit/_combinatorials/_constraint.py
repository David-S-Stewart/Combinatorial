"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from unittest import TestCase
from combinatorials import Constraint, Dimension, Extent


class _Constraint(TestCase):

    """Unit tests for Constraint class."""

    def test_evaluate_dimension_not_set(self):
        """Evaluate an constraint where the dimension is not set."""
        constraint = Constraint([Extent('a', (1,))])
        self.assertFalse(constraint.evaluate())

    def test_evaluate_no_dimension_feature(self):
        """Evaluate an extent for truth where the feature is not set."""
        dimension = Dimension('a', (1, 2, 3))
        constraint = Constraint([Extent('a', (1,))])
        constraint.extents[0].dimension = dimension
        self.assertFalse(constraint.evaluate())

    def test_evaluate_true(self):
        """Evaluate an extent for truth."""
        dimension = Dimension('a', (1, 2, 3))
        constraint = Constraint([Extent('a', (1,))])
        constraint.extents[0].dimension = dimension
        dimension.feature = dimension.features[0]
        self.assertTrue(constraint.evaluate())

    def test_evaluate_false(self):
        """Evaluate an extent for truth."""
        dimension = Dimension('a', (1, 2, 3))
        constraint = Constraint([Extent('a', (1,))])
        constraint.extents[0].dimension = dimension
        dimension.feature = dimension.features[1]
        self.assertFalse(constraint.evaluate())

    def _test_evaluate_out_of_range(self):
        """Evaluate an extent for truth where the extent is out of range."""
        dimension = Dimension('a', (1, 2, 3))
        constraint = Constraint([Extent('a', (4,))])
        constraint.extents[0].dimension = dimension
        dimension.feature = dimension.features[1]
        self.assertFalse(constraint.evaluate())
