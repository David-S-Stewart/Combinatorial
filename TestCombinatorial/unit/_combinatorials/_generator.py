"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection, Generator
from itertools import combinations_with_replacement, product
from unittest import TestCase
from combinatorials import Configuration, Dimension, Generator_
from combinatorials import SubCombination


class _Generator(TestCase):

    """Unit tests for Generator_ class."""

    @classmethod
    def validate(cls, generator: Generator_) -> int:
        """Validate the generator by iteration and examination of the
        results. Validation will fail if any of the following are found:
        - A constrained combination
        - A duplicate combination
        - A sub-combination not returned that is not constrained

        :var generator: The Generator to validate.
        """
        if generator.minimum == 0:
            return 0
        errors = []
        option, seed = Configuration.get_option(generator)
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

    def get_dimensions(self, sizes: Collection[int] = ()) -> list[Dimension]:
        """Get a set of dimensions for the given collection of sizes."""
        result = []
        for index, features in enumerate(sizes):
            identity = f'Dimension {index}'
            dimension = Dimension(identity, list(range(features)))
            result.append(dimension)
        return result

    def get_generators(self) -> Generator[Generator_, None, None]:
        """Return an iterator of valid Generator_ configurations."""
        for limit in range(1, 5):
            for x in combinations_with_replacement(range(6), limit):
                dimensions = self.get_dimensions(x)
                for coverage in range(0, 5):
                    yield Configuration.get_generator(dimensions, (),
                                                      coverage, 0)

    def test_unconstrained(self):
        """Test that a full spread of generators validates."""
        for generator in self.get_generators():
            self.validate(generator)
