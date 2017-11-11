"""
Find one image inside another

Completely based on
scikit-image.org/docs/0.9.x/auto_examples/plot_template.html
"""

import time

import numpy as np
import skimage.io as io
from skimage.feature import match_template


class Matcher:
    """
    Calculates (and stores) a correlation between two images
    """
    def __init__(self):
        self.correlation = None

    def extract_match(self, threshold):
        """
        Returns the x,y position of a within b (if any)

        @param threshold: float from -1 up to 1
        @return Top left corner of the match (or None if nothing
        topped threshold)
        """
        # Having 1 matching blip isn't enough.
        # Honestly, we need to look for a subset the same size as subimage.
        # On the other hand, it seems to work out OK on my test images.
        strongest = self.correlation.max()
        if strongest > threshold:
            top_left = np.argmax(self.correlation)
            ij = np.unravel_index(top_left, self.correlation.shape)
            return ij[::-1]

    def calculate_match(self, image, subimage):
        """
        This is where the work happens
        """
        # This is slow.
        # But I don't really have anything else to use
        # as comparison.
        # The skimage mailing list implies that it will
        # run on the GPU. After the images' "first usage
        # on a GPU backed canvas."
        # TODO: Delve into that to see if it helps.
        self.correlation = match_template(image, subimage)

        # For color images, we have 3-D "matrices", with
        # 1 plane per color channel
        # But correlation should be grayscale.
        # Crazily enough, it doesn't seem to be.
        # Although it does only have color plane.
        # It would be interesting to dig in and find
        # out what's going on there.
        # Calculating the
        # norm only works on grayscale, anyway.
        # So ditch that, if it exists
        if self.correlation.ndim == 3:
            dims = self.correlation.shape[0:2]
            self.correlation = self.correlation.reshape(dims)

    def compare_images(self, name1, name2, threshold):
        """
        Looks for a cropped version of name1 inside name2 (or vice-versa)

        @param name1: the name of an image file to examine
        @param name2: the name of an image file to examine
        @return
        """
        # Comparing grayscale images may cut back on accuracy,
        # but it's very significantly faster.
        x = io.imread(name1, as_grey=True)
        y = io.imread(name2, as_grey=True)
        if len(x) < len(y):
            y, x = x, y
        self.calculate_match(x, y)
        return self.extract_match(threshold)
