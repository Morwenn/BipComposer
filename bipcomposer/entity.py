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


class Entity:
    """
    Entity that can have a sprite and has
    x and y properties associated to this
    sprite.
    """
    sprite = None
    _x, _y = 0, 0
    to_draw = True

    def __init__(self, texture=None):
        """
        Create a new Entity from a texture or
        from nothing.

        :param texture: Optional texture to build the sprite.
        :type texture: sfml.graphics.Texture
        """
        if texture:
            self.sprite = sf.Sprite(texture)

    def draw(self, target):
        """
        Draw the entity's sprite to the target.
        The variable to_draw can be toggled to
        draw or not the entity.
        """
        if self.sprite and to_draw:
            target.draw(self.sprite)

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        if self.sprite:
            self.sprite.position = (value, self._y)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        if self.sprite:
            self.sprite.position = (self._x, value)
