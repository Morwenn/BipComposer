#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gettext
import locale
import os


LOCALE_DIR = os.path.join(os.path.abspath('.'),
                          'bipcomposer',
                          'locale')

# Default language is English from the UK
languages = ['en_GB']

# Find available translations by looking
# at the dir names in LOCALE_DIR
for _path in os.listdir(LOCALE_DIR):
    if not _path.startswith('_'): # Ignore __pycache__
        if os.path.isdir(os.path.join(LOCALE_DIR, _path)):
            languages.append(_path)
languages = set(languages) # Avoid duplicates

# Default locale used in the Adelie
default = locale.getdefaultlocale()[0]
if not default in languages:
    default = 'en_GB'

# Create the translations
_translations = {}
for _lang in languages:
    _translations[_lang] = gettext.translation('bipcomposer',
                                              LOCALE_DIR,
                                              [_lang])

# Install _() for the whole application
# with the default locale
_translations[default].install()


def set(language):
    """
    Change project language on the fly.
    
    :param language: Language code
    :type language: str
    :raises: ValueError
    """
    if language not in languages:
        raise ValueError("unknown locale: %s" % language)
    translations[language].install()


