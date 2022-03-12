from PyQt5 import QtCore, QtWidgets, QtGui, uic
import json
from collections import namedtuple
from copy import deepcopy
import os
from PIL import Image

import Resources
from Save import EditManagement
from Items import Items
from GraphicsScene import GraphicsScene
import ConnectSignal.SelectModeRadioAndCombo as connect_mode
from KeyBank import KeyState
from HighlightItem import item_in_focus
import Constant as c
from ConnectSignal.Lambda import (
    tabWidget_func,
    listWidget_text_changed_func,
    listWidget_double_func,
    listWidget_current_row_changed_func
)
from SyntaxHighlight import syntax_highlight
import CanvasRendering as cr
from Compile import compile_latex
from ConnectSignal.ConnectPoint import connect_point
from ConnectSignal.ConnectColour import connect_colour
from ConnectSignal.ConnectSegment import connect_segment
from ConnectSignal.ConnectCircle import connect_circle
from ConnectSignal.ConnectPolygon import connect_polygon
from ConnectSignal.ConnectLinestring import connect_linestring
from ConnectSignal.ConnectCode import connect_code
from Fill.ListWidget import fill_listWidget_with_data, set_selected_id_in_listWidget
from Fill.FillAll import fill_all_fields


class EuclMainWindow(QtWidgets.QMainWindow):
    """
    class defining the main window inheriting QtWidgets.QMainWindow
    """
    def __init__(self):
        """
        SUMMARY
            contructor for graphicsScene

        PARAMETERS
            nothing

        RETURNS
            None
        """
        super(EuclMainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon("../../icon/ico.png"))
        self.ui = uic.loadUi('main.ui', self)
        self.scene = GraphicsScene(self.ui, self.setWindowTitle)
        self.ui.graphicsView.setScene(self.scene)
        self.show() # computes the widget dimensions
        self.resize(1200, 800) # NEED it because we want to force call the resizeEvent
        self.scene.init_canvas_dims = [self.scene.ui.graphicsView.width(), self.scene.ui.graphicsView.height()]
        self.clipboard = QtWidgets.QApplication.clipboard()

        self.listWidget_edit_row = None
        self.skip_combobox_changes = False
        self.skip_plaintextedit_changes = False

        self.ui.actionOpen.triggered.connect(lambda x: self.scene.edit.open_file(self.scene, x))
        self.ui.actionUndo.triggered.connect(lambda x: self.scene.edit.perform_undo(self.scene, x))
        self.ui.actionRedo.triggered.connect(lambda x: self.scene.edit.perform_redo(self.scene, x))
        self.ui.actionNew.triggered.connect(lambda x: self.scene.edit.perform_new(self.scene, x))
        self.ui.actionSave.triggered.connect(lambda x: self.scene.edit.save(self.scene, x))
        self.ui.actionSave_As.triggered.connect(lambda x: self.scene.edit.save_as(self.scene, x))
        self.ui.actionCopy_tikzpicture.triggered.connect(self.copy_tikzpicture_func)
        self.ui.actionCopy_document.triggered.connect(self.copy_tikzdoc_func)
        self.ui.actionShow_Aspect_Ratio.triggered.connect(self.aspect_ratio_func)

        self.ui.point_radio.clicked.connect(lambda x: connect_mode.point_radio_func(self))
        self.ui.segment_radio.clicked.connect(lambda x: connect_mode.segment_radio_func(self))
        self.ui.circle_radio.clicked.connect(lambda x: connect_mode.circle_radio_func(self))
        self.ui.polygon_radio.clicked.connect(lambda x: connect_mode.polygon_radio_func(self))
        self.ui.linestring_radio.clicked.connect(lambda x: connect_mode.linestring_radio_func(self))
        self.ui.angle_radio.clicked.connect(lambda x: connect_mode.angle_radio_func(self))
        self.ui.right_angle_radio.clicked.connect(lambda x: connect_mode.right_angle_radio_func(self))
        self.ui.cloud_radio.clicked.connect(lambda x: connect_mode.cloud_radio_func(self))

        self.ui.auto_compile_checkbox.stateChanged.connect(self.auto_compile_func)

        self.ui.point_combo.currentIndexChanged.connect(lambda x: connect_mode.point_combo_func(x, self))
        self.ui.circle_combo.currentIndexChanged.connect(lambda x: connect_mode.circle_combo_func(x, self))
        self.ui.cloud_combo.currentIndexChanged.connect(lambda x: connect_mode.cloud_combo_func(x, self))

        self.ui.tabWidget.currentChanged.connect(lambda x: tabWidget_func(x, self))
        self.ui.listWidget.itemDoubleClicked.connect(lambda x: listWidget_double_func(self))
        self.ui.listWidget.itemChanged.connect(lambda x: listWidget_text_changed_func(x, self))
        self.ui.listWidget.itemSelectionChanged.connect(lambda : listWidget_current_row_changed_func(self))

        self.ui.actionShow_PDF.toggled.connect(self.show_pdf_checked_func)
        self.ui.actionShow_Canvas_Labels.toggled.connect(self.show_canvas_labels_func)
        self.ui.actionShow_Canvas_Items.toggled.connect(self.show_canvas_items_func)

        self.ui.zoom_slider.sliderMoved.connect(self.zoom_slider_move_func)
        self.ui.zoom_slider.sliderPressed.connect(self.zoom_slider_pressed_func)
        self.ui.zoom_slider.sliderReleased.connect(self.zoom_slider_release_func)

        connect_point(self.scene)
        connect_segment(self.scene)
        connect_circle(self.scene)
        connect_polygon(self.scene)
        connect_linestring(self.scene)
        connect_colour(self.scene)
        connect_code(self.scene)

        img = Image.new("RGB", (self.width(), self.height()), (255, 255, 255))
        img.save("try-1.png", "PNG")

    def resizeEvent(self, event):
        self.scene.current_canvas_dims = [self.ui.graphicsView.width(), self.ui.graphicsView.height()]
        self.scene.setSceneRect(0, 0, self.scene.current_canvas_dims[0], self.scene.current_canvas_dims[1])
        self.ui.graphicsView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.scene.project_data.recompute_canvas(*self.scene.init_canvas_dims)
        cr.clear(self.scene)
        cr.add_all_items(self.scene)

    def closeEvent(self, event):
        if self.scene.edit.unsaved_progress:
            if self.scene.edit.unsaved_msg_box_cancelled(self.scene):
                event.ignore()

    def keyPressEvent(self,event):
        if event.isAutoRepeat():
            return None
        if event.key() == self.scene.key_bank.move_point.key:
            self.scene.key_bank.set_move_point_down()
            self.scene.select_history.reset_history()
            if self.scene.key_bank.move_point.state == KeyState.DOWN:
                focus = item_in_focus(self.scene.project_data, self.scene.mouse)
                if bool(focus)\
                and self.scene.project_data.items[focus].item["type"] == 'point'\
                and self.scene.project_data.items[focus].item["sub_type"] in [c.Point.Definition.FREE, c.Point.Definition.ON_LINE]:
                    self.scene.focus_id = focus

        if event.key() == self.scene.key_bank.move_canvas.key:
            self.scene.key_bank.set_move_canvas_down()
            self.scene.select_history.reset_history()

        if event.matches(QtGui.QKeySequence.Refresh):
            compile_latex(self.scene, False)
            cr.clear(self.scene)
            cr.add_all_items(self.scene)

        if event.matches(QtGui.QKeySequence.Delete):
            if self.scene.ui.listWidget.count() == 0:
                return
            id = self.scene.ui.listWidget.currentItem().text()
            self.scene.project_data.items[id].delete(self.scene.project_data.items)
            current_row_old = self.scene.ui.listWidget.currentRow()
            fill_listWidget_with_data(self.scene.project_data, self.scene.ui.listWidget, self.scene.current_tab_idx)
            set_selected_id_in_listWidget(self.scene, min(current_row_old, self.scene.ui.listWidget.count()-1))
            self.scene.edit.add_undo_item(self.scene)

    def keyReleaseEvent(self,event):
        if event.isAutoRepeat():
            return None
        if event.key() == self.scene.key_bank.move_point.key:
            self.scene.key_bank.set_move_point_up()
            self.scene.select_history.reset_history()
        if event.key() == self.scene.key_bank.move_canvas.key:
            self.scene.key_bank.set_move_canvas_up()
            self.scene.select_history.reset_history()
            if self.scene.canvas_moved:
                self.scene.edit.add_undo_item(self.scene)
                self.scene.canvas_moved = False

        if self.scene.focus_id:
            self.scene.edit.add_undo_item(self.scene)
        self.scene.focus_id = ''
        browser_text = syntax_highlight(self.scene.project_data.tikzify(*self.scene.current_canvas_dims, *self.scene.init_canvas_dims))
        self.scene.ui.textBrowser.setText(browser_text)

    def show_pdf_checked_func(self, state):
        self.scene.show_pdf = state
        cr.clear(self.scene)
        cr.add_all_items(self.scene)

    def show_canvas_labels_func(self, state):
        self.scene.show_canvas_labels = state
        cr.clear(self.scene)
        cr.add_all_items(self.scene)

    def show_canvas_items_func(self, state):
        self.scene.show_canvas_items = state
        cr.clear(self.scene)
        cr.add_all_items(self.scene)

    def aspect_ratio_func(self, state):
        self.scene.is_aspect_ratio = state
        cr.clear(self.scene)
        cr.add_all_items(self.scene)

    def auto_compile_func(self, state):
        self.scene.auto_compile = bool(state)

    def copy_tikzpicture_func(self):
        print('copieren')
        text = self.scene.project_data.tikzify()
        self.clipboard.clear(mode=self.clipboard.Clipboard)
        self.clipboard.setText(text, mode=self.clipboard.Clipboard)

    def copy_tikzdoc_func(self):
        print('copieren')
        text = self.scene.project_data.doc_surround_tikzify(self.scene.width(), self.scene.height(), *self.scene.init_canvas_dims)
        self.clipboard.clear(mode=self.clipboard.Clipboard)
        self.clipboard.setText(text, mode=self.clipboard.Clipboard)

    def zoom_slider_move_func(self, value):
        slider_size = 200
        value_transform = lambda x: -4 * x * (x / slider_size) if x < 0 else x
        # if value < 0:
        #     value *= 4
        value = value_transform(value)
        self.scene.project_data.set_window(
            scale=self.scene.zoom_old_saved.scale * (-value + slider_size + 10) / slider_size,
            left=self.scene.project_data.window.left,
            top=self.scene.project_data.window.top
        )
        self.scene.project_data.set_window(
            scale=self.scene.project_data.window.scale,
            left=self.scene.zoom_old_saved.left - 5 * (self.scene.project_data.window.scale - self.scene.zoom_old_saved.scale),
            top=self.scene.zoom_old_saved.top + 5 * (self.scene.project_data.window.scale - self.scene.zoom_old_saved.scale)
        )
        self.scene.project_data.recompute_canvas(self.scene.width(), self.scene.height())
        cr.clear(self.scene)
        cr.add_all_items(self.scene)

        # self.scene.eucl["window"]["scale"] = old_scale * (value + 512 + 0.5) / 512
        # scale = self.scene.eucl["window"]["scale"]
        # self.scene.eucl["window"]["left"] = old_left - 5 * (scale - old_scale)
        # self.scene.eucl["window"]["bottom"] = old_bottom - 5 * (scale - old_scale)
        # self.scene.compute_mapped_points()
        # cd.always_on_drawing_plan(self.scene)
        # cd.always_off_drawing_plan(self.scene)
        # self.scene.selected_objects.clear()
        # cd.add_all_items_to_scene(self.scene, QtCore.Qt.darkMagenta)

    def zoom_slider_pressed_func(self):
        """
        SUMMARY
            called when the zoom slider gets pressed on, saves the original position of
            the window
        PARAMETERS
            nothing
        RETURNS
            None
        """
        self.scene.zoom_old_saved = self.scene.project_data.window

    def zoom_slider_release_func(self):
        """
        SUMMARY
            called when the zoom slider is released, compiles displays change
        PARAMETERS
            value: passed from the slider
        RETURNS
            None
        """
        self.zoom_slider.setValue(0)
        self.scene.zoom_old_saved = None
        self.scene.project_data.recompute_canvas(self.scene.width(), self.scene.height())
        self.scene.edit.add_undo_item(self.scene)