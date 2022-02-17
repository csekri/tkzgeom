#!/usr/bin/env python
"""
contains the main method
"""

import sys
from PyQt5 import QtWidgets
from EuclMainWindow import EuclMainWindow

if __name__ == '__main__':
    # initialises the GUI interface and makes the main window pop up
    app = QtWidgets.QApplication(sys.argv)
    eucl_main_window = EuclMainWindow()
    eucl_main_window.setWindowTitle("TkzGeom")
    # eucl_main_window.installEventFilter(eucl_main_window)
    eucl_main_window.show()
    sys.exit(app.exec_())
