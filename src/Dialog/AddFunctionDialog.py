from PyQt5 import QtWidgets, uic

from AddNewItem import register_new_function
from Constants import *
import CanvasDrawing as cd

# class for the function pop-up window
class AddFunctionDialog(QtWidgets.QDialog):
    def __init__(self, scene):
        super(AddFunctionDialog, self).__init__()
        self.ui = uic.loadUi('layouts/function_dialog.ui', self)
        self.setWindowTitle("Add function")
        self.scene = scene
        self.function_type = YFX_FUNCTION
        self.function = ''
        self.start = ''
        self.end = ''
        self.ui.radioButton.clicked.connect(self.rad_yfx)
        self.ui.radioButton_2.clicked.connect(self.rad_polar)
        self.ui.radioButton_3.clicked.connect(self.rad_parametric)
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)
        self.ui.textEdit.textChanged.connect(self.le_function_editing_finished)
        self.ui.lineEdit.editingFinished.connect(self.le_start_editing_finished)
        self.ui.lineEdit_2.editingFinished.connect(self.le_end_editing_finished)

    def rad_yfx(self):
        self.function_type = YFX_FUNCTION
    def rad_polar(self):
        self.function_type = POLAR_FUNCTION
    def rad_parametric(self):
        self.function_type = PARAMETRIC_FUNCTION
    def accepted(self):
        register_new_function(self.scene.eucl, [self.function, self.start, self.end], setup=self.function_type)
        self.scene.add_new_undo_item()
        self.scene.compile_tkz_and_render()
    def rejected(self):
        pass

    def le_function_editing_finished(self):
        self.function = self.ui.textEdit.toPlainText()
    def le_start_editing_finished(self):
        self.start = self.ui.lineEdit.text()
    def le_end_editing_finished(self):
        self.end = self.ui.lineEdit_2.text()
