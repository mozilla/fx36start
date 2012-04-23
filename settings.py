import os


ROOT = os.path.dirname(__file__)

# Static folders. All of these will be copied into the output dir, and
# symlinked from the locale directories.
STATIC_FOLDERS = ['css', 'fonts', 'img', 'js']

# L10n dir
LOCALE_DIR = os.path.join(ROOT, 'locale')
if not os.path.exists(LOCALE_DIR):
    LOCALE_DIR = os.path.join(ROOT, 'locale_test')

# .lang file, filename
LANG_FILENAME = 'fx36start.lang'

# List of languages.
LANGS = (
    'af', 'ar', 'as', 'ast', 'be', 'bg', 'bn-BD', 'bn-IN', 'ca', 'cs', 'cy',
    'da', 'de', 'el', 'en-GB', 'en-US', 'eo', 'es-AR', 'es-CL', 'es-ES',
    'es-MX', 'et', 'eu', 'fa', 'fi', 'fr', 'fy-NL', 'ga-IE', 'gd', 'gl',
    'gu-IN', 'he', 'hi-IN', 'hr', 'hu', 'id', 'is', 'it', 'ja', 'ka', 'kk',
    'kn', 'ko', 'ku', 'lt', 'lv', 'mk', 'ml', 'mn', 'mr', 'nb-NO', 'nl',
    'nn-NO', 'oc', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT', 'rm', 'ro', 'ru',
    'si', 'sk', 'sl', 'sq', 'sr', 'sv-SE', 'ta', 'ta-LK', 'te', 'th', 'tr',
    'uk', 'vi', 'zh-CN', 'zh-TW',
)

# RTL languages.
RTL_LANGS = ('ar', 'fa', 'he')

# Language fallbacks. Langs listed here will be symlinked to their respective
# fallbacks rather than generated on their owns. Both sides must exist in
# LANGS.
LANG_FALLBACK = {
    'be': 'ru',
    'en-GB': 'en-US',
    'es-CL': 'es-ES',
    'es-MX': 'es-ES',
    'ka': 'en-US',
    'mn': 'ru',
    'oc': 'fr',
}

# View to build - specify either 'passive' or 'urgent'
BUILD_VERSION = 'passive'
