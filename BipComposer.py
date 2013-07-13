#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
