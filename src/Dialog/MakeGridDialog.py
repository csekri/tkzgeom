from PyQt5 import QtWidgets, uic

from AddNewItem import register_new_point, first_disengaged_name
from Constants import *
import CanvasDrawing as cd

# class for the function pop-up window
class MakeGridDialog(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(MakeGridDialog, self).__init__()
        self.ui = uic.loadUi('layouts/make_grid_dialog.ui', self)
        self.setWindowTitle("Enter grid parameters")
        self.scene = scene
        self.rows = 1
        self.cols = 1
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)

        self.ui.hslider_col.valueChanged.connect(self.hslider_col_func)
        self.ui.hslider_row.valueChanged.connect(self.hslider_row_func)


    def hslider_col_func(self, value):
        self.cols = value
        self.ui.col_label.setText(str(value))

    def hslider_row_func(self, value):
        self.rows = value
        self.ui.row_label.setText(str(value))


    def accepted(self):
        origin, right, bottom = self.data
        x, y = right, bottom
        for j in range(self.rows):
            for i in range(self.cols-1):
                if j == i == 0:
                    continue
                next_name = first_disengaged_name(self.scene.eucl, "upper")
                register_new_point(self.scene.eucl, [origin, right, x], setup=TRANSLATION)
                x = next_name

            if (j != self.rows - 1) and (j != 0):
                next_name = first_disengaged_name(self.scene.eucl, "upper")
                register_new_point(self.scene.eucl, [origin, bottom, y], setup=TRANSLATION)
                y = next_name
            x = y


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
