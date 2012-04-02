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

import settings
from dotlang.translate import parse as parse_lang


def gettext_extract():
    """
    Extract strings from templates, using gettext tools, then convert to
    .lang.
    """
    try:
        tmpdir = tempfile.mkdtemp()
        potfile = join(tmpdir, 'messages.pot')

        sys.stderr.write('Extracting strings from templates...\n')
        try:
            check_call(['xgettext', '-L', 'Python', '-o', potfile] +
                       glob.glob(join(settings.ROOT, 'templates', '*.html')))
        except CalledProcessError, e:
             sys.stderr.write('Error extracting strings: %s\n' % e)
             sys.exit(1)

        extract_lang(potfile)
        sys.stderr.write('Done.\n')
    finally:
        shutil.rmtree(tmpdir)


def _extract_content(s):
    """Strip the first word and quotes from msgids."""
    return s[s.find(' ')+1:].strip('"')


def parse_po(path):
    """Extract messages from a .pot file."""
    msgs = []

    if not os.path.exists(path):
        return msgs

    with codecs.open(path, 'r', 'utf-8') as lines:
        msgid = None

        for line in lines:
            line = line.strip()
            if line.startswith('msgid'):
                msgid = _extract_content(line)
            elif line.startswith('msgstr') and msgid:
                msgs.append(msgid)
            else:
                msgid = None

    return msgs


def lang_translations(lang_file):
    """Read existing translations for a .lang file."""
    trans = []

    if os.path.exists(lang_file):
        trans.extend(parse_lang(lang_file).keys())

    return trans


def extract_lang(potfile):
    """Convert .pot file to .lang file."""
    for lang in settings.LANGS:
        sys.stderr.write('Creating %s/%s\n' % (lang, settings.LANG_FILENAME))
        output_file = join(settings.LOCALE_DIR, lang, settings.LANG_FILENAME)
        lang_trans = lang_translations(output_file)  # Existing translations

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with codecs.open(output_file, 'a+', 'utf-8') as out:
            # Keep existing files in place, append new strings.
            for msg in parse_po(potfile):
                if msg not in lang_trans:
                    out.write(";%s\n%s\n\n\n" % (msg, msg))
