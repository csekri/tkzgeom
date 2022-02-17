from copy import deepcopy
import json
from PyQt5 import QtCore, QtWidgets, QtGui

from Factory import Factory
from Items import Items
from Point import Point
from PointClasses.FreePoint import FreePoint
from Segment import Segment

import CanvasRendering as cr

class EditManagement:
    def __init__(self):
        self.unsaved_progress = 0
        self.opened_file = ''
        self.undo_history = []
        self.redo_history = []

    def perform_undo(self, project_data, qaction_undo, qaction_redo, qaction_save):
        if len(self.undo_history) <= 2:
            return None
        project_data = deepcopy(self.undo_history[-2])
        self.redo_history.append(self.undo_history.pop())
        if len(self.undo_history) == 1:
            self.qaction_undo.setEnabled(False)
        self.qaction_redo.setEnabled(True)

        self.unsaved_progress -= 1

        if self.unsaved_progress == 0:
            self.qaction_save.setEnabled(False)
        else:
            self.qaction_save.setEnabled(True)

    def perform_redo(self, project_data, qaction_undo, qaction_redo, qaction_save):
        if not self.redo_history:
            return None
        project_data = deepcopy(self.redo_history[-1])
        self.undo_history.append(self.redo_history.pop())
        if not self.redo_history:
            self.ui.actionRedo.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        self.unsaved_progress += 1
        if self.unsaved_progress == 0:
            self.qaction_save.setEnabled(False)
        else:
            self.qaction_save.setEnabled(True)



    def open_file(self, main_window, scene, *kwargs):
        fname = QtWidgets.QFileDialog.getOpenFileName(parent=main_window, caption="Open a file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
        if fname[0] != '':
            with open(fname[0]) as f:
                dictionary = json.load(f)
                scene.project_data = Items(
                    dictionary["window"],
                    dictionary["packages"],
                    dictionary["bg_colour"],
                    dictionary["colours"],
                    dictionary["code_before"],
                    dictionary["code_after"]
                )
                for item in (dictionary["items"]):
                    scene.project_data.add(Factory.create_item(item))
            self.opened_file = fname[0]
        scene.project_data.recompute_canvas(641, 641)
        cr.clear(scene)
        cr.add_all_items(scene)
        scene.key_bank.set_move_canvas_up()
