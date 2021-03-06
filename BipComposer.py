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

import sys

from PySide.QtGui import (
    QApplication
)

# Install _() in the project
import bipcomposer.locale
from bipcomposer.gui.MainWindow import MainWindow


def main():
    """
    Main function to run BipComposer.
    """
    app = QApplication(sys.argv)
    main_w = MainWindow()

    main_w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
