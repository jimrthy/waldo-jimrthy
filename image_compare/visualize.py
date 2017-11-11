#! /usr/bin/env python
"""
Script for visualizing what the comparison is doing
"""

import sys

import matplotlib.pyplot as plt
import skimage.io as io

import find_sub_image as finder


def display_subset(name1, name2):
    image = io.imread(name1)
    template = io.imread(name2)
    if len(image) < len(template):
        image, template = template, image
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(8, 3))
    ax1.imshow(template)
    ax1.set_axis_off()
    ax1.set_title('template')

    ax2.imshow(image)
    ax2.set_axis_off()
    ax2.set_title('image')

    matcher = finder.Matcher()
    matcher.calculate_match(image, template)
    top_left = matcher.extract_match(0.9)

    # highlight matched region
    shape = template.shape
    if len(shape) == 2:
        h, w = template.shape
    else:
        # Assume this means it's grayscale
        h, w, _ = template.shape
    rect = plt.Rectangle(top_left, w, h, edgecolor='r', facecolor='none')
    ax2.add_patch(rect)

    ax3.imshow(matcher.correlation)
    ax3.set_axis_off()
    ax3.set_title('`match template`\nresult')
    # highlight matched region
    ax3.autoscale(False)
    if top_left:
        x, y = top_left
        ax3.plot(x, y, 'o', markeredgecolor='r',
                 markerfacecolor='none',
                 markersize=10)
    else:
        print('Warning: no match found')

    plt.show()


if __name__ == '__main__':
    name1 = sys.argv[1]
    name2 = sys.argv[2]
    display_subset(name1, name2)
