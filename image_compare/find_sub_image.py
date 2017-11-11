"""
Find one image inside another

Completely based on scikit-image.org/docs/0.9.x/auto_examples/plot_template.html
"""

import numpy as np
import skimage.io as io
from skimage.feature import match_template


def pick_match(a, b, threshold):
    """
    Returns the x,y position of a within b if the correlation is above threshold
    """
    if len(a) > len(b):
        b, a = a, b
    correlation = match_template(b, a)
    strongest = np.argmax(correlation)
    if strongest > threshold:
        ij = np.unravel_index(np.argmax(correlation), correlation.shape)
        return ij[::-1]


def compare_images(a, b, threshold):
    """
    If a is a cropped version of b (or vice versa) return top-left coordinate of that subset
    """
    x = io.imread(a)
    y = io.imread(b)
    return pick_match(x, y, threshold)
