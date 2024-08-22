"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from itertools import product
from unittest import TestCase
from combinatorials import Combinatorial, Dimension, Generator_
from combinatorials import MinusOneGenerator, SubCombination


class _Combinatorial(TestCase):

    """Unit tests for Combinatorial class."""

    @classmethod
    def validate(cls, combinatorial: Combinatorial) -> int:
        """Validate the generator by iteration and examination of the
        results. Validation will fail if any of the following are found:
        - A constrained combination
        - A duplicate combination
        - A sub-combination not returned that is not constrained

        :var combinatorial: The Combinatorial to validate.
        """
        if combinatorial.generator.minimum == 0:
            return 0
        errors = []
        generator = combinatorial.generator
        option, seed = Combinatorial.get_option(generator)
        duplicates = SubCombination(generator.dimensions)
        sub_combinations = generator.get_sub_combinations()
        # Iterate and cover.
        count = 0
        for combination in generator.iterate(option, seed):
            count += 1
            indexes = [f.index if f else None for f in combination]
            if generator.is_constrained():
                errors.append(f'Constrained: {indexes}')
            if duplicates.is_covered:
                errors.append(f'Duplicate: {indexes}')
            duplicates.cover()
            for sub_combination in sub_combinations:
                sub_combination.cover()
        # Check for missing.
        for sub_combination in sub_combinations:
            for index in sub_combination.indexes_of(False):
                duplicates.sub_combination_index = None
                sub_combination.sub_combination_index = index
                combination = [d.feature.index if d.feature else None
                               for d in generator.dimensions]
                if not generator.is_constrained():
                    # This sub_combination can still be constrained out if
                    # several constraints work together to leave no instances.
                    dimensions = [d for d in generator.dimensions
                                  if not d.feature]
                    for features in product(*[d.features for d in dimensions]):
                        for feature, dimension in zip(features, dimensions):
                            dimension.feature = feature
                        if not generator.is_constrained():
                            # If an unconstrained combination is met, the
                            # requirement is not met.
                            errors.append(f'Missing: {combination} {index}')
                            break

        if errors:
            for error in errors:
                print(error)
            raise Exception()
        else:
            return count

    # Test core iterations.

    def test_null(self):
        """Test that an empty generation validates at minimum (1)."""
        dimensions = []
        combinatorial = Combinatorial(dimensions, ())
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, Generator_)
        # The Generator_ class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 1)
        self.assertEqual(combinatorial.generator.coverage, 1)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_empty_dimension(self):
        """Test that a generation with an empty dimension validates at
        minimum (0).
        """
        dimensions = [Dimension('a', [])]
        combinatorial = Combinatorial(dimensions, ())
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, Generator_)
        # The Generator_ class always validates to minimum. No generator
        # actually supports this fully.
        self.assertEqual(combinatorial.generator.coverage, 0)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_single_dimension(self):
        """Test that a single generation validates at minimum (1)."""
        # In this case, the generator operates on zero dimensions and the
        # the single  is returned with fixed dimension values.
        dimensions = [Dimension('a', [0])]
        combinatorial = Combinatorial(dimensions, ())
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, Generator_)
        # The Generator_ class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 1)
        self.assertEqual(combinatorial.generator.coverage, 1)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_single_dimensions(self):
        """Test that multiple singles in a generation validates at
        minimum (1).
        """
        # In this case, the generator operates on zero dimensions and the
        # the single  is returned with fixed dimension values.
        dimensions = [Dimension('a', [0]),
                      Dimension('b', [0]),
                      Dimension('c', [0])]
        combinatorial = Combinatorial(dimensions, ())
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, Generator_)
        # The Generator_ class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 1)
        self.assertEqual(combinatorial.generator.coverage, 1)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_multiple_dimension(self):
        """Test that a multiple dimension generation validates at minimum."""
        dimensions = [Dimension('a', [0, 1, 2])]
        combinatorial = Combinatorial(dimensions, ())
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, Generator_)
        # The Generator_ class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 3)
        self.assertEqual(combinatorial.generator.coverage, 1)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_multiple_dimensions(self):
        """Test that a multiple generation validates at minimum."""
        dimensions = [Dimension('a', [0, 1, 2]),
                      Dimension('b', [0, 1, 2]),
                      Dimension('c', [0, 1, 2])]
        combinatorial = Combinatorial(dimensions, ())
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, Generator_)
        # The Generator_ class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 27)
        self.assertEqual(combinatorial.generator.coverage, 3)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_multiple_dimensions_coverage(self):
        """Test that a multiple generation validates at minimum."""
        dimensions = [Dimension('a', [0, 1, 2]),
                      Dimension('b', [0, 1, 2]),
                      Dimension('c', [0, 1, 2])]
        combinatorial = Combinatorial(dimensions, (), 2)
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, MinusOneGenerator)
        # The MinusOneGenerator class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 9)
        self.assertEqual(combinatorial.generator.coverage, 2)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)

    def test_multiple_dimensions_negative_coverage(self):
        """Test that a multiple generation validates at minimum."""
        dimensions = [Dimension('a', [0, 1, 2]),
                      Dimension('b', [0, 1, 2]),
                      Dimension('c', [0, 1, 2])]
        combinatorial = Combinatorial(dimensions, (), -1)
        # Note we want to assert only the Generator_ here.
        self.assertEqual(combinatorial.generator.__class__, MinusOneGenerator)
        # The MinusOneGenerator class always validates to minimum.
        self.assertEqual(combinatorial.generator.minimum, 9)
        self.assertEqual(combinatorial.generator.coverage, 2)
        self.assertEqual(self.validate(combinatorial),
                         combinatorial.generator.minimum)
