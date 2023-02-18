from PyQt5 import QtWidgets, uic


class NoCompilerDialog(QtWidgets.QDialog):
    def __init__(self):
        """Construct NoCompilerDialog."""
        super(NoCompilerDialog, self).__init__()
        self.bool = False
        self.ui = uic.loadUi('layouts/nocompiler.ui', self)
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)

    def accepted(self):
        self.bool = True

    def rejected(self):
        self.bool = False

