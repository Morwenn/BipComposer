# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bipcomposer\gui\generated\MainWindow.ui'
#
# Created: Sat Jul 27 20:31:32 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/BipComposerIcone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setObjectName("tabs")
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbarFile = QtGui.QToolBar(MainWindow)
        self.toolbarFile.setIconSize(QtCore.QSize(17, 14))
        self.toolbarFile.setObjectName("toolbarFile")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbarFile)
        self.toolbarEdit = QtGui.QToolBar(MainWindow)
        self.toolbarEdit.setIconSize(QtCore.QSize(17, 14))
        self.toolbarEdit.setObjectName("toolbarEdit")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbarEdit)
        self.actionNew = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon1)
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/save-as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAs.setIcon(icon4)
        self.actionSaveAs.setShortcut("Ctrl+Shift+S")
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionUndo = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon5)
        self.actionUndo.setShortcut("Ctrl+Z")
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon6)
        self.actionRedo.setShortcut("Ctrl+Shift+Z, Ctrl+Y")
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setShortcut("Ctrl+X")
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setShortcut("Ctrl+V")
        self.actionPaste.setObjectName("actionPaste")
        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setShortcut("Del")
        self.actionDelete.setObjectName("actionDelete")
        self.actionSelectAll = QtGui.QAction(MainWindow)
        self.actionSelectAll.setShortcut("Ctrl+A")
        self.actionSelectAll.setObjectName("actionSelectAll")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSelectAll)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.toolbarFile.addAction(self.actionNew)
        self.toolbarFile.addAction(self.actionOpen)
        self.toolbarFile.addAction(self.actionSave)
        self.toolbarFile.addAction(self.actionSaveAs)
        self.toolbarEdit.addAction(self.actionUndo)
        self.toolbarEdit.addAction(self.actionRedo)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_('BipComposer'))
        self.menuFile.setTitle(_('&File'))
        self.menuEdit.setTitle(_('&Edit'))
        self.toolbarFile.setWindowTitle(_('toolBar'))
        self.toolbarEdit.setWindowTitle(_('toolBar_2'))
        self.actionNew.setText(_('&New'))
        self.actionOpen.setText(_('&Open...'))
        self.actionSave.setText(_('&Save'))
        self.actionSaveAs.setText(_('Save &as...'))
        self.actionUndo.setText(_('&Undo'))
        self.actionRedo.setText(_('&Redo'))
        self.actionCut.setText(_('&Cut'))
        self.actionCopy.setText(_('C&opy'))
        self.actionPaste.setText(_('&Paste'))
        self.actionDelete.setText(_('&Delete'))
        self.actionSelectAll.setText(_('&Select all'))

import bipcomposer.icons
