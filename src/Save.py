from copy import deepcopy
import json
from PyQt5 import QtWidgets
from PIL import Image

from Factory import Factory
from Items import Items
from Compile import compile_latex
from SyntaxHighlight import syntax_highlight
import CanvasRendering as cr
from Fill.FillAll import fill_all_fields
from Fill.ListWidget import fill_listWidget_with_data, set_selected_id_in_listWidget


class EditManagement:
    def __init__(self):
        """Construct EditManagement."""
        self.unsaved_progress = -1
        self.opened_file = ''
        self.undo_history = []
        self.redo_history = []

    def window_name(self):
        """Return window name."""
        name = 'TkzGeom | '
        if self.opened_file == '':
            name += 'untitled'
        else:
            name += self.opened_file
        if self.unsaved_progress != 0:
            name += '*'
        return name

    def add_undo_item(self, scene):
        """Add new undo point after edit."""
        self.undo_history.append(deepcopy(scene.project_data))
        self.redo_history.clear()
        self.unsaved_progress += 1
        scene.ui.actionUndo.setEnabled(True)
        scene.ui.actionRedo.setEnabled(False)
        scene.ui.actionSave.setEnabled(bool(self.unsaved_progress))
        scene.title(self.window_name())
        compile_latex(scene, True)
        browser_text = syntax_highlight(scene.syntax,
                                        scene.project_data.tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        scene.ui.textBrowser.setText(browser_text)
        fill_all_fields(scene)

        cr.clear(scene)
        cr.add_all_items(scene)

    def perform_undo(self, scene, *kwargs):
        """Do undo."""
        if len(self.undo_history) < 2:
            return None
        scene.project_data = deepcopy(self.undo_history[-2])
        self.redo_history.append(self.undo_history.pop())
        if len(self.undo_history) == 1:
            scene.ui.actionUndo.setEnabled(False)
        scene.ui.actionRedo.setEnabled(True)

        self.unsaved_progress -= 1
        scene.ui.actionSave.setEnabled(bool(self.unsaved_progress))

        compile_latex(scene, True)
        browser_text = syntax_highlight(scene.syntax, scene.project_data.tikzify(*scene.current_canvas_dims,
                                                                                 *scene.init_canvas_dims))
        scene.ui.textBrowser.setText(browser_text)
        current_row_old = scene.ui.listWidget.currentRow()
        fill_listWidget_with_data(scene.project_data, scene.ui.listWidget, scene.current_tab_idx)
        set_selected_id_in_listWidget(scene, min(current_row_old, scene.ui.listWidget.count() - 1))
        fill_all_fields(scene)
        cr.clear(scene)
        cr.add_all_items(scene)
        scene.title(self.window_name())

    def perform_redo(self, scene, *kwargs):
        """Do redo."""
        if not self.redo_history:
            return None
        scene.project_data = deepcopy(self.redo_history[-1])
        self.undo_history.append(self.redo_history.pop())
        scene.ui.actionRedo.setEnabled(bool(self.redo_history))
        scene.ui.actionUndo.setEnabled(True)
        self.unsaved_progress += 1
        scene.ui.actionSave.setEnabled(bool(self.unsaved_progress))
        compile_latex(scene, True)
        browser_text = syntax_highlight(scene.syntax, scene.project_data.tikzify(*scene.current_canvas_dims,
                                                                                 *scene.init_canvas_dims))
        scene.ui.textBrowser.setText(browser_text)
        current_row_old = scene.ui.listWidget.currentRow()
        fill_listWidget_with_data(scene.project_data, scene.ui.listWidget, scene.current_tab_idx)
        set_selected_id_in_listWidget(scene, min(current_row_old, scene.ui.listWidget.count() - 1))
        fill_all_fields(scene)
        cr.clear(scene)
        cr.add_all_items(scene)
        scene.title(self.window_name())

    def perform_new(self, scene, *kwargs):
        """Do new."""
        if not self.unsaved_msg_box_cancelled(scene):
            img = Image.new("RGB", (int(scene.width()), int(scene.height())), (255, 255, 255))
            img.save("try-1.png", "PNG")
            scene.project_data = Items()
            fill_listWidget_with_data(scene.project_data, scene.ui.listWidget, scene.current_tab_idx)
            set_selected_id_in_listWidget(scene, 0)
            self.add_undo_item(scene)
            self.unsaved_progress = 0
            # compile_latex(scene, True)
            browser_text = syntax_highlight(scene.syntax, scene.project_data.tikzify(*scene.current_canvas_dims,
                                                                                     *scene.init_canvas_dims))
            scene.ui.textBrowser.setText(browser_text)
            fill_all_fields(scene)
            cr.clear(scene)
            cr.add_all_items(scene)
        scene.title(self.window_name())

    def open_file(self, scene, *kwargs):
        """Open file."""
        if not self.unsaved_msg_box_cancelled(scene):
            fname = QtWidgets.QFileDialog.getOpenFileName(
                caption='Open a file',
                filter='TikzGeom Project File / .tgeo (*.tgeo *.TGEO)')
            if fname[0] != '':
                with open(fname[0]) as f:
                    dictionary = json.load(f)
                    scene.project_data = Items(
                        dictionary["window"],
                        dictionary["packages"],
                        dictionary["bg_colour"],
                        dictionary["code_before"],
                        dictionary["code_after"]
                    )
                    for item in (dictionary["items"]):
                        scene.project_data.add(Factory.create_item(item))
                self.opened_file = fname[0]
                scene.project_data.recompute_canvas(*scene.init_canvas_dims)
                fill_listWidget_with_data(scene.project_data, scene.ui.listWidget, scene.current_tab_idx)
                set_selected_id_in_listWidget(scene, 0)
                scene.edit.add_undo_item(scene)
                self.unsaved_progress = 0
                # compile_latex(scene, True)
                browser_text = syntax_highlight(scene.syntax, scene.project_data.tikzify(*scene.current_canvas_dims,
                                                                                         *scene.init_canvas_dims))
                scene.ui.textBrowser.setText(browser_text)
                # fill_all_fields(scene)
                # cr.clear(scene)
                # cr.add_all_items(scene)
        scene.key_bank.set_move_canvas_up()
        scene.title(self.window_name())

    def save(self, scene, *kwargs):
        """Save file."""
        print('before save', self.unsaved_progress)
        if self.opened_file != '' and self.unsaved_progress != 0:
            with open(self.opened_file, 'w') as f:
                json.dump(scene.project_data.state_dict(), f, indent=4)
            self.unsaved_progress = 0
            scene.ui.actionSave.setEnabled(False)
        else:
            self.save_as(scene)
        scene.title(self.window_name())
        scene.key_bank.set_move_canvas_up()
        print('after save', self.unsaved_progress)

    def save_as(self, scene, *kwargs):
        """Save as."""
        """
        SUMMARY
            equivalent to "Save As", brings up save popup window in any case
        PARAMETERS
            nothing
        RETURNS
            None
        """
        fname = QtWidgets.QFileDialog.getSaveFileName(
            caption='Save file',
            filter='TikzGeom Project File / .tgeo (*.tgeo *.TGEO)')
        if fname[0] != '':
            with open(fname[0], 'w') as f:
                json.dump(scene.project_data.state_dict(), f, indent=4)
            self.opened_file = fname[0]
            self.unsaved_progress = 0
        scene.title(self.window_name())
        scene.key_bank.set_move_canvas_up()

    def unsaved_msg_box_cancelled(self, scene):
        """Make save messagebox."""
        print(self.unsaved_progress)
        if self.unsaved_progress == 0:
            return False
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText('The document has been modified.')
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
        ret = msgBox.exec_()
        if ret == QtWidgets.QMessageBox.Save:
            self.save(scene)
        scene.key_bank.set_move_canvas_up()
        if ret == QtWidgets.QMessageBox.Cancel:
            return True
        return False
