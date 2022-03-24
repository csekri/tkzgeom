from PyQt5 import QtWidgets, uic

from Factory import Factory
from Dialogs.DialogMacros import turn_into_free_point, free_point_checkbox
from Fill.ListWidget import fill_listWidget_with_data, set_selected_id_in_listWidget
import Constant as c


class MakeGridDialog(QtWidgets.QDialog):
    def __init__(self, scene, data):
        """Construct MakeGridDialog."""
        super(MakeGridDialog, self).__init__()
        self.ui = uic.loadUi('makegrid.ui', self)
        self.scene = scene
        self.rows = 1
        self.cols = 1
        self.free_point = False
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)

        self.ui.cols_slider.valueChanged.connect(self.hslider_col_func)
        self.ui.rows_slider.valueChanged.connect(self.hslider_row_func)

        self.ui.checkBox.stateChanged.connect(lambda x: free_point_checkbox(self, x))

    def hslider_col_func(self, value):
        """Be slider callback function to set columns."""
        self.cols = value
        self.ui.cols_spin.setValue(value)

    def hslider_row_func(self, value):
        """Be slider callback function to set rows."""
        self.rows = value
        self.ui.rows_spin.setValue(value)

    def accepted(self):
        """Create new grid with settings."""
        origin, right, bottom = self.data
        top_accumulator = [origin, right]
        left_accumulator = [origin, bottom]
        right_accumulator = []
        bottom_accumulator = []
        x, y = right, bottom
        for j in range(self.rows):
            for i in range(self.cols-1):
                if j == i == 0:
                    continue
                item = Factory.create_empty_item('point', c.Point.Definition.TRANSLATION)
                definition = {'A': origin, 'B': right, 'P': x}
                id_ = Factory.next_id(item, definition, self.scene.project_data.items)
                item.item["id"] = id_
                item.item["definition"] = definition
                if self.free_point:
                    item = turn_into_free_point(item, self.scene)
                self.scene.project_data.add(item)
                x = item.item["id"]
                if j == 0:
                    top_accumulator.append(x)
                if j == self.rows-1:
                    bottom_accumulator.append(x)

            right_accumulator.append(x)

            if (j != self.rows - 1) and (j != 0):
                item = Factory.create_empty_item('point', c.Point.Definition.TRANSLATION)
                definition = {'A': origin, 'B': bottom, 'P': y}
                id_ = Factory.next_id(item, definition, self.scene.project_data.items)
                item.item["id"] = id_
                item.item["definition"] = definition
                if self.free_point:
                    item = turn_into_free_point(item, self.scene)
                self.scene.project_data.add(item)
                y = item.item["id"]
                if j == self.rows - 2:
                    bottom_accumulator.append(y)
                left_accumulator.append(y)
            x = y

        linestring = []
        if self.rows == 1:
            linestring = top_accumulator
        elif self.cols == 1:
            linestring = left_accumulator
        else:
            for i in range(len(top_accumulator)):
                linestring.append(top_accumulator[i])
                linestring.append(bottom_accumulator[i])
                linestring.append(top_accumulator[i])
            for i in range(len(left_accumulator)):
                linestring.append(left_accumulator[i])
                linestring.append(right_accumulator[i])
                linestring.append(left_accumulator[i])
        item = Factory.create_empty_item('linestring', None)
        definition = linestring
        item.item["id"] = Factory.next_id(item, definition, self.scene.project_data.items)
        item.item["definition"] = definition
        self.scene.project_data.add(item)

        self.scene.project_data.recompute_canvas(*self.scene.init_canvas_dims)
        current_row_old = self.scene.ui.listWidget.currentRow()
        fill_listWidget_with_data(self.scene.project_data, self.scene.ui.listWidget, self.scene.current_tab_idx)
        set_selected_id_in_listWidget(self.scene, current_row_old)
        self.scene.edit.add_undo_item(self.scene)

    def rejected(self):
        """Add no new grid graph."""
        pass
