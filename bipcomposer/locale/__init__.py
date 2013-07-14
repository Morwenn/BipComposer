#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the BipComposer project.
# Copyright (C) 2013 Morwenn
# Contact: Morwenn <morwenn29@hotmail.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

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


