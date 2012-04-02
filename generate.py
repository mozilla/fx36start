#!/usr/bin/env python
import os
import shutil
import sys
import codecs
import urllib2
from optparse import OptionParser

import settings


# Import vendor lib.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'vendor'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'vendor', 'jinja2'))


import jinja2

import helpers
from dotlang.translate import translate


ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader([
        os.path.join(settings.ROOT, 'templates'),
    ]), extensions=[])
# Hook up template filters.
ENV.filters['f'] = helpers.f  # |f(...)


optparser = OptionParser(usage='%prog --output-dir=/tmp/path/example')
optparser.add_option("--output-dir", action="store", dest="output_path",
                     help="Specify the output directory")
optparser.add_option('-f', '--force', action='store_true', dest='force',
                     default=False, help='Delete output dir if it exists.')
optparser.add_option('--nowarn', action='store_false', dest='warn',
                     default=True, help=("Don't warn if unknown L10n strings "
                                         "are encountered"))
optparser.add_option('-v', '--version', action='store', dest='version',
                    default='passive', help="Version to generate. Accepts 'passive' or 'urgent'")
(options, args) = optparser.parse_args()

OUTPUT_PATH = (options.output_path if options.output_path else
               os.path.join(settings.ROOT, 'html'))


def copy_file(output_dir, fileName):
    """Helper function that copies a file to a new folder."""
    resource_path = os.path.split(settings.ROOT)[0]
    shutil.copyfile(os.path.join(resource_path, fileName),
                    os.path.join(output_dir, fileName))


def write_output(output_dir, filename, text):
    """Helper function that writes a string out to a file."""
    f = codecs.open(os.path.join(output_dir, filename), 'w', 'utf-8')
    f.write(text)
    f.close()


def main():
    """Function run when script is run from the command line."""
    template = ENV.get_template('index.html')

    sys.stdout.write("Writing " + options.version + " template to " + OUTPUT_PATH + "...\n")

    if os.path.exists(OUTPUT_PATH):
        if not options.force:
            sys.stderr.write('Output path "%s" exists, please remove it or '
                             'run with --force to overwrite automatically.\n' % (
                                 OUTPUT_PATH))
            sys.exit(1)
        else:
            shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    STATIC_PATH = os.path.join(OUTPUT_PATH, 'static')
    for folder in settings.STATIC_FOLDERS:
        folder_path = os.path.join(STATIC_PATH, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        shutil.copytree(os.path.join(settings.ROOT, folder), folder_path)

    for lang in settings.LANGS:
        # Load _() translation shortcut for jinja templates and point it to dotlang.
        ENV.globals['_'] = lambda txt: translate(lang, txt, warn=options.warn)

        # Make language dir
        LANG_PATH = os.path.join(OUTPUT_PATH, lang)
        os.makedirs(LANG_PATH)

        # symlink static folders into language dir
        for folder in settings.STATIC_FOLDERS:
            os.symlink(os.path.join('..', 'static', folder),
                       os.path.join(LANG_PATH, folder))

        # Data to be passed to template
        data = {
            'LANG': lang,
            'DIR': 'rtl' if lang in settings.RTL_LANGS else 'ltr',
            'VERSION': options.version,
        }

        write_output(LANG_PATH, 'index.html', template.render(data))


if __name__ == '__main__':
    main()
