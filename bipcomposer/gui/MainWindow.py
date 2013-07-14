#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

from PySide.QtGui import (
    QFileDialog,
    QMainWindow
)

from .CanvasScore import CanvasScore
from .generated import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, position=None, size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.actionNew.triggered.connect(self.newScore)
        self.actionOpen.triggered.connect(self.openScore)
        self.actionSave.triggered.connect(self.saveScore)
        self.actionSaveAs.triggered.connect(self.saveScoreAs)

        # Add a default empty score
        self.newScore()

    def setupUi(self, target):
        super().setupUi(self)

        self.setCentralWidget(self.tabs)

    def newScore(self, name=None):
        """
        Creates a new score with the given name.
        If no name is provided, a research is
        performed to create a consitent "new n"
        name.

        :param name: Name of the new score.
        :type name: str
        :return: Newly created score.
        :rtype: CanvasScore
        """
        score = CanvasScore(self.tabs)
        if not name:
            # Find the latest "new n"
            new_n = 0
            for i in range(self.tabs.count()):
                text = self.tabs.tabText(i)
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
        self.tabs.addTab(score, name)

        score.nameChanged.connect(lambda text:
            self.tabs.setTabText(self.tabs.indexOf(score), name))

        # Set the score properties
        score.name = name
        # Return the newly created score
        return score

    def openScore(self, fname=None):
        """
        Opens the given score if given, otherwise
        asks for the user to provide a file name
        and opens the score.
        
        :param fname: File to open.
        :type fname: str
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
            score = self.newScore(name)
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
            name, ext = os.path.splitext(fname)
            self.score().save(name + '.bcf')
        else:
            path = self.score().path
            if path:
                self.score().save(path)
            else:
                self.saveScoreAs()

    def saveScoreAs(self):
        """
        Asks for the user to provide a file name and
        saves the score to this file, creating it if
        it does not already exist.
        """
        path = self.score().path
        if path:
            dname = os.path.dirname(path)
        else:
            dname = os.path.expanduser('~')

        fname = QFileDialog.getSaveFileName(self,
            _("Save File"), dname, _("BipComposer Files (*.bcf)"))[0]
        if fname:
            name, ext = os.path.splitext(fname)
            self.score().save(name + '.bcf')

    def score(self):
        """
        Returns the CanvasScore at the current index.

        :return: Current score.
        :rtype: CanvasScore
        """
        return self.tabs.currentWidget()
