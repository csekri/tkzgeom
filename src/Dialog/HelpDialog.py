from PyQt5 import QtCore, QtWidgets, QtGui, uic

class HelpDialog(QtWidgets.QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.ui = uic.loadUi('layouts/help.ui', self)
        self.setWindowTitle("Help")
