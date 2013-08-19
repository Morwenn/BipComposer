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

import bipcomposer.textures.background as tex
from bipcomposer.entity import Entity


# The background is dependant of
# the rythmic signature
textures = {
    '2/4' : None,
    '3/4' : None,
    '4/4' : tex.b4_4,
    '5/4' : None,
    '6/4' : None
}

# All of the background textures
# can be repeated
for _tex in textures.values():
    if _tex:
        _tex.repeated = True


class Background(Entity):
    """
    Background static class.
    """
    def __init__(self, score, rythm='4/4'):
        self.score = score
        self.sprite = sf.Sprite(textures[rythm])
        self.sprite.position = (0, 12)

        # Bind signals and slots
        self.score.resized.connect(self.resize)
        self.score.refreshed.connect(self.refresh)

    def resize(self, size):
        """
        Set the size (width, height) to the room
        background.

        :param size: New size.
        :type size: sfml.system.Vector2
        """
        if self.sprite:
            width, height = size
            self.sprite.texture_rectangle = (0, 0, width, height-24)

    def refresh(self):
        """
        Resize the background to the size of the
        current score.
        """
        self.resize(self.score.view.size)


