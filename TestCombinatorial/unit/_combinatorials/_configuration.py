"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-08-20
:Compatibility: Python 3.9
:License:       MIT
"""

from unittest import TestCase
from combinatorials import Configuration, Dimension


class _Configuration(TestCase):

    """Unit tests for Configuration class."""

    def test_get_coverage_empty(self):
        """Effective coverage will be 1 for any configuration with zero
        dimensions.
        """
        for coverage in range(-5, 5):
            self.assertEqual(Configuration.get_coverage([], coverage), 1)

    def test_get_coverage_with_empty(self):
        """Effective coverage will be 1 for any configuration with zero
        effective dimensions.
        """
        for coverage in range(-5, 5):
            dimensions = [Dimension('identity1', [0]),
                          Dimension('identity2', [0]),
                          Dimension('identity3', [0])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 1)

    def test_get_coverage_empty_dimension(self):
        """Effective coverage will be 0 for any configuration with an empty
        dimension.
        """
        for coverage in range(-5, 5):
            dimensions = [Dimension('identity', [])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 0)

    def test_get_coverage_with_empty_dimension(self):
        """Effective coverage will be 0 for any configuration with an empty
        dimension.
        """
        for coverage in range(-5, 5):
            dimensions = [Dimension('identity1', [0]),
                          Dimension('identity2', [0, 1, 2]),
                          Dimension('identity3', [])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 0)

    def test_get_coverage_single_dimension(self):
        """Effective coverage with one effective dimension will always be 1."""
        for coverage in range(-5, 5):
            dimensions = [Dimension('identity', [0, 1, 2])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 1)

    def test_get_coverage_minimum(self):
        """Effective coverage will be 1 at a minimum."""
        for coverage in [1, -2, -3, -4]:
            dimensions = [Dimension('identity1', [0, 1, 2]),
                          Dimension('identity2', [0, 1, 2]),
                          Dimension('identity3', [0, 1, 2])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 1)

    def test_get_coverage_minimum_with_single(self):
        """Effective coverage will be 1 at a minimum."""
        for coverage in [1, -3, -4, -5]:
            dimensions = [Dimension('identity1', [0, 1, 2]),
                          Dimension('identity2', [0, 1, 2]),
                          Dimension('identity3', [0, 1, 2]),
                          Dimension('identity4', [0])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 1)

    def test_get_coverage_maximum(self):
        """Effective coverage will be number of effective dimensions at a
        maximum.
        """
        for coverage in [0, 3, 4, 5]:
            dimensions = [Dimension('identity1', [0, 1, 2]),
                          Dimension('identity2', [0, 1, 2]),
                          Dimension('identity3', [0, 1, 2])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 3)

    def test_get_coverage_maximum_with_single(self):
        """Effective coverage will be number of effective dimensions at a
        maximum.
        """
        for coverage in [0, 3, 4, 5]:
            dimensions = [Dimension('identity1', [0, 1, 2]),
                          Dimension('identity2', [0, 1, 2]),
                          Dimension('identity3', [0, 1, 2]),
                          Dimension('identity4', [0])]
            self.assertEqual(Configuration.get_coverage(dimensions,
                                                        coverage), 3)
