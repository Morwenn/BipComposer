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

import ctypes
import platform

import sfml as sf
from PySide.QtCore import (
    Qt,
    QEvent,
    Signal
)

from bipcomposer.utils.qsfml import QSFMLCanvas
from bipcomposer.background import Background
from bipcomposer.note import Note
from bipcomposer.reader import Reader


class CanvasScore(QSFMLCanvas):
    """
    A CanvasScore is a surface object where are drawn all
    the notes of a score.
    score.
    """
    mouse_pressed = Signal(QEvent)
    mouse_released = Signal(QEvent)
    mouse_double_clicked = Signal(QEvent)
    mouse_moved = Signal(QEvent)
    resized = Signal(tuple)
    refreshed = Signal()
    view_moved = Signal(sf.Vector2)

    def __init__(self, score, parent=None, frameTime=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.score = score
        self.reader = Reader(self)
        self.background = Background(self)

    def onUpdate(self):
        """
        This procedure describes what happens on
        each frame. Basically, it draws all the
        elements of the canvas.
        """
        if self.initialized:
            # The order of drawing is important:
            # the last drawn object will be the
            # last drawn on the screen
            self.draw(self.background.sprite)
            for note in self.score.notes:
                self.draw(note.sprite)
            self.reader.draw()

    def mousePressEvent(self, event):
        """
        When the mouse is pressed, several things can
        occur: create a note, delete a note, open a
        contextual menu, select note, etc...
        """
        x, y = event.x(), event.y()
        x, y = self.window.map_pixel_to_coords((x, y), self.view)

        # Check whether a note is selected
        targets = self.objects_at(x, y)

        if event.button() == Qt.LeftButton:
            if targets:
                pass
            else:
                self.create_note(x, y)

        elif event.button() == Qt.RightButton:
            for elem in targets:
                if isinstance(elem, Note):
                    self.score.remove_note(elem)

        self.mouse_pressed.emit(event)

    def mouseReleaseEvent(self, event):
        self.mouse_released.emit(event)

    def mouseDoubleClickEvent(self, event):
        self.mouse_double_clicked.emit(event)

    def mouseMoveEvent(self, event):
        """
        Does basically the same thing as mousePressEvent,
        since always clicking is long and boring.
        """
        x, y = event.x(), event.y()
        x, y = self.window.map_pixel_to_coords((x, y), self.view)

        # Check whether a note is selected
        targets = self.objects_at(x, y)

        if event.buttons() & Qt.LeftButton:
            if targets:
                pass
            else:
                self.create_note(x, y)

        elif event.buttons() & Qt.RightButton:
            for elem in targets:
                if isinstance(elem, Note):
                    self.score.remove_note(elem)
        
        self.mouse_moved.emit(event)

    def resizeEvent(self, event):
        """
        When the window is resized, the room is resized
        accordingly, and the different backgrounds have
        to be expanded.
        """
        if self.initialized:
            width, height = event.size().width(), event.size().height()
            x, y = self.window.map_pixel_to_coords((0, 0), self.view)

            view = sf.View(sf.Rectangle((x, y), (width, height)))
            self.view = view

            self.resized.emit((width, height))

    def refresh(self):
        """
        Emits a signal that the underlying widgets
        will get to refresh themselves.
        """
        if self.initialized:
            self.refreshed.emit()

    def move_view(self, x, y):
        """
        Move the view. This wrapper emits a view_moved
        signal which contains the position of the view.
        """
        self.view.move(x, y)
        self.view_moved.emit(self.view_origin)

    def editable(self, x, y):
        """
        Returns whether the given position editable
        or not. Which means the reader and keyboard
        are absent, and the position is in the score.
        """
        _x, _y = self.view_origin

        min_x = _x
        min_y = _y + 12
        max_x = _x + self.view.size.x
        max_y = _y + self.view.size.y - 13

        return (min_x <= x <= max_x
            and min_y <= y <= max_y)

    def objects_at(self, x, y):
        """
        Returns all the objects at a given position.

        :return: Objects at the given position.
        :rtype: list(object)
        """
        res = []
        # Check the notes
        for note in self.score.notes:
            rec = note.sprite.global_bounds
            if rec.contains((x, y)):
                res.append(note)
        # Check the reader parts
        for elem in (self.reader.sprites['bg-up'],
                     self.reader.sprites['bg-down']):
            rec = elem.global_bounds
            if rec.contains((x, y)):
                res.append(self.reader)
        return res

    def create_note(self, x, y, length=None, type=None):
        """
        Creates a note at the given position.
        If length and type are note specified,
        the global ones are taken.
        """
        # Default values and stuff
        x = int(x / 12) * 12
        y = int(y / 12) * 12

        if not length:
            length = 1
        if not type:
            type = 'basic'

        if self.editable(x, y):
            note = Note(x, y, length, type)
            self.score.add_note(note)

    @property
    def view_origin(self):
        """
        Returns the SFML coordinates of the origin of
        view. Be careful, this may not work if a zoom
        or a rotation have been applied.

        :return: SFML coordinates of the origin of the view.
        :rtype: sfml.system.Vector2
        """
        return self.window.map_pixel_to_coords((0, 0), self.view)

    @property
    def view_rectangle(self):
        """
        Returns a rectangle corresponding to the view
        origin and the view size.

        :return: View origin and view size.
        :rtype: sfml.graphics.Rectangle
        """
        return sf.Rectangle(self.view_origin, self.view.size)


