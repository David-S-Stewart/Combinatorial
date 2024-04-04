"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Generator
from itertools import product
from random import Random
from .feature import Feature
from .generator import Generator_


class SequenceGenerator(Generator_):

    """Generator that provides n-level solution sets using the standard
    coverages."""

    def get_features(self) -> Generator[tuple[Feature], None, None]:
        """Return an iterator through the SequenceGenerator."""
        if not self._dimensions:
            yield ()
        elif next((True for d in self._dimensions if len(d) == 0), False):
            return

        self._clear()
        random = Random(self._seed)
        dimensions = [d for d in self._dimensions if len(d) > 1]
        coverages = self.get_coverages()
        while coverages:
            self._order_coverages(coverages, random)
            # Select the retirement sub-combination.
            retire = coverages[0]
            retire.select(random)
            variable = [d for d in dimensions if d not in retire.dimensions]
            if variable:
                # Generate solutions.
                best = len(coverages)
                solutions = []
                for solution in product(*[d.select(random) for d in variable]):
                    for feature, dimension in zip(solution, variable):
                        dimension.feature = feature
                    if not self.is_constrained():
                        cover = len([c for c in coverages if c.is_covered()])
                        if cover == best:
                            solutions.append([d.feature for d in variable])
                            if best == 0:
                                break
                        if cover < best:
                            best = cover
                            solutions = [[d.feature for d in variable]]
                if solutions:
                    # Select a solution, cover and yield.
                    solution = solutions[0]
                    for feature, dimension in zip(solution, variable):
                        dimension.feature = feature
                    for coverage in coverages:
                        coverage.cover()
                    yield [d.feature for d in self._dimensions]
                else:
                    # This one is constrained out.
                    retire.cover()
            else:
                retire.cover()
                if not self.is_constrained():
                    yield [d.feature for d in self._dimensions]

            # Remove complete coverages and increment the counts.
            coverages = [c for c in coverages if False in c]
            for dimension in self._dimensions:
                dimension.feature.count += 1
