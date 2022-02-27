from PyQt5 import QtCore, QtWidgets, QtGui, uic
import json
from collections import namedtuple
from copy import deepcopy
import os

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
from ConnectSignal.ConnectPolygon import connect_polygon
from Fill.ListWidget import fill_listWidget_with_data
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
        self.ui = uic.loadUi('main_2.ui', self)
        self.scene = GraphicsScene(self.ui, self.setWindowTitle)
        self.ui.graphicsView.setScene(self.scene)
        self.show()
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

        self.ui.point_radio.clicked.connect(lambda x: connect_mode.point_radio_func(self))
        self.ui.segment_radio.clicked.connect(lambda x: connect_mode.segment_radio_func(self))
        self.ui.circle_radio.clicked.connect(lambda x: connect_mode.circle_radio_func(self))
        self.ui.polygon_radio.clicked.connect(lambda x: connect_mode.polygon_radio_func(self))
        self.ui.linestring_radio.clicked.connect(lambda x: connect_mode.linestring_radio_func(self))
        self.ui.angle_radio.clicked.connect(lambda x: connect_mode.angle_radio_func(self))
        self.ui.right_angle_radio.clicked.connect(lambda x: connect_mode.right_angle_radio_func(self))

        self.ui.auto_compile_checkbox.stateChanged.connect(self.auto_compile_func)

        self.ui.point_combo.currentIndexChanged.connect(lambda x: connect_mode.point_combo_func(x, self))
        self.ui.circle_combo.currentIndexChanged.connect(lambda x: connect_mode.circle_combo_func(x, self))

        self.ui.tabWidget.currentChanged.connect(lambda x: tabWidget_func(x, self))
        self.ui.listWidget.itemDoubleClicked.connect(lambda x: listWidget_double_func(x, self))
        self.ui.listWidget.itemChanged.connect(lambda x: listWidget_text_changed_func(x, self))
        self.ui.listWidget.itemSelectionChanged.connect(lambda : listWidget_current_row_changed_func(self))

        self.ui.actionShow_PDF.toggled.connect(self.show_pdf_checked_func)
        self.ui.actionShow_Canvas_Labels.toggled.connect(self.show_canvas_labels_func)
        self.ui.actionShow_Canvas_Items.toggled.connect(self.show_canvas_items_func)

        connect_point(self.scene)
        connect_segment(self.scene)
        connect_polygon(self.scene)
        connect_colour(self.scene)

    def resizeEvent(self, event):
        self.scene.setSceneRect(0, 0, self.ui.graphicsView.width(), self.ui.graphicsView.height())

    def closeEvent(self, event):
        if self.scene.edit.unsaved_progress:
            if self.scene.edit.unsaved_msg_box_cancelled(self.scene):
                event.ignore()

    def keyPressEvent(self,event):
        if event.isAutoRepeat():
            return None
        modifiers = event.modifiers()
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
            fill_listWidget_with_data(self.scene.project_data, self.ui.listWidget, self.scene.current_tab_idx)
            if self.scene.ui.listWidget.count() > 0:
                self.scene.ui.listWidget.item(self.scene.ui.listWidget.count()-1).setSelected(True)
                self.scene.ui.listWidget.setCurrentRow(self.scene.ui.listWidget.count()-1)
            fill_all_fields(self.scene)
            compile_latex(self.scene, True)
            cr.clear(self.scene)
            cr.add_all_items(self.scene)


    def keyReleaseEvent(self,event):
        if event.isAutoRepeat():
            return None
        if event.key() == self.scene.key_bank.move_point.key:
            self.scene.key_bank.set_move_point_up()
            self.scene.select_history.reset_history()
        if event.key() == self.scene.key_bank.move_canvas.key:
            self.scene.key_bank.set_move_canvas_up()
            self.scene.select_history.reset_history()
            self.scene.edit.add_undo_item(self.scene)

        if self.scene.focus_id:
            self.scene.edit.add_undo_item(self.scene)
        self.scene.focus_id = ''
        browser_text = syntax_highlight(self.scene.project_data.tikzify())
        self.scene.ui.textBrowser.setText(browser_text)


    def references_to_scene(self):
        dictionary = {}
        dictionary["list_widget"] = self.ui.listWidget
        dictionary["tab_widget"] = self.ui.tabWidget
        dictionary["text_browser"] = self.ui.textBrowser
        dictionary["action_undo"] = self.ui.actionUndo
        dictionary["action_redo"] = self.ui.actionRedo
        dictionary["action_save"] = self.ui.actionSave
        return dictionary

    def point_widgets():
        dictionary = {}
        dictionary["plain_text_edit"] = self.plainTextEdit
        # dictionary["plain_text_edit"] = self.plainTextEdit

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

    def auto_compile_func(self, state):
        self.scene.auto_compile = bool(state)

    def copy_tikzpicture_func(self):
        print('copieren')
        text = self.scene.project_data.tikzify()
        self.clipboard.clear(mode=self.clipboard.Clipboard)
        self.clipboard.setText(text, mode=self.clipboard.Clipboard)

    def copy_tikzdoc_func(self):
        print('copieren')
        text = self.scene.project_data.doc_surround_tikzify()
        self.clipboard.clear(mode=self.clipboard.Clipboard)
        self.clipboard.setText(text, mode=self.clipboard.Clipboard)
#
