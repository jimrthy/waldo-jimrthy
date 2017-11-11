#! /bin/env python

import find_sub_image as finder


def usage():
    msg = """Usage:
python image_compare path/to/file1.jpg path/to/file2.png

Output: """
    print(msg)

def main(a, b):
    x, y = finder.compare_images(a, b):
        print "Cropped at position ({}, {})".format(x, y)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        usage()
    else:
        main(sys.argv[1], sys.argv[2])