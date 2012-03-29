#!/usr/bin/env python

import os
import shutil
import sys
import urllib2
from optparse import OptionParser


# Import vendor lib.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'vendor'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'vendor', 'jinja2'))


import jinja2


CURRENT_PATH = os.path.dirname(__file__)

ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader([
        os.path.join(CURRENT_PATH, 'templates'),
    )]), extensions=['jinja2.ext.i18n'])
# FIXME: stub out gettext functionality
ENV.install_null_translations()

optparser = OptionParser(usage='%prog --output-dir=/tmp/path/example')
optparser.add_option("--output-dir", action="store", dest="output_path",
                     help="Specify the output directory")
(options, args) = optparser.parse_args()

OUTPUT_PATH = options.output_path if options.output_path else 'html'


def copy_file(output_dir, fileName):
    """Helper function that copies a file to a new folder."""
    resource_path = os.path.split(CURRENT_PATH)[0]
    shutil.copyfile(os.path.join(resource_path, fileName),
                    os.path.join(output_dir, fileName))


def write_output(output_dir, filename, text):
    """Helper function that writes a string out to a file."""
    f = open(os.path.join(output_dir, filename), 'w')
    f.write(text)
    f.close()


def main():
    """Function run when script is run from the command line."""
    template = ENV.get_template('index.html')

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    for folder in ['css', 'fonts', 'img', 'js']:
        folder_path = os.path.join(CURRENT_PATH, OUTPUT_PATH, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        shutil.copytree(os.path.join(CURRENT_PATH, folder), folder_path)

    # Data to be passed to template
    data = {}

    write_output(OUTPUT_PATH, 'index.html', template.render(data))


if __name__ == '__main__':
    main()
