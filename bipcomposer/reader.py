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

import sfml as sf

import bipcomposer.textures as tex
from bipcomposer.entity import Entity


class EndIndicator(Entity):
    """
    Indicator pointing to the last part of the
    score to be played when playing.
    """
    def __init__(self):
        self.sprite = sf.Sprite(tex.end_indicator)


class Head:
    """
    Reader head. It contains a head at the
    top of the screen and one at the bottom.

    Changing the x coodinate changes both the
    reader's top and bottom heads x coordinate.
    """
    def __init__(self):
        self.top = Entity(tex.reader_head_top)
        self.bottom = Entity(tex.reader_head_bottom)

        #Line between the top and the bottom
        self.line = sf.VertexArray(sf.PrimitiveType.LINES, 2)
        self.line[0].position = (7, 9)
        self.line[0].color = sf.Color.RED
        self.line[1].color = sf.Color.YELLOW

    def draw(self, target):
        """
        Draw the heads and the line between them
        to the target.
        """
        target.draw(self.top.sprite)
        target.draw(self.bottom.sprite)
        target.draw(self.line)

    @property
    def x(self):
        return self.top.x
    @x.setter
    def x(self, value):
        self.top.x = value
        self.bottom.x = value
        self.line[0].position = (value+7, 9)
        self.line[1].position = (value+7, self.bottom.y+3)


class Reader:
    """
    Handles the reader head, and all the necessary
    drawing.
    """
    def __init__(self, score):
        self.score = score

        # Reader elements
        self.head = Head()
        self.indicator = None

        # Load sprites
        self.sprites = {
            'bg-up' : sf.Sprite(tex.reader_background),
            'bg-down' : sf.Sprite(tex.reader_background),
        }
        # Repeat background
        self.sprites['bg-up'].texture.repeated = True
        self.sprites['bg-down'].texture.repeated = True
        # Set the sprite's positions
        self.head.top.y = 1

    def draw(self):
        """
        Draw the reader heads, the reader line
        and the reader background.
        """
        target = self.score.window
        target.draw(self.sprites['bg-up'])
        target.draw(self.sprites['bg-down'])
        self.head.draw(target)
        if self.indicator:
            target.draw(self.indicator.sprite)

    def set_size(self, size):
        """
        Make sure the reader's size matches the
        room's size.
        """
        width, height = size[0], size[1]

        # Set background rectangle
        self.sprites['bg-up'].texture_rectangle = (0, 0, width, 12)
        self.sprites['bg-down'].texture_rectangle = (0, 0, width, 12)

        # Set the sprite's positions
        self.sprites['bg-down'].position = (0, height-12)
        self.head.bottom.y = height - 12
        self.head.line[1].position = (self.head.x+7, self.head.bottom.y+3)
