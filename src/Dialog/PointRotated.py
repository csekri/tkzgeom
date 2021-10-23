from PyQt5 import QtWidgets, uic

from AddNewItem import register_new_point
from Constants import *
import CanvasDrawing as cd

# class for the function pop-up window
class PointRotated(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(PointRotated, self).__init__()
        self.ui = uic.loadUi('layouts/point_rotate_dialog.ui', self)
        self.setWindowTitle("Enter angle")
        self.scene = scene
        self.angle = ""
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)
        self.ui.lineEdit.editingFinished.connect(self.le_editing_finished)

    def le_editing_finished(self):
        self.angle = self.ui.lineEdit.text()

    def accepted(self):
        register_new_point(self.scene.eucl, self.data + [self.angle], setup=ROTATION)
        #self.scene.add_new_undo_item()
        #self.scene.compile_tkz_and_render()
        self.scene.compute_mapped_points()
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.scene.selected_objects.clear()

        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def rejected(self):
        pass

    def le_function_editing_finished(self):
        self.function = self.ui.textEdit.toPlainText()
    def le_start_editing_finished(self):
        self.start = self.ui.lineEdit.text()
    def le_end_editing_finished(self):
        self.end = self.ui.lineEdit_2.text()
