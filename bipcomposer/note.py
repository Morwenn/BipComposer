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

import os
import xml.etree.ElementTree as ET

import sfml as sf


class NoteType(dict):
    """
    A note type. I determines how a note
    looks like and behaves.
    """
    _files = {}

    def __init__(self, name, load_textures=True):
        """
        Searches for all the files whose name
        corresponds to the the given name, loads
        them and apply transparency to the MAGENTA
        pixels of the image.
        Files must be of in the format 'name-length.png'.

        :param name: Name of the note type.
        :type name: str
        """
        dname = os.path.join('bipcomposer', 'sprites', 'notes')
        for fname in os.listdir(dname):
            root, ext = os.path.splitext(fname)
            type, length = root.split('-')
            if type == name:
                length = int(length)
                tmp = os.path.join(dname, fname)
                self._files[length] = tmp
                if load_textures:
                    self.load_textures()

    def load_textures(self):
        """
        Load the textures from the type files.
        """
        for key, value in self._files.items():
            img = sf.Image.from_file(value)
            img.create_mask_from_color(sf.Color.MAGENTA)
            tex = sf.Texture.from_image(img)
            self[key] = tex


types = {}
for _type in (
        'basic',
        'gb',
        'ramp',
        'random',
        'wave'):
    types[_type] = NoteType(_type)


class Note:
    """
    Simple note.
    """
    def __init__(self, x, y, length, type='basic'):
        self.x = x
        self.y = y
        self.length = length
        self.type = type

    @property
    def sprite(self):
        tex = types[self.type][self.length]
        spr = sf.Sprite(tex)
        spr.position = (self.x, self.y)
        return spr

    def xml(self):
        """
        Creates an xml element an returns it.

        :return: New xml element.
        :rtype: xml.etree.ElementTree.Element
        """
        attrib = {
            'x' : self.x,
            'y' : self.y,
            'length' : self.length,
            'type' : self.type
        }
        attrib = { key : str(val) for key, val in attrib.items() }
        return ET.Element('note', attrib=attrib)

    @staticmethod
    def fromXml(elem):
        """
        Creates a new note from a corrresponding
        xml element.

        :param elem: xml element discribing the note.
        :type elem: xml.etree.ElementTree.Element
        """
        from ast import literal_eval as lev
        x = lev(elem.attrib['x'])
        y = lev(elem.attrib['y'])
        length = lev(elem.attrib['length'])
        type = elem.attrib['type']
        return Note(x, y, length, type)


if __name__ == '__main__':
    a = Note(2, 2, 1, 'basic')
    b = Note(1, 1, 2, 'basic')
    c = Note(2, 2, 1, 'wave')
    d = Note(5, 8, 3, 'basic')
    e = Note(4, 2, 9, 'random')
    for note in (a, b, c, d, e):
        tmp = note.xml()
        ET.dump(tmp)
        note = Note.fromXml(tmp)




