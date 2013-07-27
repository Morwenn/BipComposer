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

import ast
import os.path
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
    changed = Signal(bool)

    length = 64
    tempo = 120

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = CanvasScore(self)
        self.notes = []
        self.modified = False

    def addNote(self, note):
        """
        Add a new note to the score.

        :param note: Note to add to the score.
        :type note: bipcomposer.note.Note
        """
        self.notes.append(note)
        self.modified = True

    def removeNote(self, note):
        """
        Remove the given note from the score.

        :param note: Note to remove from the score.
        :type note: bipcomposer.note.Note
        """
        self.notes.remove(note)
        self.modified = True

    def load(self, fname=None):
        """
        Loads the given .bcf file if given.
        Otherwise, loads the cached one.

        :param fname: .bcf file to load.
        :type fname: str
        """
        if fname:
            self.path = fname

        with open(fname, 'r') as f:
            root = ET.fromstring(f.read())
            self.path = fname
            length = root.attrib['length']
            tempo = root.attrib['tempo']
            self.length = ast.literal_eval(length)
            self.tempo = ast.literal_eval(tempo)
            for elem in root:
                note = Note.fromXml(elem)
                self.notes.append(note)

    def save(self, fname=None):
        """
        Saves the score to the given .bcf file.

        :param fname: .bcf file where to save the score.
        :type fname: str
        """
        root = self.xml()
        with open(fname, 'w') as f:
            f.write(ET.tostring(root, encoding="unicode"))

    def updateName(self):
        """
        Creates a new name from the score's path.
        Add '*' at the end if the score has been
        modified.
        """
        name = self.name
        if self.path:
            name, ext = os.path.splitext(self.path)
            name = os.path.basename(name)

        # Handles the modified property
        if self.modified:
            if not name.endswith('*'):
                name += '*'
        else:
            if name.endswith('*'):
                name = name[:-1]
        self.name = name

    def xml(self):
        """
        Creates an xml element an returns it.

        :return: New xml element.
        :rtype: xml.etree.ElementTree.Element
        """
        attrib = {
            'length' : self.length,
            'tempo' : self.tempo
        }
        attrib = { key : str(val) for key, val in attrib.items() }
        score = ET.Element('score', attrib=attrib)
        for note in self.notes:
            score.append(note.xml())
        return score

    @staticmethod
    def fromXml(elem):
        """
        Creates a new score from a corrresponding
        xml element.

        :param elem: xml element discribing the score.
        :type elem: xml.etree.ElementTree.Element
        """
        lenght = elem.attrib['length']
        tempo = elem.attrib['tempo']
        score = Score()
        score.length = ast.literal_eval(length)
        score.tempo = ast.literal_eval(tempo)
        for subelem in elem:
            note = Note.fromXml(subelem)
            score.notes.append(note)
        return score

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value
        self.updateName()
        self.pathChanged.emit(value)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        self.nameChanged.emit(value)

    @property
    def modified(self):
        return self._modified
    @modified.setter
    def modified(self, value):
        self._modified = value
        self.updateName()
        self.changed.emit(value)
