"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from random import Random
from unittest import TestCase
from combinatorials import Dimension, SubCombination


class _SubCombination(TestCase):

    """Unit tests for Coverage class."""

    def test_sequence(self):
        """Test sub-combinations by filling sequentially and testing each
        step.
        """
        sub_combination = SubCombination([Dimension('1', [0, 1, 2, 3]),
                                          Dimension('2', [0, 1, 2]),
                                          Dimension('3', [0, 1])])
        self.assertFalse(True in sub_combination)
        for index, _ in enumerate(sub_combination):
            sub_combination.sub_combination_index = index
            self.assertEqual(index, sub_combination.sub_combination_index)
            self.assertFalse(sub_combination.is_covered)
            sub_combination.cover()
            self.assertTrue(sub_combination.is_covered)
        self.assertFalse(False in sub_combination)

    def test_random(self):
        """Test sub-combinations by filling randomly and testing each step."""
        random = Random()
        sub_combination = SubCombination([Dimension('1', [0, 1, 2, 3]),
                                          Dimension('2', [0, 1, 2]),
                                          Dimension('3', [0, 1])])
        self.assertFalse(True in sub_combination)
        for _ in sub_combination:
            index = sub_combination.random_index(False, random)
            sub_combination.sub_combination_index = index
            self.assertEqual(index, sub_combination.sub_combination_index)
            self.assertFalse(sub_combination.is_covered)
            sub_combination.cover()
            self.assertTrue(sub_combination.is_covered)
        self.assertFalse(False in sub_combination)
