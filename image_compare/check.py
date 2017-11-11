#! /usr/bin/env python

"""
Unit testing
"""

# Sticking this in the same folder is a bad idea for bigger projects.
# For something this small, it's convenient

import unittest

from skimage import data

import find_sub_image


class Subset(unittest.TestCase):
    def setUp(self):
        self.src = data.coins()
        self.subset = self.src[170:220, 75:130]
        self.matcher = find_sub_image.Matcher()

    def test_a_b(self):
        self.matcher.calculate_match(self.src, self.subset)
        position = self.matcher.extract_match(0.99)
        self.assertEqual(position[0], 75)
        self.assertEqual(position[1], 170)


class Mismatch(unittest.TestCase):
    def setUp(self):
        self.a = data.camera()
        self.b = data.coins()
        self.matcher = find_sub_image.Matcher()

    def test_thresholds(self):
        self.matcher.calculate_match(self.a, self.b)
        position = self.matcher.extract_match(1.0)
        self.assertIsNone(position)
        position = self.matcher.extract_match(0.5)
        self.assertIsNone(position)
        # Eventually, we *can* drop the threshold low enough to get a match
        position = self.matcher.extract_match(0.1)
        self.assertEqual(position, (24, 0))


if __name__ == '__main__':
    unittest.main()
