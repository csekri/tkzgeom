from PyQt5 import QtCore, QtWidgets, QtGui, uic
import json
from collections import namedtuple
from pandas.io.clipboard import copy as copy_to_clipboard
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
        uic.loadUi('main_2.ui', self)
        self.scene = GraphicsScene(self.references_to_scene(), self.setWindowTitle)
        self.graphicsView.setScene(self.scene)
        self.show()
        self.listWidget_edit_row = None
        self.skip_combobox_changes = False

        self.actionOpen.triggered.connect(lambda x: self.scene.edit.open_file(self.scene, x))
        self.actionUndo.triggered.connect(lambda x: self.scene.edit.perform_undo(self.scene, x))
        self.actionRedo.triggered.connect(lambda x: self.scene.edit.perform_redo(self.scene, x))
        self.actionNew.triggered.connect(lambda x: self.scene.edit.perform_new(self.scene, x))
        self.actionSave.triggered.connect(lambda x: self.scene.edit.save(self.scene, x))
        self.actionSave_As.triggered.connect(lambda x: self.scene.edit.save_as(self.scene, x))


        self.point_radio.clicked.connect(lambda x: connect_mode.point_radio_func(self))
        self.segment_radio.clicked.connect(lambda x: connect_mode.segment_radio_func(self))
        self.circle_radio.clicked.connect(lambda x: connect_mode.circle_radio_func(self))
        self.polygon_radio.clicked.connect(lambda x: connect_mode.polygon_radio_func(self))
        self.linestring_radio.clicked.connect(lambda x: connect_mode.linestring_radio_func(self))
        self.angle_radio.clicked.connect(lambda x: connect_mode.angle_radio_func(self))
        self.right_angle_radio.clicked.connect(lambda x: connect_mode.right_angle_radio_func(self))

        self.auto_compile_checkbox.stateChanged.connect(self.auto_compile_func)

        self.point_combo.currentIndexChanged.connect(lambda x: connect_mode.point_combo_func(x, self))
        self.circle_combo.currentIndexChanged.connect(lambda x: connect_mode.circle_combo_func(x, self))

        self.tabWidget.currentChanged.connect(lambda x: tabWidget_func(x, self))
        self.listWidget.itemDoubleClicked.connect(lambda x: listWidget_double_func(x, self))
        self.listWidget.itemChanged.connect(lambda x: listWidget_text_changed_func(x, self))
        self.listWidget.itemSelectionChanged.connect(lambda : listWidget_current_row_changed_func(self))

        self.actionShow_PDF.toggled.connect(self.show_pdf_checked_func)
        self.actionShow_Canvas_Labels.toggled.connect(self.show_canvas_labels_func)
        self.actionShow_Canvas_Items.toggled.connect(self.show_canvas_items_func)

        connect_point(self)

    def resizeEvent(self, event):
        self.scene.setSceneRect(0, 0, self.graphicsView.width(), self.graphicsView.height())


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

    def keyReleaseEvent(self,event):
        if event.isAutoRepeat():
            return None
        if event.key() == self.scene.key_bank.move_point.key:
            self.scene.key_bank.set_move_point_up()
            self.scene.select_history.reset_history()
        if event.key() == self.scene.key_bank.move_canvas.key:
            self.scene.key_bank.set_move_canvas_up()
            self.scene.select_history.reset_history()
        if self.scene.focus_id:
            self.scene.edit.add_undo_item(self.scene)
        self.scene.focus_id = ''
        browser_text = syntax_highlight(self.scene.project_data.tikzify())
        self.scene.widgets["text_browser"].setText(browser_text)


    def references_to_scene(self):
        dictionary = {}
        dictionary["list_widget"] = self.listWidget
        dictionary["tab_widget"] = self.tabWidget
        dictionary["text_browser"] = self.textBrowser
        dictionary["action_undo"] = self.actionUndo
        dictionary["action_redo"] = self.actionRedo
        dictionary["action_save"] = self.actionSave
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

#
