import os


ROOT = os.path.dirname(__file__)

# Static folders. All of these will be copied into the output dir, and
# symlinked from the locale directories.
STATIC_FOLDERS = ['css', 'fonts', 'img', 'js']

# L10n dir
LOCALE_DIR = os.path.join(ROOT, 'locale')
if not os.path.exists(LOCALE_DIR):
    LOCALE_DIR = os.path.join(ROOT, 'locale_test')

# Example languages.
# Either put a fixed list here or write some code to parse out locale/.
LANGS = ('de', 'en-US')

# RTL languages.
RTL_LANGS = ('ar', 'fa', 'he')