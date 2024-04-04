"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Generator
from unittest import TestCase
from combinatorials import Combinatorial, Dimension, Generator_
from combinatorials import KnuthGenerator, ProductGenerator, SequenceGenerator


class _Generator(TestCase):

    """Unit tests for Generator_ class."""

    # Test unconstrained generation.

    def get_dimensions(self, dimensions_minimum: int,
                       dimensions_maximum: int, minimum: int,
                       maximum: int) -> Generator[list[Dimension], None, None]:
        """Yield a generator of dimensions."""
        for features in range(minimum, maximum + 1):
            for dimensions in range(dimensions_minimum,
                                    dimensions_maximum + 1):
                result = []
                for index, _ in enumerate(range(dimensions)):
                    result.append(Dimension(f'D{index}',
                                            list(range(features))))
                yield result

    def _test_generator_zero_dimensions(self):
        """Any generator with zero dimensions should yield a single, empty
        tuple. No constraint can apply.
        """
        dimensions = []
        for class_ in (Combinatorial, KnuthGenerator, ProductGenerator,
                       SequenceGenerator):
            count = 0
            generator = class_(dimensions)
            for combination in generator:
                count += 1
                self.assertEqual(combination, ())
            self.assertEqual(count, generator.minimum_length)
            generator.validate()

    def _test_generator_empty_dimensions(self):
        """Any generator with any empty dimensions should yield no tuples.
        Constraints can apply but have no effect.
        """
        dimensions = [Dimension('a', [])]
        for class_ in (Combinatorial, KnuthGenerator, ProductGenerator,
                       SequenceGenerator):
            count = 0
            generator = class_(dimensions)
            for combination in generator:
                count += 1
                self.assertEqual(len(combination), len(generator.dimensions))
            self.assertEqual(count, generator.minimum_length)
            generator.validate()

    def _test_generator_single_dimension(self):
        """Any generator with single effective dimension should yield only
        that dimension changing within the feature set.
        """
        dimensions = [Dimension('a', [0, 1, 2, 3])]
        for class_ in (Combinatorial, KnuthGenerator, ProductGenerator,
                       SequenceGenerator):
            count = 0
            generator = class_(dimensions)
            for combination in generator:
                count += 1
                self.assertEqual(len(combination), len(generator.dimensions))
            self.assertEqual(count, generator.minimum_length)
            generator.validate()

    def _test_generator_coverage_1(self):
        """Test sets of balanced dimensions against coverage = 1. These
        should all return the minimum."""
        for dimensions in self.get_dimensions(2, 6, 2, 4):
            for class_ in (Combinatorial, KnuthGenerator, SequenceGenerator):
                count = 0
                generator = class_(dimensions, coverage=1)
                for combination in generator:
                    count += 1
                    self.assertEqual(len(combination),
                                     len(generator.dimensions))
                self.assertEqual(count, generator.minimum_length)
                generator.validate()

    def _test_generator_coverage_1_product(self):
        """Test sets of balanced dimensions against coverage = 1. The
        ProductGenerator does not support this."""
        for dimensions in self.get_dimensions(2, 6, 2, 4):
            try:
                generator = ProductGenerator(dimensions, coverage=1)
                # The exception occurs on the call to the generator.
                for _ in generator:
                    pass
            except Exception:
                pass
            else:
                self.fail()
