from PyQt5 import QtWidgets, uic

from Factory import Factory
from PointClasses.FreePoint import FreePoint
from Fill.ListWidget import fill_listWidget_with_data, set_selected_id_in_listWidget
import Constant as c


class CompleteGraphDialog(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(CompleteGraphDialog, self).__init__()
        self.ui = uic.loadUi('regularpolygon.ui', self)
        self.scene = scene
        self.sides = 3
        self.free_point = False
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)

        self.ui.sides_slider.valueChanged.connect(self.hslider_sides_func)

        self.ui.checkBox.stateChanged.connect(self.checkbox_free_point)

    def hslider_sides_func(self, value):
        self.sides = value
        self.ui.sides_spin.setValue(value)

    def checkbox_free_point(self, state):
        self.free_point = bool(state)

    def accepted(self):
        A, B = self.data
        angle = -(self.sides - 2) * 180 / self.sides
        polygon = [A, B]

        for _ in range(self.sides - 2):
            item = Factory.create_empty_item('point', c.Point.Definition.ROTATION)
            definition = {'A': A, 'B': B, 'angle': angle}
            id_ = Factory.next_id(item, definition, self.scene.project_data.items)
            item.item["id"] = id_
            item.item["definition"] = definition
            if self.free_point:
                item.recompute_canvas(self.scene.project_data.items,
                                      self.scene.project_data.window,
                                      *self.scene.init_canvas_dims)
                canvas_coords = item.get_canvas_coordinates()
                tikz_coords = FreePoint.phi_inverse(self.scene.project_data.window,
                                       *item.get_canvas_coordinates(),
                                       *self.scene.init_canvas_dims)
                item = Factory.create_empty_item('point', c.Point.Definition.FREE)
                definition = dict(zip(['x', 'y'], tikz_coords))
                item.item["id"] = id_
                item.item["definition"] = definition
                item.set_canvas_coordinates(*canvas_coords)
            self.scene.project_data.add(item)
            A = B
            B = id_
            polygon.append(id_)

        for i in range(len(polygon)):
            for j in range(i):
                item = Factory.create_empty_item('segment', None)
                definition = {'A': polygon[j], 'B': polygon[i]}
                item.item["id"] = Factory.next_id(item, definition, self.scene.project_data.items)
                item.item["definition"] = definition
                self.scene.project_data.add(item)
        self.scene.project_data.recompute_canvas(*self.scene.init_canvas_dims)

        current_row_old = self.scene.ui.listWidget.currentRow()
        fill_listWidget_with_data(self.scene.project_data, self.scene.ui.listWidget, self.scene.current_tab_idx)
        set_selected_id_in_listWidget(self.scene, current_row_old)
        self.scene.edit.add_undo_item(self.scene)

    def rejected(self):
        pass
