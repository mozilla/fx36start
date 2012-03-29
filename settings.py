import os


ROOT = os.path.dirname(__file__)

# Static folders. All of these will be copied into the output dir, and
# symlinked from the locale directories.
STATIC_FOLDERS = ['css', 'fonts', 'img', 'js']

# Example languages.
# Either put a fixed list here or write some code to parse out locale/.
LANGS = ('de', 'en-US')
