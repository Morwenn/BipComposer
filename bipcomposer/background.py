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

import bipcomposer.textures.background as texture


class Background:
    """
    Background static class.
    """
    sprite = None
    texture = None

    @classmethod
    def load(cls):
        cls.texture = texture.b4_4
        cls.texture.repeated = True
        # Parametrize the sprite
        cls.sprite = sf.Sprite(cls.texture)
        cls.sprite.position = (0, 12)

    @classmethod
    def set_size(cls, size):
        """
        Set the size (width, height) to the room
        background.
        """
        if cls.sprite:
            width, height = size[0], size[1]
            cls.sprite.texture_rectangle = (0, 0, width, height-24)




