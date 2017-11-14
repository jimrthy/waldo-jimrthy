#! /usr/bin/env python

"""
Unit testing
"""

# Sticking this in the same folder as "real" source files
# really isn't a great way to organize bigger projects.
# For something this small, it's convenient

import unittest

from skimage import data

import find_sub_image


class Subset(unittest.TestCase):
    def setUp(self):
        self.src = data.coins()
        self.subset = self.src[170:220, 75:130]

    def test_a_b(self):
        correlation = find_sub_image.calculate_match(self.src,
                                                     self.subset)
        position = find_sub_image.extract_match(correlation, 0.99)
        self.assertEqual(position[0], 75)
        self.assertEqual(position[1], 170)


class Mismatch(unittest.TestCase):
    def setUp(self):
        self.a = data.camera()
        self.b = data.coins()

    def test_thresholds(self):
        correlation = find_sub_image.calculate_match(self.a, self.b)
        position = find_sub_image.extract_match(correlation, 1.0)
        self.assertIsNone(position)
        position = find_sub_image.extract_match(correlation, 0.5)
        self.assertIsNone(position)
        # Eventually, we *can* drop the threshold low enough to get a
        # match
        position = find_sub_image.extract_match(correlation, 0.1)
        self.assertEqual(position, (24, 0))


if __name__ == '__main__':
    unittest.main()
