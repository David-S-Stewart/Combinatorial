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


class KnuthGenerator(Generator_):

    """Generator that provides n-level solution sets based on Knuth's
    Algorithm X. This generator will find the best combination but scales
    very badly.
    """

    def get_features(self) -> Generator[tuple[Feature], None, None]:
        """Return an iterator through the KnuthGenerator."""
        random = Random(self._seed)
        coverages = self.get_coverages()

        def process(feature_sets: list[tuple], products: list[product]):
            # Process the current combination until a good match is found.
            while True:
                feature_sets[-1] = next(products[-1])
                for feature, dimension in zip(feature_sets[-1],
                                              self.effective_dimensions):
                    dimension.feature = feature
                cover = len([c for c in coverages if c.is_covered()])
                if cover == 0:
                    for coverage in coverages:
                        coverage.cover()
                    break

        def forward(feature_sets: list[tuple], products: list[product]):
            # Get a generator for the next combination.
            feature_sets.append(())
            products.append(product(*[d.select(random) for d in
                                      self.effective_dimensions]))

        def back(feature_sets: list[tuple], products: list[product]):
            # Backtrack to the last combination.
            feature_sets.pop()
            for feature, dimension in zip(feature_sets[-1],
                                          self.effective_dimensions):
                dimension.feature = feature
            for coverage in coverages:
                coverage.uncover()
            products.pop()

        if not self._dimensions:
            yield ()
        elif next((True for d in self._dimensions if len(d) == 0), False):
            pass
        else:
            feature_sets = []
            products = []
            forward(feature_sets, products)
            while True:
                try:
                    process(feature_sets, products)
                    if [c for c in coverages if False not in c]:
                        break
                except StopIteration:
                    back(feature_sets, products)
                else:
                    forward(feature_sets, products)

            for features in feature_sets:
                for feature, dimension in zip(features,
                                              self.effective_dimensions):
                    dimension.feature = feature
                yield features
