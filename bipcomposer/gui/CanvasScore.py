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
    QPoint,
    QSize,
    QTimer,
    Signal
)
from PySide.QtGui import (
    QWidget
)

from bipcomposer.background import Background
from bipcomposer.note import Note


class CanvasScore(QWidget):
    """
    A CanvasScore is a surface object where are drawn all
    the notes of a score.
    score.
    """
    mousePressed = Signal(QEvent)
    mouseReleased = Signal(QEvent)
    mouseDoubleClicked = Signal(QEvent)
    mouseMoved = Signal(QEvent)

    def __init__(self, score, parent=None, position=None, size=None,
                 frameTime=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initialized = False
        self.score = score

        if not position:
            position = QPoint(0, 0)
        if not size:
            size = QSize(800, 600)

        w = size.width()
        h = size.height()

        self.window = sf.HandledWindow()
        self.window.view.size = (w, h)
        self.__dict__['draw'] = self.window.draw
        self.__dict__['clear'] = self.window.clear
        self.__dict__['view'] = self.window.view
        self.__dict__['display'] = self.window.display

        # setup some states to allow direct rendering into the widget
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # set strong focus to enable keyboard events to be received
        self.setFocusPolicy(Qt.StrongFocus)

        # setup the widget geometry
        self.move(position)
        self.resize(size)

        # setup the timer
        self.timer = QTimer()
        self.timer.setInterval(frameTime)

        Background.load()

    def onInit(self):
        pass

    def onUpdate(self):
        self.clear(sf.Color.BLACK)
        if Background.sprite:
            self.window.draw(Background.sprite)
        try:
            for note in self.score.notes:
                self.window.draw(note.sprite)
        except:
            # Sometimes, score's __init__ seems to
            # occur too late. This fix allows it to
            # be late.
            pass

    def sizeHint(self):
        return self.size()

    def paintEngine(self):
        # let the derived class do its specific stuff
        self.onUpdate()
        # display on screen
        self.display()

    def showEvent(self, event):
        if not self.initialized:
            # under X11, we need to flush the commands sent to the server
            # to ensure that SFML will get an updated view of the windows
            # create the SFML window with the widget handle
            if platform.system() == 'Linux':
            
                x11 = ctypes.cdll.LoadLibrary("libX11.so")

                display = sip.unwrapinstance(QX11Info.display())
                x11.XFlush(display)

        ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
        hwnd = ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)
        self.window.create(hwnd)

        # let the derived class do its specific stuff
        self.onInit()

        # setup the timer to trigger a refresh at specified framerate
        self.timer.timeout.connect(self.repaint)
        self.timer.start()

        self.initialized = True

    def paintEvent(self, event):
        pass

    def mousePressEvent(self, event):
        """
        When the mouse is pressed, several things can
        occur: create a note, delete a note, open a
        contextual menu, select note, etc...
        """
        x, y = event.x(), event.y()
        # Check whether a note is selected
        targets = self.objectsAt(x, y)

        if event.button() == Qt.LeftButton:
            if targets:
                pass
            else:
                x = int(x / 12) * 12
                y = int(y / 12) * 12
                note = Note(x, y, 1)
                self.score.addNote(note)

        elif event.button() == Qt.RightButton:
            for note in targets:
                self.score.removeNote(note)

        self.mousePressed.emit(event)

    def mouseReleaseEvent(self, event):
        self.mouseReleased.emit(event)

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClicked.emit(event)

    def mouseMoveEvent(self, event):
        self.mouseMoved.emit(event)

    def resizeEvent(self, event):
        # Resize the room so that it fits the view
        width, height = event.size().width(), event.size().height()
        view = sf.View(sf.Rectangle((0, 0), (width, height)))
        self.window.view = view
        # Extend the background box
        Background.set_size((width, height))

    def objectsAt(self, x, y):
        """
        Returns all the objects at a given position.

        :return: Objects at the given position.
        :rtype: list(object)
        """
        res = []
        for note in self.score.notes:
            rec = note.sprite.global_bounds
            if rec.contains((x, y)):
                res.append(note)
        return res



