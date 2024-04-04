"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from random import Random
from unittest import TestCase
from combinatorials import Coverage, Dimension


class _Coverage(TestCase):

    """Unit tests for Coverage class."""

    def test_index_to_indexes(self):
        """Test that index_to_indexes is reversible."""
        # This covers both directions of this conversion.
        coverage = Coverage([Dimension('one', ['a', 'b', 'c']),
                             Dimension('two', ['d', 'e', 'f', 'z', 'y']),
                             Dimension('three', ['g', 'h'])])
        for index in range(len(coverage)):
            indexes = coverage.index_to_indexes(index)
            self.assertEqual(coverage.indexes_to_index(indexes), index)

    def test_index_to_combination(self):
        """Test that index_to_combination is reversible."""
        # This covers both directions of this conversion.
        coverage = Coverage([Dimension('one', ['a', 'b', 'c']),
                             Dimension('two', ['d', 'e', 'f', 'z', 'y']),
                             Dimension('three', ['g', 'h'])])
        for index in range(len(coverage)):
            combination = coverage.index_to_combination(index)
            self.assertEqual(coverage.combination_to_index(combination), index)

    def test_indexes_to_combination(self):
        """Test that indexes_to_combination is reversible."""
        # This covers both directions of this conversion.
        coverage = Coverage([Dimension('one', ['a', 'b', 'c']),
                             Dimension('two', ['d', 'e', 'f', 'z', 'y']),
                             Dimension('three', ['g', 'h'])])
        for index in range(len(coverage)):
            indexes = coverage.index_to_indexes(index)
            combination = coverage.indexes_to_combination(indexes)
            self.assertEqual(coverage.combination_to_indexes(combination),
                             indexes)

    def test_clear(self):
        """Test that clear zeros the coverage."""
        random = Random()
        coverage = Coverage([Dimension('one', ['a', 'b', 'c']),
                             Dimension('two', ['d', 'e', 'f', 'z', 'y']),
                             Dimension('three', ['g', 'h'])])
        for _ in range(5):
            coverage.select(random)
            coverage.cover()
        # Test using base class functionality.
        self.assertTrue(True in coverage)
        coverage.clear()
        self.assertTrue(False in coverage)
