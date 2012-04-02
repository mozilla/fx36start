#!/usr/bin/env python
import os
import sys

# Import vendor lib.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'vendor'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'vendor', 'jinja2'))

from dotlang.extract import gettext_extract


def main():
    """Function run when script is run from the command line."""
    gettext_extract()


if __name__ == '__main__':
    main()
