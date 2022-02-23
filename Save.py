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
        self.unsaved_progress = -1
        self.opened_file = ''
        self.undo_history = []
        self.redo_history = []

    def window_name(self):
        name = 'TkzGeom | '
        if self.opened_file == '':
            name += 'untitled'
        else:
            name += self.opened_file
        if self.unsaved_progress != 0:
            name += '*'
        return name

    def add_undo_item(self, scene):
        self.undo_history.append(deepcopy(scene.project_data))
        self.redo_history.clear()
        self.unsaved_progress += 1
        scene.widgets["action_undo"].setEnabled(True)
        scene.widgets["action_redo"].setEnabled(False)
        if self.unsaved_progress != 0:
            scene.widgets["action_save"].setEnabled(True)
        else:
            scene.widgets["action_save"].setEnabled(False)
        scene.title(self.window_name())

    def perform_undo(self, scene, *kwargs):
        if len(self.undo_history) < 2:
            return None
        scene.project_data = deepcopy(self.undo_history[-2])
        self.redo_history.append(self.undo_history.pop())
        if len(self.undo_history) == 1:
            scene.widgets["action_undo"].setEnabled(False)
        scene.widgets["action_redo"].setEnabled(True)

        self.unsaved_progress -= 1

        if self.unsaved_progress == 0:
            scene.widgets["action_save"].setEnabled(False)
        else:
            scene.widgets["action_save"].setEnabled(True)

        cr.clear(scene)
        cr.add_all_items(scene)
        scene.title(self.window_name())


    def perform_redo(self, scene, *kwargs):
        if not self.redo_history:
            return None
        scene.project_data = deepcopy(self.redo_history[-1])
        self.undo_history.append(self.redo_history.pop())
        if not self.redo_history:
            scene.widgets["action_redo"].setEnabled(False)
        scene.widgets["action_undo"].setEnabled(True)
        self.unsaved_progress += 1
        if self.unsaved_progress == 0:
            scene.widgets["action_save"].setEnabled(False)
        else:
            scene.widgets["action_save"].setEnabled(True)
        cr.clear(scene)
        cr.add_all_items(scene)
        scene.title(self.window_name())


    def perform_new(self, scene, *kwargs):
        if not self.unsaved_msg_box_cancelled(scene):
            scene.project_data = Items()
            self.add_undo_item(scene)
            self.unsaved_progress = 0
            cr.clear(scene)
            cr.add_all_items(scene)
        scene.title(self.window_name())


    def open_file(self, scene, *kwargs):
        if not self.unsaved_msg_box_cancelled(scene):
            fname = QtWidgets.QFileDialog.getOpenFileName(caption="Open a file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
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
                scene.edit.add_undo_item(scene)
                cr.clear(scene)
                cr.add_all_items(scene)
        scene.key_bank.set_move_canvas_up()
        scene.title(self.window_name())


    def save(self, scene, *kwargs):
        if self.opened_file != '' and self.unsaved_progress != 0:
            with open(self.opened_file, 'w') as f:
                    json.dump(scene.project_data.state_dict(), f, indent=4)
            self.unsaved_progress = 0
            scene.widgets["action_save"].setEnabled(False)
        else:
            self.save_as(scene)
        scene.title(self.window_name())


    def save_as(self, scene, *kwargs):
        """
        SUMMARY
            equivalent to "Save As", brings up save popup window in any case
        PARAMETERS
            nothing
        RETURNS
            None
        """
        fname = QtWidgets.QFileDialog.getSaveFileName(caption="Save file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
        if fname[0] != '':
            with open(fname[0], 'w') as f:
                    json.dump(scene.project_data.state_dict(), f, indent=4)
            self.opened_file = fname[0]
            self.unsaved_progress = False
        scene.title(self.window_name())

    def unsaved_msg_box_cancelled(self, scene):
        print(self.unsaved_progress)
        if self.unsaved_progress == 0:
            return False
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText('The document has been modified.')
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
        ret = msgBox.exec_()
        if ret == QtWidgets.QMessageBox.Save:
            self.save(scene)
        scene.key_bank.set_move_canvas_up()
        if ret == QtWidgets.QMessageBox.Cancel:
            return True
        return False


#
