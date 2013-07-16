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

import xml.etree.ElementTree as ET

from PySide.QtCore import (
    QObject,
    Signal
)

from .note import Note
from bipcomposer.gui.CanvasScore import CanvasScore


class Score(QObject):
    """
    Score. In a MVC, this would be both the Model and
    the Controller parts, while CanvasScore would be
    the View part and a bit of the Controller one too.
    """

    _path = ""          # Score file (.bcf)
    _name = ""          # Name of the score (generally generated from the path)
    _modified = False   # Whether it the score has been modified

    # Corresponding signals
    pathChanged = Signal(str)
    nameChanged = Signal(str)    

    notes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = CanvasScore(self)

    def load(self, fname=None):
        """
        Loads the given .bcf file if given.
        Otherwise, loads the cached one.

        :param fname: .bcf file to load.
        :type fname: str
        """
        # FIXME
        if fname:
            self.path = fname
        raise NotImplementedError

    def save(self, fname=None):
        """
        Saves the score to the given .bcf file.

        :param fname: .bcf file where to save the score.
        :type fname: str
        """
        raise NotImplementedError

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value
        self.pathChanged.emit(value)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        self.nameChanged.emit(value)
