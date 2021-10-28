from PyQt5 import QtCore, QtWidgets, QtGui, uic
import json
from collections import namedtuple
from pandas.io.clipboard import copy as copy_to_clipboard
from copy import deepcopy

import AddNewItem
import Utils
from Constants import *
import CanvasDrawing as cd
from SyntaxHighlight import syntax_highlight
from GraphicsScene import GraphicsScene
from Dialog.AddFunctionDialog import AddFunctionDialog

save_state = namedtuple('save_state', 'opened_file unsaved_progress')


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
        self.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        self.ui = uic.loadUi('layouts/main.ui', self)
        self.scene = GraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        #1 BEGIN: GUI widget passes in order to be able to modify them when later
        self.scene.get_textBrowser(self.ui.textBrowser)
        self.scene.get_textBrowser_pdflatex(self.ui.textBrowser_pdflatex)
        self.scene.get_actionRedo(self.ui.actionRedo)
        self.scene.get_actionUndo(self.ui.actionUndo)
        self.scene.get_actionSave(self.ui.actionSave)
        self.scene.get_actionCoordinate(self.ui.x_axis_show, self.ui.y_axis_show, self.ui.grid_show)
        self.mouse_x = 0 # mouse x coordinate
        self.mouse_y = 0 # mouse y coordinate
        #1 END

        self.current_mode = 0 # the current mode
        self.current_tool = 0 # type of mode set by the radio button

        self.point_index = 0 # the index of selected row in point dropdown list
        self.line_index = 0 # the index of selected row in segment dropdown list
        self.circle_index = 0 # the index of selected row in circle dropdown list
        self.move_index = 0 # the index of selected row in move dropdown list
        self.decorator_index = 0 # the index of selected row in decorator dropdown list

        #2 BEGIN: connects gui elements with functions
        self.ui.comboBox.currentIndexChanged.connect(self.combobox_point_change)
        self.ui.comboBox_2.currentIndexChanged.connect(self.combobox_line_change)
        self.ui.comboBox_3.currentIndexChanged.connect(self.combobox_circle_change)
        self.ui.comboBox_4.currentIndexChanged.connect(self.combobox_move_change)
        self.ui.comboBox_5.currentIndexChanged.connect(self.combobox_decorator_change)
        self.ui.radioButton.clicked.connect(self.radiobutton_triggered)
        self.ui.radioButton_2.clicked.connect(self.radiobutton_triggered_2)
        self.ui.radioButton_3.clicked.connect(self.radiobutton_triggered_3)
        self.ui.radioButton_4.clicked.connect(self.radiobutton_triggered_4)
        self.ui.radioButton_5.clicked.connect(self.radiobutton_triggered_5)
        self.ui.actionSave_As.triggered.connect(lambda x: Utils.save_as(self))
        self.ui.actionSave.triggered.connect(lambda x: Utils.save(self))
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionNew.triggered.connect(self.new_file)
        self.ui.actionopen_settings.triggered.connect(self.scene.open_settings)
        self.ui.menuHelp.aboutToShow.connect(self.scene.open_help)
        self.ui.horizontalSlider.sliderMoved.connect(self.scale_slider_move)
        self.ui.horizontalSlider.sliderPressed.connect(self.scale_slider_pressed)
        self.ui.horizontalSlider.sliderReleased.connect(self.scale_slider_release)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.x_axis_show.toggled.connect(
        lambda state: self.checkb_action_changed(state, "axis_x", "show"))
        self.ui.y_axis_show.toggled.connect(
        lambda state: self.checkb_action_changed(state, "axis_y", "show"))
        self.ui.grid_show.toggled.connect(
        lambda state: self.checkb_action_changed(state, "grid", "show"))
        self.ui.pb_add_function.clicked.connect(self.pb_add_function_clicked)
        self.ui.pb_copy_tikzpicture.triggered.connect(self.pb_copy_tikzpicture_clicked)
        self.ui.pb_copy_document.triggered.connect(self.pb_copy_document_clicked)
        self.ui.checkb_autocompile.stateChanged.connect(self.checkb_autocompile_stateChanged)
        self.ui.checkb_autocompile.setChecked(True)
        self.ui.checkb_canvas_always_on.stateChanged.connect(self.checkb_canvas_always_on_stateChanged)
        self.ui.checkb_canvas_always_on.setChecked(False)
        self.ui.checkb_show_pdf.stateChanged.connect(self.checkb_show_pdf_state_changed)
        self.ui.checkb_show_pdf.setChecked(True)
        #2 END
        #3 BEGIN: set the TikZ source code and put on the window box
        width_height = (self.scene.width(), self.scene.height())
        browser_text = AddNewItem.eucl2tkz(self.scene.eucl, self.scene.left_bottom_scale(), width_height)
        browser_text = syntax_highlight(browser_text)
        self.scene.textBrowser.setText(browser_text)
        #3 END
        self.scene.textBrowser_pdflatex.setText('')

    def showEvent(self, event):
        self.scene.setSceneRect(0, 0, self.ui.graphicsView.width(), self.ui.graphicsView.height())
        cd.empty_jpg(int(self.scene.width()), int(self.scene.height())) # write new blank image into jpg
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)


    def resizeEvent(self, event):
        self.scene.setSceneRect(0, 0, self.ui.graphicsView.width(), self.ui.graphicsView.height())
        self.scene.compute_mapped_points()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)


    def keyPressEvent(self,event):
        """
        SUMMARY
            called whenever a key is pressed, inherited method,
            performs autocompile when f5 is pressed

        PARAMETERS
            event: mandatory (inherited) parameter, passes mouse status

        RETURNS
            None
        """
        if event.matches(QtGui.QKeySequence.Refresh):
            previous_autocompile = self.scene.autocompile
            self.scene.autocompile = True
            self.scene.compile_tkz_and_render()
            self.scene.autocompile = previous_autocompile

    def combobox_point_change(self, i):
        """
        SUMMARY
            signal called when selection changes in the point combobox
            sets current mode

        PARAMETERS
            i: the index of the new item in the combobox

        RETURNS
            None
        """
        self.point_index = i
        if self.current_tool == POINT:
            self.current_mode = 100*self.current_tool+i
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def combobox_line_change(self, i):
        """
        SUMMARY
            signal called when selection changes in the segment combobox
            sets current mode

        PARAMETERS
            i: the index of the new item in the combobox

        RETURNS
            None
        """
        self.line_index = i
        if self.current_tool == SEGMENT:
            self.current_mode = 100*self.current_tool+i
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def combobox_circle_change(self, i):
        """
        SUMMARY
            signal called when selection changes in the circle combobox
            sets current mode

        PARAMETERS
            i: the index of the new item in the combobox

        RETURNS
            None
        """
        self.circle_index = i
        if self.current_tool == CIRCLE:
            self.current_mode = 100*self.current_tool+i
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def combobox_move_change(self, i):
        """
        SUMMARY
            signal called when selection changes in the move combobox
            sets current mode

        PARAMETERS
            i: the index of the new item in the combobox

        RETURNS
            None
        """
        self.move_index = i
        if self.current_tool == MOVE:
            self.current_mode = 100*self.current_tool+i
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def combobox_decorator_change(self, i):
        """
        SUMMARY
            signal called when selection changes in the decorator combobox
            sets current mode

        PARAMETERS
            i: the index of the new item in the combobox

        RETURNS
            None
        """
        self.decorator_index = i
        if self.current_tool == DECORATOR:
            self.current_mode = 100*self.current_tool+i
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def radiobutton_triggered(self):
        """
        SUMMARY
            signal called when the point radio button is clicked into focus
            sets current mode

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.current_tool = POINT
        self.current_mode = 100*self.current_tool+self.point_index
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def radiobutton_triggered_2(self):
        """
        SUMMARY
            signal called when the segment radio button is clicked into focus
            sets current mode

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.current_tool = SEGMENT
        self.current_mode = 100*self.current_tool+self.line_index
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def radiobutton_triggered_3(self):
        """
        SUMMARY
            signal called when the circle radio button is clicked into focus
            sets current mode

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.current_tool = CIRCLE
        self.current_mode = 100*self.current_tool+self.circle_index
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def radiobutton_triggered_4(self):
        """
        SUMMARY
            signal called when the move radio button is clicked into focus
            sets current mode

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.current_tool = MOVE
        self.current_mode = 100*self.current_tool+self.move_index
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def radiobutton_triggered_5(self):
        """
        SUMMARY
            signal called when the decorator radio button is clicked into focus
            sets current mode

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.current_tool = DECORATOR
        self.current_mode = 100*self.current_tool+self.decorator_index
        self.scene.set_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)


    def open_file(self):
        """
        SUMMARY
            brings up open file popup window, loads and displays it

        PARAMETERS
            nothing

        RETURNS
            None
        """
        fname = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption="Open a file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
        if fname[0] != '':
            self.scene.eucl = Utils.read_eucl_file(fname[0])
            self.scene.compute_mapped_points()
            self.scene.compile_tkz_and_render()
            self.scene.save_state = save_state(fname[0], self.scene.save_state.unsaved_progress)
            self.scene.add_new_undo_item()
            cd.always_on_drawing_plan(self.scene)
            cd.always_off_drawing_plan(self.scene)
            self.scene.axis_grid_checkbox_shifter()

    def new_file(self):
        """
        SUMMARY
            creates new file, clears the canvas

        PARAMETERS
            nothing

        RETURNS
            None
        """
        cd.empty_jpg(int(self.scene.width()), self.scene.height())
        self.scene.eucl = AddNewItem.new_eucl_file()
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
        previous_autocompile = self.scene.autocompile
        self.scene.autocompile = False
        self.scene.compile_tkz_and_render()
        self.scene.autocompile = previous_autocompile
        self.scene.add_new_undo_item()
        self.scene.axis_grid_checkbox_shifter()


    def scale_slider_move(self, value):
        """
        SUMMARY
            called when the zoom slider is moves, draws the changed positions of
            the objects

        PARAMETERS
            value: passed from the slider

        RETURNS
            None
        """
        old_left, old_bottom, old_scale = self.scene.zoom_new_window_params
        self.scene.eucl["window"]["scale"] = old_scale * (value+512+0.5)/512
        scale = self.scene.eucl["window"]["scale"]
        self.scene.eucl["window"]["left"] = old_left - 5 * (scale-old_scale)
        self.scene.eucl["window"]["bottom"] = old_bottom - 5 * (scale-old_scale)
        self.scene.compute_mapped_points()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
        self.scene.selected_objects.clear()
        cd.add_all_items_to_scene(self.scene, QtCore.Qt.darkMagenta)

    def scale_slider_pressed(self):
        """
        SUMMARY
            called when the zoom slider gets pressed on, saves the original position of
            the window

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.zoom_new_window_params = self.scene.left_bottom_scale()

    def scale_slider_release(self):
        """
        SUMMARY
            called when the zoom slider is released, compiles displays change

        PARAMETERS
            value: passed from the slider

        RETURNS
            None
        """
        self.horizontalSlider.setValue(0)
        self.zoom_new_window_params = [0,0,0]
        self.scene.selected_objects.clear()
        self.scene.compile_tkz_and_render()
        self.scene.compute_mapped_points()
        self.scene.add_new_undo_item()

    def undo(self):
        """
        SUMMARY
            called when CTRL+Z is pressed, deals with undo & redo history,
            compiles and displays change

        PARAMETERS
            nothing

        RETURNS
            None
        """
        if len(self.scene.undo_history) > 1:
            self.scene.eucl = deepcopy(self.scene.undo_history[-2])
            self.scene.redo_history.append(self.scene.undo_history.pop())
            self.scene.selected_objects.clear()
            self.scene.compute_mapped_points()
            self.scene.compile_tkz_and_render()
            if len(self.scene.undo_history) == 1:
                self.ui.actionUndo.setEnabled(False)
            self.ui.actionRedo.setEnabled(True)
            self.scene.axis_grid_checkbox_shifter()
            self.scene.save_state = save_state(self.scene.save_state.opened_file, self.scene.save_state.unsaved_progress - 1)
            if self.scene.save_state.unsaved_progress == 0:
                self.ui.actionSave.setEnabled(False)
            else:
                self.ui.actionSave.setEnabled(True)

    def redo(self):
        """
        SUMMARY
            called when CTRL+SHIFT+Z is pressed, deals with undo & redo history,
            compiles and displays change

        PARAMETERS
            nothing

        RETURNS
            None
        """
        if self.scene.redo_history != []:
            self.scene.eucl = deepcopy(self.scene.redo_history[-1])
            self.scene.undo_history.append(self.scene.redo_history.pop())
            self.scene.selected_objects.clear()
            self.scene.compute_mapped_points()
            self.scene.compile_tkz_and_render()
            if self.scene.redo_history == []:
                self.ui.actionRedo.setEnabled(False)
            self.ui.actionUndo.setEnabled(True)
            self.scene.axis_grid_checkbox_shifter()
            self.scene.save_state = save_state(self.scene.save_state.opened_file, self.scene.save_state.unsaved_progress + 1)
            if self.scene.save_state.unsaved_progress == 0:
                self.scene.actionSave.setEnabled(False)
            else:
                self.scene.actionSave.setEnabled(True)

    def checkb_state_changed(self, state, property, secondary_property=None):
        """
        SUMMARY
            called when CTRL+SHIFT+Z is pressed, deals with undo & redo history,
            compiles and displays change

        PARAMETERS
            state: mandatory parameter, passes checkbox state
            property: eucl dictionary key ("points", "segments", ...)
            secondary_property: property of the (point, segment, ...)

        RETURNS
            None
        """
        if secondary_property is None:
            item = self.scene.eucl
            my_property = property
        else:
            item = self.scene.eucl[property]
            my_property = secondary_property

        if state == QtCore.Qt.Unchecked and item[my_property] == True:
            item[my_property] = False
            self.scene.selected_objects.clear()
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        elif state == QtCore.Qt.Checked and item[my_property] == False:
            item[my_property] = True
            self.scene.selected_objects.clear()
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()

    def checkb_action_changed(self, state, property, secondary_property=None):
        """
        SUMMARY
            called when CTRL+SHIFT+Z is pressed, deals with undo & redo history,
            compiles and displays change

        PARAMETERS
            state: mandatory parameter, passes checkbox state
            property: eucl dictionary key ("points", "segments", ...)
            secondary_property: property of the (point, segment, ...)

        RETURNS
            None
        """
        if secondary_property is None:
            item = self.scene.eucl
            my_property = property
        else:
            item = self.scene.eucl[property]
            my_property = secondary_property

        if state == False and item[my_property] == True:
            item[my_property] = False
            self.scene.selected_objects.clear()
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        elif state == True and item[my_property] == False:
            item[my_property] = True
            self.scene.selected_objects.clear()
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()


    def pb_add_function_clicked(self):
        """
        SUMMARY
            called when add function button is pressed, brings up add function dialog

        PARAMETERS
            nothing

        RETURNS
            None
        """
        dialog = AddFunctionDialog(self.scene)
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def pb_copy_tikzpicture_clicked(self):
        """
        SUMMARY
            copies tikzpicture environment to the clipboard

        PARAMETERS
            nothing

        RETURNS
            None
        """
        copy_to_clipboard(AddNewItem.eucl2tkz(self.scene.eucl, self.scene.left_bottom_scale(),\
                                              width_height = [self.scene.width(), self.scene.height()]))

    def pb_copy_document_clicked(self):
        """
        SUMMARY
            copies tikz document to the clipboard

        PARAMETERS
            nothing

        RETURNS
            None
        """
        tikzpicture_string = AddNewItem.eucl2tkz(self.scene.eucl, self.scene.left_bottom_scale(),\
                                              width_height = [self.scene.width(), self.scene.height()])
        copy_to_clipboard(AddNewItem.tkz2tex(self.scene.eucl, tikzpicture_string))

    def checkb_autocompile_stateChanged(self, state):
        """
        SUMMARY
            copies tikzpicture environment to the clipboard

        PARAMETERS
            nothing

        RETURNS
            None
        """
        if state == QtCore.Qt.Unchecked:
            self.scene.autocompile = False
        else:
            self.scene.autocompile = True
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def checkb_canvas_always_on_stateChanged(self, state):
        """
        SUMMARY
            changes canvas_always_on value according to the checkbox

        PARAMETERS
            state: the checkbox state

        RETURNS
            None
        """
        if state == QtCore.Qt.Unchecked:
            self.scene.canvas_always_on = False
        else:
            self.scene.canvas_always_on = True
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def checkb_show_pdf_state_changed(self, state):
        """
        SUMMARY
            changes show_pdf value according to the checkbox

        PARAMETERS
            state: the checkbox state

        RETURNS
            None
        """
        if state == QtCore.Qt.Unchecked:
            self.scene.show_pdf = False
        else:
            self.scene.show_pdf = True
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
