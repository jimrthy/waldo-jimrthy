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

    def test_a_b(self):
        position = find_sub_image.pick_match(self.subset, self.src, 1.0)
        self.assertEqual(position[0], 170)
        self.assertEqual(position[1], 75)

    def test_b_a(self):
        position = find_sub_image.pick_match(self.src, self.subset, 1.0)
        self.assertEqual(position[0], 170)
        self.assertEqual(position[1], 75)


class Mismatch(unittest.TestCase):
    def setUp(self):
        self.a = data.coins()
        self.b = data.camera()

    def test_thresholds(self):
        position = find_sub_image.pick_match(self.a, self.b, 1.0)
        self.assertIsNone(position)
        position = find_sub_image.pick_match(self.a, self.b, 0.5)
        self.assertIsNone(position)


if __name__ == '__main__':
    unittest.main()
