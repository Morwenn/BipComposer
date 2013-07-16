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

import os.path


def addext(path, ext, match_case=False):
    """
    Add the given extension to the given
    path if this path does not already end
    with this extension.

    :param path: Original file path.
    :type path: str
    :param ext: File extension to add to the path.
    :type ext: str
    :param match_case: Whether to consider the extension case.
    :type match_case: bool
    """
    _name, _ext = os.path.splitext(path)
    if not match_case:
        ext = ext.lower()
        _ext = _ext.lower()
    if ext == _ext:
        return path
    else:
        return path + ext


if __name__ == '__main__':
    path = 'ham/spam.eggs'
    print(addext(path, '.eggs'))
    print(addext(path, '.blop'))
    print(addext(path, '.EGGS'))
    print(addext(path, '.EGGS', True))
