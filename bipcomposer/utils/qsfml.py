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
from PySide.QtCore import Qt, QTimer
from PySide.QtGui import QWidget


class QSFMLCanvas(QWidget):
    """
    Canvas class using SFML instead of Qt to
    draw on the screen.
    """
    def __init__(self, parent=None, frameTime=30, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initialized = False

        self.window = sf.HandledWindow()
        # Have the canvas act like its underlying RenderTarget
        self.__dict__['draw'] = self.window.draw
        self.__dict__['clear'] = self.window.clear
        self.__dict__['display'] = self.window.display

        # Setup some states to allow direct rendering into the widget
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_StaticContents)

        # Set strong focus to enable keyboard events to be received
        self.setFocusPolicy(Qt.StrongFocus)

        # Setup the timer
        self.timer = QTimer()
        self.timer.setInterval(frameTime)

    def onInit(self):
        pass

    def onUpdate(self):
        pass

    def sizeHint(self):
        return self.size()

    def paintEngine(self):
        pass

    def showEvent(self, event):
        if not self.initialized:
            # Under X11, we need to flush the commands sent to the server
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

        # Let the derived class do its specific stuff
        self.onInit()

        # Setup the timer to trigger a refresh at specified framerate
        self.timer.timeout.connect(self.repaint)
        self.timer.start()

        self.initialized = True

    def paintEvent(self, event):
        # Let the derived class do its specific stuff
        self.onUpdate()
        # Display on screen
        self.display()

    @property
    def view(self):
        return self.window.view
    @view.setter
    def view(self, value):
        self.window.view = value


