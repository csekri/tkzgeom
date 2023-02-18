#!/usr/bin/env python
"""
contains the main method
"""

import sys
from PyQt5 import QtWidgets
from EuclMainWindow import EuclMainWindow
import platform
import subprocess
from Dialogs.NoCompilerDialog import NoCompilerDialog

COMMAND_NAME = 'pdflatex'


def is_compiler_installed():
    cmd = "where" if platform.system() == "Windows" else "which"
    return not bool(subprocess.call([cmd, COMMAND_NAME]))


if __name__ == '__main__':
    # initialise the GUI interface and makes the main window pop up

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    if not is_compiler_installed():
        dialog = NoCompilerDialog()
        dialog.exec_()
        if not dialog.bool:
            sys.exit()

    eucl_main_window = EuclMainWindow()
    eucl_main_window.setWindowTitle("TkzGeom")
    # eucl_main_window.installEventFilter(eucl_main_window)
    eucl_main_window.show()
    sys.exit(app.exec_())
