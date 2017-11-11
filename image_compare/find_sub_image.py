"""
Find one image inside another

Completely based on scikit-image.org/docs/0.9.x/auto_examples/plot_template.html
"""

import time

import numpy as np
import numpy.linalg as LA
import skimage.io as io
from skimage.feature import match_template


class Matcher:
    def __init__(self):
        self.correlation = None

    def extract_match(self, threshold):
        """
        Returns the x,y position of a within b if the correlation is above threshold

        @param threshold: float from -1 up to 1
        @return Top left corner of the match (or None if nothing topped threshold)
        """
        #import pdb; pdb.set_trace()
        # Having 1 matching blip isn't enough.
        # Honestly, we need to look for a subset the same size as subimage
        strongest = self.correlation.max()
        if strongest > threshold:
            top_left = np.argmax(self.correlation)
            ij = np.unravel_index(top_left, self.correlation.shape)
            return ij[::-1]

    def calculate_match(self, image, subimage):
        """
        This is where the work happens
        """
        start_time = time.time()
        self.correlation = match_template(image, subimage)
        correlated_time = time.time()
        # For color images, we have 3-D "matrices", with
        # 1 plane per color channel
        # But correlation is grayscale. And calculating the
        # norm only works on grayscale, anyway.
        # So ditch that, if it exists
        if self.correlation.ndim == 3:
            self.correlation = self.correlation.reshape(self.correlation.shape[0:2])
        length = LA.norm(self.correlation, ord=2)
        normalized = self.correlation / length
        calculated_time = time.time()
        rough_profile = 'Correlating took {} ms. Getting correlation from -1 to 1 took {} ms'
        print(rough_profile.format((correlated_time - start_time)*1000,
                                   (calculated_time - correlated_time)*1000))

    def compare_images(self, name1, name2, threshold):
        """
        Looks for a cropped version of name1 inside name2 (or vice-versa)

        @param name1: the name of an image file to examine
        @param name2: the name of an image file to examine
        @return
        """
        # Q: How much difference do we get by adding as_grey=True?
        x = io.imread(name1)
        y = io.imread(name2)
        if len(x) < len(y):
            y, x = x, y
        self.calculate_match(x, y)
        return self.extract_match(threshold)
