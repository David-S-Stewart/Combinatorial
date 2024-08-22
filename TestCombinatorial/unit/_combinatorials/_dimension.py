"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from random import Random
from unittest import TestCase
from combinatorials import Dimension


class _Dimension(TestCase):

    """Unit tests for Dimension class."""

    def test_initialise_empty(self):
        """Test initialise with empty feature list."""
        dimension = Dimension('identity', ())
        features = dimension.features
        self.assertEqual(features, [])
        dimension.initialise()
        self.assertEqual(dimension.features, features)
        # Initialising random in this case has no effect.
        dimension.initialise(Random(0))
        self.assertEqual(dimension.features, features)

    def test_initialise_single(self):
        """Test initialise with single feature list."""
        dimension = Dimension('identity', (0,))
        features = dimension.features
        dimension.initialise()
        self.assertEqual(dimension.features, features)
        # Initialising random in this case has no effect.
        dimension.initialise(Random(0))
        self.assertEqual(dimension.features, features)

    def test_initialise_multiple(self):
        """Test initialise with multiple feature list."""
        dimension = Dimension('identity', (0, 1, 2, 3))
        features = dimension.features
        dimension.initialise()
        self.assertEqual(dimension.features, features)
        # Initialising random in this case will create a different order.
        dimension.initialise(Random(0))
        self.assertNotEqual(dimension.features, features)
        self.assertEqual(len(dimension.features), len(features))

    def test_get_features_empty(self):
        """Test get_features with an empty dimension."""
        dimension = Dimension('identity', ())
        self.assertEqual(len(dimension.get_features()), 0)
        self.assertEqual(len(dimension.get_features(Random(0))), 0)
        self.assertEqual(len(dimension.get_features(-1)), 0)
        self.assertEqual(len(dimension.get_features(0)), 0)
        self.assertEqual(len(dimension.get_features(1)), 0)

    def test_get_features_single(self):
        """Test get_features with an empty dimension."""
        dimension = Dimension('identity', (0, ))
        self.assertEqual(len(dimension.get_features()), 1)
        self.assertEqual(len(dimension.get_features(Random(0))), 1)
        self.assertEqual(len(dimension.get_features(-1)), 1)
        self.assertEqual(len(dimension.get_features(0)), 1)
        self.assertEqual(len(dimension.get_features(1)), 1)

    def test_get_features_none(self):
        """Test get_features with default."""
        dimension = Dimension('identity', (0, 1, 2, 3))
        # With all counts equal, input order will equal output order.
        self.assertEqual([f.index for f in dimension.get_features()],
                         [0, 1, 2, 3])
        # With different counts, output returns lowest count order.
        dimension.features[0].count = 2
        dimension.features[1].count = 6
        dimension.features[2].count = 0
        dimension.features[3].count = 5
        self.assertEqual([f.index for f in dimension.get_features()],
                         [2, 0, 3, 1])

    def test_get_features_random(self):
        """Test get_features with random."""
        dimension = Dimension('identity', (0, 1, 2, 3))
        features = [f.index for f in dimension.get_features(Random(0))]
        self.assertNotEqual(dimension.features, features)
        self.assertEqual(len(dimension.features), len(features))

    def test_get_features_positive(self):
        """Test get_features with positive offset."""
        dimension = Dimension('identity', (0, 1, 2, 3))
        self.assertEqual([f.index for f in dimension.get_features(0)],
                         [0, 1, 2, 3])
        self.assertEqual([f.index for f in dimension.get_features(1)],
                         [1, 2, 3, 0])
        self.assertEqual([f.index for f in dimension.get_features(2)],
                         [2, 3, 0, 1])
        self.assertEqual([f.index for f in dimension.get_features(3)],
                         [3, 0, 1, 2])
        # Wrap around.
        self.assertEqual([f.index for f in dimension.get_features(4)],
                         [0, 1, 2, 3])

    def test_get_features_negative(self):
        """Test get_features with negagtive offset."""
        dimension = Dimension('identity', (0, 1, 2, 3))
        self.assertEqual([f.index for f in dimension.get_features(-1)],
                         [0, 3, 2, 1])
        self.assertEqual([f.index for f in dimension.get_features(-2)],
                         [1, 0, 3, 2])
        self.assertEqual([f.index for f in dimension.get_features(-3)],
                         [2, 1, 0, 3])
        # Standard reverse (-len(features))
        self.assertEqual([f.index for f in dimension.get_features(-4)],
                         [3, 2, 1, 0])
        # Wrap around.
        self.assertEqual([f.index for f in dimension.get_features(-5)],
                         [0, 3, 2, 1])
