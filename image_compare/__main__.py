#! /bin/env python

import sys
import traceback as tb

import find_sub_image as finder


def usage():
    msg = """Usage:
python image_compare path/to/file1.jpg path/to/file2.png

Output: """
    print(msg)


def main(a, b):
    try:
        result = finder.compare_images(a, b, 0.9)
        coordinate = result['top_left']
        if coordinate:
            fmt = ("{} is a cropped version of {}, "
                   "starting at at position {}")
            print(fmt.format(result['template_name'],
                             result['image_name'],
                             coordinate))
    except Exception:
        tb.print_exc()
        return -1
    else:
        return 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        sys.exit(main(sys.argv[1], sys.argv[2]))
