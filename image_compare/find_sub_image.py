"""
Find one image inside another

Completely based on
scikit-image.org/docs/0.9.x/auto_examples/plot_template.html
"""

import numpy as np
import skimage.io as io
from skimage.feature import match_template


def extract_match(correlation, threshold):
    """
    Returns the x,y position of a within b (if any)

    @param threshold: float from -1 up to 1
    @return Top left corner of the match (or None if nothing
    topped threshold)
    """
    # Having 1 matching blip seems like it shouldn't enough.
    # It seems as though we need to look for a subset the same size as
    # subimage. That "seems" stems from a lack of understanding the
    # fundamental algorithms that are involved here.
    # This is basically treating the bytes as wave functions. Peaks correspond
    # to the "start" of the intersection.
    strongest = correlation.max()
    if strongest > threshold:
        top_left = np.argmax(correlation)
        ij = np.unravel_index(top_left, correlation.shape)
        return ij[::-1]


def calculate_match(image, template):
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
    correlation = match_template(image, template)

    # For color images, we have 3-D "matrices", with
    # 1 plane per color channel
    # But correlation should be grayscale.
    # Crazily enough, it doesn't seem to be.
    # Although it does only have color plane.
    # It would be interesting to dig in and find
    # out what's going on there.
    # Calculating the
    # norm only works on grayscale, anyway.
    # So ditch the extra color planes, if any
    if correlation.ndim == 3:
        dims = correlation.shape[0:2]
        correlation = correlation.reshape(dims)
    return correlation


def load_images(name1, name2):
    """
    Read image files into byte arrays

    @return A dict that contains:
    template: smaller image
    image larger image
    template_name: name of the smaller image file
    image_name: name of the larger image file
    """
    # Comparing grayscale images may cut back on accuracy,
    # but it's very significantly faster.
    x = io.imread(name1, as_grey=True)
    y = io.imread(name2, as_grey=True)
    result = {}
    if len(x) < len(y):
        y, x = x, y
        result['template_name'] = name1
        result['image_name'] = name2
    else:
        result['template_name'] = name2
        result['image_name'] = name1
    result['template'] = y
    result['image'] = x
    return result


def compare_images(name1, name2, threshold):
    """
    Looks for a cropped version of name1 inside name2 (or vice-versa)

    @param name1: the name of an image file to examine
    @param name2: the name of an image file to examine
    @return A dict that contains:
    template: smaller image
    image larger image
    template_name: name of the smaller image file
    image_name: name of the larger image file
    top_left: position of start point (if any)
    """
    description = load_images(name1, name2)
    correlation = calculate_match(description['image'],
                                  description['template'])
    result = extract_match(correlation, threshold)
    description['top_left'] = result
    return description
