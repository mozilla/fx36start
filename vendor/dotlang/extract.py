"""
Extract strings from template dir and convert them into a .lang file.

Partially lifted from bedrock.
"""

import codecs
import glob
import os
import shutil
import sys
import tempfile
from os.path import join
from subprocess import CalledProcessError, check_call

import jinja2

import helpers
import settings
from dotlang.translate import parse as parse_lang


ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader([
        os.path.join(settings.ROOT, 'templates'),
    ]), extensions=['jinja2.ext.i18n'])


def gettext_extract():
    """Extract strings from templates, then convert to .lang."""
    sys.stderr.write('Extracting strings from templates...\n')

    templates = glob.glob(join(settings.ROOT, 'templates', '*.html'))

    extracted = []
    for tpl in templates:
        for lnum, func, trans in ENV.extract_translations(open(tpl).read()):
            if trans not in extracted:  # Avoid dupes.
                extracted.append(trans)

    extract_lang(extracted)
    sys.stderr.write('Done.\n')


def lang_translations(lang_file):
    """Read existing translations for a .lang file."""
    trans = []

    if os.path.exists(lang_file):
        trans.extend(parse_lang(lang_file).keys())

    return trans


def extract_lang(extracted):
    """Merge extracted strings into .lang files."""
    for lang in settings.LANGS:
        if lang in settings.LANG_FALLBACK:
            sys.stderr.write('Skipping %s (falls back to %s)\n' % (
                lang, settings.LANG_FALLBACK[lang]))
            continue

        sys.stderr.write('Creating %s/%s\n' % (lang, settings.LANG_FILENAME))

        output_dir = join(settings.LOCALE_DIR, lang)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = join(output_dir, settings.LANG_FILENAME)
        lang_trans = lang_translations(output_file)  # Existing translations

        with codecs.open(output_file, 'a+', 'utf-8') as out:
            # Keep existing files in place, append new strings.
            for msg in extracted:
                if msg not in lang_trans:
                    out.write(";%s\n%s\n\n\n" % (msg, msg))
