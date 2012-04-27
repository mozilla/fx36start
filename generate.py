#!/usr/bin/env python
import codecs
import glob
import os
import shlex
import shutil
import subprocess
import sys
import StringIO
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
helpers.load_filters(ENV)


optparser = OptionParser(usage='%prog --output-dir=/tmp/path/example')
optparser.add_option("--output-dir", action="store", dest="output_path",
                     help="Specify the output directory")
optparser.add_option('-f', '--force', action='store_true', dest='force',
                     default=False, help='Delete output dir if it exists.')
optparser.add_option('-m', '--minify', action='store_true', dest='minify',
                     default=False, help='Minify HTML, CSS, JS.')
optparser.add_option('-v', '--version', action='store', dest='version',
                    default=settings.BUILD_VERSION,
                    help="Version to generate. Accepts 'passive' or 'urgent'")
optparser.add_option('--nowarn', action='store_false', dest='warn',
                     default=True, help=("Don't warn if unknown L10n strings "
                                         "are encountered"))
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


def call(command, stdin):
    """Call a subprocess, feed it stdin data, return stdout."""
    proc = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, cwd=settings.ROOT)
    return proc.communicate(stdin.encode('utf-8'))[0].decode('utf-8')


def main():
    """Function run when script is run from the command line."""
    template = ENV.get_template('index.html')

    # allow parameter to override settings build version
    if options.version not in ('passive', 'urgent'):
        options.version = settings.BUILD_VERSION

    sys.stdout.write("Writing %s template to %s\n" % (options.version, OUTPUT_PATH))

    if os.path.exists(OUTPUT_PATH):
        if not options.force:
            sys.stderr.write('Output path "%s" exists, please remove it or '
                             'run with --force to overwrite automatically.\n' % (
                                 OUTPUT_PATH))
            sys.exit(1)
        else:
            shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    # Copy "root" files into output dir's root.
    for f in (glob.glob(os.path.join(settings.ROOT, 'root', '*')) +
              glob.glob(os.path.join(settings.ROOT, 'root', '.*'))):
        shutil.copy(f, OUTPUT_PATH)

    # Place static files into output dir.
    STATIC_PATH = os.path.join(OUTPUT_PATH, 'static')
    for folder in settings.STATIC_FOLDERS:
        folder_path = os.path.join(STATIC_PATH, folder)
        if options.minify and folder in ('css', 'js'):
            os.makedirs(folder_path)
            # concat
            data = StringIO.StringIO()
            for f in glob.glob(os.path.join(folder, '*.%s' % folder)):
                shutil.copyfileobj(open(f, 'r'), data)
            # minify
            data = call('java -jar java/yuicompressor.jar --type %s' % folder,
                        data.getvalue())
            write_output(folder_path, '{f}-min.{f}'.format(f=folder), data)
        else:
            shutil.copytree(os.path.join(settings.ROOT, folder), folder_path)

    for lang in settings.LANGS:
        # Make language dir, or symlink to fallback language
        LANG_PATH = os.path.join(OUTPUT_PATH, lang)
        if lang in settings.LANG_FALLBACK:
            os.symlink(settings.LANG_FALLBACK[lang], LANG_PATH)
            continue
        else:
            os.makedirs(LANG_PATH)

        # symlink static folders into language dir
        for folder in settings.STATIC_FOLDERS:
            os.symlink(os.path.join('..', 'static', folder),
                       os.path.join(LANG_PATH, folder))

        # Data to be passed to template
        data = {
            'LANG': lang,
            'DIR': 'rtl' if lang in settings.RTL_LANGS else 'ltr',
            'MINIFY': options.minify,
            'VERSION': options.version,
        }

        # Load _() translation shortcut for jinja templates and point it to dotlang.
        ENV.globals['_'] = lambda txt: translate(lang, txt, warn=options.warn)

        rendered = template.render(data)
        if options.minify:
            rendered = call('java -jar java/htmlcompressor.jar '
                            '--type html', rendered)
        write_output(LANG_PATH, 'index.html', rendered)


if __name__ == '__main__':
    main()
