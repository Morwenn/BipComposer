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


class Reader:
    """
    Handles the reader head, and all the necessary
    drawing.
    """
    def __init__(self, score):
        self.score = score
        self.indicator = None

        # Load sprites
        self.sprites = {
            'head-up' : sf.Sprite(tex.reader_head_up),
            'head-down' : sf.Sprite(tex.reader_head_down),
            'bg-up' : sf.Sprite(tex.reader_background),
            'bg-down' : sf.Sprite(tex.reader_background),
        }

        # Repeat background
        self.sprites['bg-up'].texture.repeated = True
        self.sprites['bg-down'].texture.repeated = True

        # Set the sprite's positions
        self.sprites['head-down'].position = (0, 1)

    def draw(self):
        """
        Draw the reader heads, the reader line
        and the reader background.
        """
        target = self.score.window
        target.draw(self.sprites['bg-up'])
        target.draw(self.sprites['bg-down'])
        target.draw(self.sprites['head-up'])
        target.draw(self.sprites['head-down'])
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
        _x = self.sprites['head-up'].position.x
        self.sprites['head-up'].position = (_x, height-12)
