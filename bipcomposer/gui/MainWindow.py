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

import os.path

from PySide.QtGui import (
    QFileDialog,
    QMainWindow
)

from .generated import Ui_MainWindow
from bipcomposer.score import Score
from bipcomposer.utils.path import addext


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, position=None, size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.actionNew.triggered.connect(self.newScore)
        self.actionOpen.triggered.connect(self.openScore)
        self.actionSave.triggered.connect(self.saveScore)
        self.actionSaveAs.triggered.connect(self.saveScoreAs)

        self.actionDelete.triggered.connect(self.delete)
        self.actionSelectAll.triggered.connect(self.selectAll)

        self.tabs.tabCloseRequested.connect(self.closeScore)
        self.tabs.currentChanged.connect(self.onCurrentChanged)

        # Add a default empty score
        self.newScore()

    def setupUi(self, target):
        super().setupUi(self)

        self.setCentralWidget(self.tabs)

    def newScore(self, name=None, goto=True):
        """
        Creates a new score with the given name.
        If no name is provided, a research is
        performed to create a consitent "new n"
        name.

        :param name: Name of the new score.
        :type name: str
        :return: Newly created score.
        :rtype: CanvasScore
        :param goto: Whether to switch to the tab once openened.
        :type goto: bool
        """
        score = Score()
        if not name:
            # Find the latest "new n"
            new_n = 0
            for i in range(self.tabs.count()):
                text = self.tabs.tabText(i)
                text = text.rstrip('*') # Also count modified scores
                if text.startswith("new "):
                    n = text.split()[-1]
                    try:
                        n = int(n)
                        new_n = max(new_n, n)
                    except:
                        pass
            # Create the tab "new n+1"
            new_n += 1
            name = "new %d" % new_n
        index = self.tabs.addTab(score.canvas, name)

        if goto:
            # Go to the new tab
            self.tabs.setCurrentIndex(index)

        # Bind score signals to window slots
        score.nameChanged.connect(lambda text:
            self.tabs.setTabText(self.tabs.currentIndex(), self.score.name))
        score.changed.connect(lambda modified:
            self.actionSave.setEnabled(modified))

        # Set the score properties
        score.name = name
        # Return the newly created score
        return score

    def openScore(self, fname=None, goto=True):
        """
        Opens the given score if given, otherwise
        asks for the user to provide a file name
        and opens the score.
        
        :param fname: File to open.
        :type fname: str
        :param goto: Whether to switch to the tab once openened.
        :type goto: bool
        """
        if not fname:
            dname = os.path.expanduser('~')
            fname = QFileDialog.getOpenFileName(self,
                _("Open File"), dname, _("BipComposer Files (*.bcf)"))[0]
        if fname:
            if not os.path.exists(fname):
                raise IOError("%s is not a valid file name" % fname)
            name, ext = os.path.splitext(fname)
            if ext.lower() not in ('.bcf',):
                raise IOError("invalid file extension: %s" % ext)

            name = os.path.split(name)[1]
            score = self.newScore(name, goto=goto)
            score.load(fname)

    def saveScore(self, fname=None):
        """
        Saves the score to fname if given. Otherwise,
        saves it to the cached location if known, otherwise
        asks for the user to provide a file name and saves
        the score.

        :param fname: File where to save the score.
        :type fname: str
        """
        if fname:
            fname = addext(fname, '.bcf')
            self.score.save(fname)
        else:
            path = self.score.path
            if path:
                self.score.save(path)
            else:
                new_path = self.saveScoreAs()
                self.score.path = new_path

        # Score no more modified since the last save
        self.score.modified = False

    def saveScoreAs(self):
        """
        Asks for the user to provide a file name and
        saves the score to this file, creating it if
        it does not already exist.
        """
        path = self.score.path
        if path:
            dname = os.path.dirname(path)
        else:
            dname = os.path.expanduser('~')

        fname = QFileDialog.getSaveFileName(self,
            _("Save File"), dname, _("BipComposer Files (*.bcf)"))[0]
        if fname:
            fname = addext(fname, '.bcf')
            self.score.save(fname)
        return fname

    def closeScore(self, index):
        """
        Close the given score. Create a new score
        if there are no scores left.

        :param index: Score to close (tab index).
        :type index: int
        """
        self.tabs.removeTab(index)
        if not self.tabs.count():
            self.newScore()

    def delete(self):
        """
        Delete all the seleted notes in the current
        score.
        """
        to_remove = []
        for note in self.score.notes:
            if note.selected:
                to_remove.append(note)
        # To phases look-up in order to avoid problems
        for note in to_remove:
            self.score.removeNote(note)

    def selectAll(self):
        """
        Select all the notes in the current score.
        """
        for note in self.score.notes:
            note.selected = True

    @property
    def score(self):
        """
        Returns the CanvasScore at the current index.

        :return: Current score.
        :rtype: CanvasScore
        """
        return self.tabs.currentWidget().score

    def onCurrentChanged(self, index):
        """
        Callback called when signal currentChanged
        is emitted.

        :param index: Index of the current tab.
        :type index: int
        """
        if self.tabs.count():
            self.actionSave.setEnabled(self.score.modified)
