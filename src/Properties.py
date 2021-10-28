"""
this file contains the definition of the qui window for the property
settings for for various objects and other settings
"""

from PyQt5 import QtCore, QtWidgets, QtGui, uic
import json
from copy import deepcopy
import numpy as np
from collections import namedtuple

from CanvasDrawing import always_on_drawing_plan, always_off_drawing_plan
import AddNewItem
import Utils
from Constants import *
from Dialog.DuckProperties import DuckPropertiesDialog
from PropertiesConnectGUI import *
from PropertiesFillItemFields import fill_fields

save_state = namedtuple('save_state', 'opened_file unsaved_progress')


def add_objects_to_combobox(dialog):
    """
    SUMMARY
        adds all items to every QListWidgets

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
    dialog.ui.pt_cb_selector.clear()
    dialog.ui.sg_cb_selector.clear()
    dialog.ui.crc_cb_selector.clear()
    dialog.ui.ang_cb_selector.clear()
    dialog.ui.pol_cb_selector.clear()
    dialog.ui.fct_cb_selector.clear()
    dialog.ui.set_cb_selector.clear()
    for point in dialog.scene.eucl["points"]:
        if point["id"] == 'pt_default':
            dialog.ui.pt_cb_selector.addItem('default')
        else:
            dialog.ui.pt_cb_selector.addItem(point["id"])

    for segment in dialog.scene.eucl["segments"]:
        if segment["id"] == 'sg_default':
            dialog.ui.sg_cb_selector.addItem('default')
        else:
            text = "%s_%s" % (segment["points"]["from"], segment["points"]["to"])
            dialog.ui.sg_cb_selector.addItem(text)

    for circle in dialog.scene.eucl["circles"]:
        if circle["id"] == 'crc_default':
            dialog.ui.crc_cb_selector.addItem('default')
        else:
            if circle["type"] == 'circum_circle':
                text = 'circ_%s_%s_%s' % (circle["points"]["A"], circle["points"]["B"], circle["points"]["C"])
            elif circle["type"] == 'inscribed_circle':
                text = 'insc_%s_%s_%s' % (circle["points"]["A"], circle["points"]["B"], circle["points"]["C"])
            elif circle["type"] == 'two_point_circle':
                text = 'two_%s_%s' % (circle["points"]["O"], circle["points"]["A"])
            elif circle["type"] == 'sector':
                text = 'sect_%s_%s_%s' % (circle["points"]["O"], circle["points"]["A"], circle["points"]["B"])
            elif circle["type"] == 'arc':
                text = 'arc_%s_%s_%s' % (circle["points"]["O"], circle["points"]["A"], circle["points"]["B"])
            dialog.ui.crc_cb_selector.addItem(text)

    for angle in dialog.scene.eucl["angles"]:
        if angle["id"] == 'ang_default':
            dialog.ui.ang_cb_selector.addItem('default')
        else:
            text = "%s_%s_%s" % (angle["points"]["A"], angle["points"]["B"], angle["points"]["C"])
            dialog.ui.ang_cb_selector.addItem(text)

    for polygon in dialog.scene.eucl["polygons"]:
        if polygon["id"] == 'pol_default':
            dialog.ui.pol_cb_selector.addItem('default')
        else:
            text = "%s-gon_%s" % (len(polygon["points"]), polygon["id"])
            dialog.ui.pol_cb_selector.addItem(text)

    for function in dialog.scene.eucl["functions"]:
        if function["id"] == 'fct_default':
            dialog.ui.fct_cb_selector.addItem('default')
        else:
            if function["type"] == 'yfx':
                text = 'y=' + function["def"]
            elif function["type"] == 'polar':
                text = 'r=' + function["def"]
            elif function["type"] == 'parametric':
                func = function["def"].split('||')
                text = 'x=%s, y=%s' % (func[0], func[1])
            dialog.ui.fct_cb_selector.addItem(text)

    for i, package in enumerate(dialog.scene.eucl["packages"]):
        item = QtWidgets.QListWidgetItem(package)
        if i > 5:
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        dialog.ui.set_cb_selector.addItem(item)


class PropertiesDialog(QtWidgets.QDialog):
    """
    class for the properties dialog inheriting QtWidgets.QDialog
    """
    def __init__ (self, scene):
        """
        SUMMARY
            constructor of PropertiesDialog class

        PARAMETERS
            scene: GraphicsScene

        RETURNS
            None
        """
        super(PropertiesDialog, self).__init__ ()
        self.ui = uic.loadUi('layouts/properties_dialog.ui', self)
        self.setWindowTitle("Properties")
        self.scene = scene
        self.current_id = 0
        self.state_change_ignore = False
        self.new_default = None
        self.tab_index = self.ui.tabWidget.currentIndex()
        self.ui.tabWidget.setStyleSheet("\
QTabBar::tab {\
    height:55px;\
    width: 55px;\
    padding-left: 3px;\
    padding-right: -14px;\
    padding-top: -5px;\
    padding-bottom: -5px;\
    color: black;\
}\
QTabBar::tab:selected {\
     background: lightgray;\
}")
        self.ui.set_tabwidget.setStyleSheet("\
QTabBar::tab {\
    height:25px;\
    width: 55px;\
    padding-left: 3px;\
    padding-right: 3px;\
    padding-top: 3px;\
    padding-bottom: 3px;\
    color: black;\
}\
QTabBar::tab:selected {\
     background: lightgray;\
}")

        self.ui.tabWidget.setTabIcon(0, QtGui.QIcon("icon/tabwidget/point.png"))
        self.ui.tabWidget.setTabIcon(1, QtGui.QIcon("icon/tabwidget/segment.png"))
        self.ui.tabWidget.setTabIcon(2, QtGui.QIcon("icon/tabwidget/circle.png"))
        self.ui.tabWidget.setTabIcon(3, QtGui.QIcon("icon/tabwidget/angle.png"))
        self.ui.tabWidget.setTabIcon(4, QtGui.QIcon("icon/tabwidget/polygon_linestring.png"))
        self.ui.tabWidget.setTabIcon(5, QtGui.QIcon("icon/tabwidget/function.png"))
        self.ui.tabWidget.setTabIcon(6, QtGui.QIcon("icon/tabwidget/clip.png"))
        self.ui.tabWidget.setTabIcon(7, QtGui.QIcon("icon/tabwidget/coordgrid.png"))
        self.ui.tabWidget.setTabIcon(8, QtGui.QIcon("icon/tabwidget/settings.png"))

        add_objects_to_combobox(self)
        self.ui.pt_cb_selector.setCurrentRow(0)
        self.ui.sg_cb_selector.setCurrentRow(0)
        self.ui.crc_cb_selector.setCurrentRow(0)
        self.ui.ang_cb_selector.setCurrentRow(0)
        self.ui.pol_cb_selector.setCurrentRow(0)
        self.ui.fct_cb_selector.setCurrentRow(0)
        fill_fields(self)


        self.ui.tabWidget.currentChanged.connect(self.set_current_id)
        connect_point_gui(self)
        connect_segment_gui(self)
        connect_circle_gui(self)
        connect_angle_gui(self)
        connect_polygon_gui(self)
        connect_function_gui(self)
        connect_axes_gui(self)
        connect_settings_gui(self)


    def set_current_id(self, index):
        """
        SUMMARY
            depending on the current tab and index sets the row in QListWidget and
            fills the fields in the tab

        PARAMETERS
            scene: GraphicsScene
            index: index of newly selected item

        RETURNS
            None
        """
        self.tab_index = index
        if index == 0:
            self.current_id = self.pt_cb_selector.currentRow()
        if index == 1:
            self.current_id = self.sg_cb_selector.currentRow()
        if index == 2:
            self.current_id = self.crc_cb_selector.currentRow()
        if index == 3:
            self.current_id = self.ang_cb_selector.currentRow()
        if index == 4:
            self.current_id = self.pol_cb_selector.currentRow()
        if index == 5:
            self.current_id = self.fct_cb_selector.currentRow()
        if index == 8:
            self.current_id = self.set_cb_selector.currentRow()
        fill_fields(self)

    def hslider_release(self):
        """
        SUMMARY
            protocol when a slider is released: new values are set in the project,
            compile is performed

        PARAMETERS
            scene: GraphicsScene

        RETURNS
            None
        """
        if self.current_id == 0:
            new_value, type, property, secondary_property = self.new_default
            my_object = self.scene.eucl[type][0]
            for i, obj in enumerate(self.scene.eucl[type]):
                if i != 0:
                    if secondary_property is None:
                        if obj[property] == my_object[property]:
                            obj[property] = new_value
                    else:
                        if obj[property][secondary_property] == my_object[property][secondary_property]:
                            obj[property][secondary_property] = new_value
            if secondary_property is None:
                my_object[property] = new_value
            else:
                my_object[property][secondary_property] = new_value

        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.ui.tabWidget.setFocus()

    def hslider_moved(self, value, type, property, label_to_set, factor=1, secondary_property=None):
        """
        SUMMARY
            protocol when a slider is being moved: new values are set in the project,
            slider label updated

        PARAMETERS
            value: value returned by the slider
            type: type of object ("points", "segments", ...)
            property: property of object
            label_to_set: reference of the label widget where the slider value is printed
            factor: used to transforms the range of the slider to more appropriate range
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        my_object = self.scene.eucl[type][self.current_id]
        if self.current_id == 0:
            self.new_default = (value/factor, type, property, secondary_property)
        else:
            if secondary_property is None:
                my_object[property] = value/factor
            else:
                my_object[property][secondary_property] = value/factor
        label_to_set.setText(str(value/factor))

    def pb_default_checked(self, type, default_value, property, slider_to_set, label_to_set, factor=1, secondary_property=None):
        """
        SUMMARY
            protocol when a pressbutton labelled default is pressed,
            compile is performed

        PARAMETERS
            scene: GraphicsScene

        RETURNS
            None
        """
        if secondary_property is None:
            default_value = self.scene.eucl[type][0][property]
            self.scene.eucl[type][self.current_id][property] = default_value
        else:
            default_value = self.scene.eucl[type][0][property][secondary_property]
            self.scene.eucl[type][self.current_id][property][secondary_property] = default_value
        slider_to_set.setValue(default_value * factor)
        label_to_set.setText(str(default_value))
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def le_number_edit(self, type, property, le_box, recompute_mapped_points, secondary_property=None):
        """
        SUMMARY
            protocol when a box is clicked to enter number

        PARAMETERS
            type: type of object ("points", "segments", ...)
            property: property of object
            le_box: reference to the input box
            recompute_mapped_points: if the box is for point x/y coordinate we may
            need to recompute the mapped points, if true it does, not otherwise
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        point = self.scene.eucl[type][self.current_id]
        if not le_box.hasFocus():
            try:
                x = eval(le_box.text())
                if secondary_property is None:
                    point[property] = le_box.text()
                else:
                    point[property][secondary_property] = le_box.text()
                self.scene.compile_tkz_and_render()
                if recompute_mapped_points:
                    self.scene.compute_mapped_points()
                self.scene.add_new_undo_item()
                self.ui.tabWidget.setFocus()
            except:
                if secondary_property is None:
                    le_box.setText("%s" % point[property])
                else:
                    le_box.setText("%s" % point[property][secondary_property])

        else:
            self.ui.tabWidget.setFocus()

    def checkb_state_changed(self, state, type, property, secondary_property=None):
        """
        SUMMARY
            protocol when a checkbox was clicked

        PARAMETERS
            state: state of the checkbox
            type: type of object ("points", "segments", ...)
            property: property of object
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        if secondary_property is None:
            item = self.scene.eucl[type][self.current_id]
            my_property = property
        else:
            my_property = secondary_property
            item = self.scene.eucl[type][self.current_id][property]

        if state == QtCore.Qt.Unchecked and item[my_property] == True:
            if self.current_id == 0:
                for obj in self.scene.eucl[type]:
                    if secondary_property is None:
                        obj[property] = False
                    else:
                        obj[property][secondary_property] = False
            item[my_property] = False
            fill_fields(self)
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        elif state == QtCore.Qt.Checked and item[my_property] == False:
            if self.current_id == 0:
                for obj in self.scene.eucl[type]:
                    if secondary_property is None:
                        obj[property] = True
                    else:
                        obj[property][secondary_property] = True
            item[my_property] = True
            fill_fields(self)
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()

    def cb_selector_current_idx_changed(self, value, type, vlist, property, secondary_property=None):
        """
        SUMMARY
            protocol when a new item was selected in a combobox

        PARAMETERS
            value: index of new item
            type: type of object ("points", "segments", ...)
            vlist: list associated with the combobox
            property: property of object
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        if not self.state_change_ignore:
            my_object = self.scene.eucl[type][self.current_id]
            if self.current_id == 0:
                for i,obj in enumerate(self.scene.eucl[type]):
                    if i != 0:
                        if secondary_property is None:
                            if my_object[property] == obj[property]:
                                obj[property] = vlist[value]
                        else:
                            if my_object[property][secondary_property] == obj[property][secondary_property]:
                                obj[property][secondary_property] = vlist[value]
                if secondary_property is None:
                        my_object[property] = vlist[value]
                else:
                        my_object[property][secondary_property] = vlist[value]

            if secondary_property is None:
                self.scene.eucl[type][self.current_id][property] = vlist[value]
            else:
                self.scene.eucl[type][self.current_id][property][secondary_property] = vlist[value]
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
            fill_fields(self)
            self.ui.tabWidget.setFocus()


    def cb_selector_current_idx_changed_new(self, my_object, last_property, selected_value):
        """
        SUMMARY
            protocol when a new item was selected in a combobox (different version)

        PARAMETERS
            my_object: the object reference to modify this object (must be mutable object)
            last_property: (last) property of the object
            selected_value: the new value (usually passed as an element of a list)

        RETURNS
            None
        """
        if not self.state_change_ignore:
            my_object[last_property] = selected_value
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
            fill_fields(self)
            self.ui.tabWidget.setFocus()

    def hslider_moved_new(self, my_object, last_property, value, label_to_set, factor=1):
        """
        SUMMARY
            protocol when the slider is moved (new version)

        PARAMETERS
            my_object: the object reference to modify this object (must be mutable object)
            last_property: (last) property of the object
            value: value passed by the slider
            label_to_set: reference to the corresponding label
            factor: transforms the sliders range

        RETURNS
            None
        """
        my_object[last_property] = value/factor
        label_to_set.setText(str(value/factor))

    def hslider_release_new(self):
        """
        SUMMARY
            protocol when a slider is released (new version)

        PARAMETERS
            nothing
        RETURNS
            None
        """
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.ui.tabWidget.setFocus()

    def id_selected(self, value):
        """
        SUMMARY
            protocol when the item row is changed in QListWidget,
            fills the fields accordingly

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.current_id = value
        fill_fields(self)

    def pt_le_id_editing_finished(self):
        """
        SUMMARY
            protocol of point id LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        point = self.scene.eucl["points"][self.current_id]
        if not self.ui.pt_le_id.hasFocus():
            try:
                if point["id"] == self.ui.pt_le_id.text():
                    throw_error = 1/0
                if self.ui.pt_le_id.text() == 'default':
                    throw_error = 1/0
                for char in self.ui.pt_le_id.text():
                    if not ('a'<=char<='z' or 'A'<=char<='Z' or char == "'"):
                        throw_error = 1/0
                if Utils.point_change_id(self.scene.eucl, point["id"], self.ui.pt_le_id.text(), self.scene.mapped_points) != False:
                    self.ui.pt_cb_selector.currentItem().setText(self.ui.pt_le_id.text())
                    self.scene.compile_tkz_and_render()
                    self.scene.add_new_undo_item()
                    fill_point_fields(self)
                    add_objects_to_combobox(self)
                else:
                    throw_error = 1/0
            except ZeroDivisionError:
                self.ui.pt_le_id.setText(point["id"])
        else:
            self.ui.tabWidget.setFocus()


    def pt_le_name_editing_finished(self):
        """
        SUMMARY
            protocol of point label text LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        point = self.scene.eucl["points"][self.current_id]
        if not self.ui.pt_le_name.hasFocus():
            try:
                point["label"]["text"] = self.ui.pt_le_name.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.pt_le_name.setText(point["label"]["text"])
        else:
            self.ui.tabWidget.setFocus()

    def ang_le_name_editing_finished(self):
        """
        SUMMARY
            protocol of angle label text LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        angle = self.scene.eucl["angles"][self.current_id]
        if not self.ui.ang_le_name.hasFocus():
            try:
                angle["label"]["text"] = self.ui.ang_le_name.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.ang_le_name.setText(angle["label"]["text"])
        else:
            self.ui.tabWidget.setFocus()

    def sg_le_name_editing_finished(self):
        """
        SUMMARY
            protocol of segment label text LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        point = self.scene.eucl["segments"][self.current_id]
        if not self.ui.sg_le_name.hasFocus():
            try:
                point["label"]["text"] = self.ui.sg_le_name.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.sg_le_name.setText(point["label"]["text"])
        else:
            self.ui.tabWidget.setFocus()

    def crc_le_name_editing_finished(self):
        """
        SUMMARY
            protocol of circle label text LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        circle = self.scene.eucl["circles"][self.current_id]
        if not self.ui.crc_le_name.hasFocus():
            try:
                circle["label"]["text"] = self.ui.crc_le_name.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.crc_le_name.setText(circle["label"]["text"])
        else:
            self.ui.tabWidget.setFocus()

    def pol_le_decoration_text_editing_finished(self):
        """
        SUMMARY
            protocol of polygon decoration text LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        polygon = self.scene.eucl["polygons"][self.current_id]
        if not self.ui.pol_le_decoration_text.hasFocus():
            try:
                polygon["decoration"]["text"] = self.ui.pol_le_decoration_text.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.pol_le_decoration_text.setText(polygon["decoration"]["text"])
        else:
            self.ui.tabWidget.setFocus()

    def fct_le_function_def_text_editing_finished(self):
        """
        SUMMARY
            protocol of function definition text LineEdit when editing is finished

        PARAMETERS
            nothing

        RETURNS
            None
        """
        function = self.scene.eucl["functions"][self.current_id]
        if not self.ui.fct_le_function_def.hasFocus():
            try:
                function["def"] = self.ui.fct_le_function_def.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.fct_le_function_def.setText(function["def"])
        else:
            self.ui.tabWidget.setFocus()


    def le_line_stroke_custom_editing_finished(self, type, label_to_set):
        """
        SUMMARY
            protocol of any custom dash pattern text LineEdit when editing is finished,
            expects even number of integers

        PARAMETERS
            nothing

        RETURNS
            None
        """
        point = self.scene.eucl[type][self.current_id]
        if not label_to_set.hasFocus():
            try:
                lengths = list(map(lambda x: int(x), label_to_set.text().split(' ')))
                if len(lengths) % 2 != 0:
                    throw_error = 1/0
                point["line_stroke_custom"] = lengths
                self.scene.compile_tkz_and_render()
                self.scene.compute_mapped_points()
                self.scene.add_new_undo_item()
            except:
                lengths_str = ''
                for num in point["line_stroke_custom"]:
                    lengths_str += "%s " % str(num)
                lengths_str = lengths_str[:-1]
                label_to_set.setText(lengths_str)
        else:
            self.ui.tabWidget.setFocus()

    def fct_cb_selector_pattern_between_idx_changed(self, index):
        """
        SUMMARY
            protocol of function fill between other function ComboBox when index is changed

        PARAMETERS
            index: new index passed by the signal

        RETURNS
            None
        """
        if not self.state_change_ignore:
            my_object = self.scene.eucl["functions"][self.current_id]
            if index == 0:
                my_object["between"] = -1
            i = 0
            for function in self.scene.eucl["functions"]:
                if function["type"] == 'yfx' and function["id"] != 'fct_default' and function["id"] != my_object["id"]:
                    if i+1 == index:
                        my_object["between"] = function["id"]
                    i += 1
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
            fill_fields(self)
            self.ui.tabWidget.setFocus()

    def axes_checkb(self, state, type, property, secondary_property=None):
        """
        SUMMARY
            protocol of axes CheckButton when state is changed

        PARAMETERS
            state: state of the button
            type: type of object ("points", "segments", ...)
            property: property of object
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        if secondary_property is None:
            item = self.scene.eucl[type]
            my_property = property
        else:
            my_property = secondary_property
            item = self.scene.eucl[type][property]

        if state == QtCore.Qt.Unchecked and item[my_property] == True:
            item[my_property] = False
            fill_fields(self)
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        elif state == QtCore.Qt.Checked and item[my_property] == False:
            item[my_property] = True
            fill_fields(self)
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        self.scene.axis_grid_checkbox_shifter()

    def axe_hslider_moved(self, value, type, property, label_to_set, factor=1, secondary_property=None):
        """
        SUMMARY
            protocol of axes slider when is being moved

        PARAMETERS
            value: value given by the slider
            type: type of object ("points", "segments", ...)
            property: property of object
            label_to_set: reference of the label of the slider
            factor: transforms to range of the slider
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        my_object = self.scene.eucl[type]
        if secondary_property is None:
            my_object[property] = value/factor
        else:
            my_object[property][secondary_property] = value/factor
        label_to_set.setText(str(value/factor))

    def axe_hslider_release(self):
        """
        SUMMARY
            protocol of axes slider when slider is released

        PARAMETERS
            nothing
        RETURNS
            None
        """
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.ui.tabWidget.setFocus()

    def axe_cb_selector_current_idx_changed(self, value, type, vlist, property, secondary_property=None):
        """
        SUMMARY
            protocol of axes ComboBox when index is changed

        PARAMETERS
            value: value given by the ComboBox
            type: type of object ("points", "segments", ...)
            vlist: list with  to choose from
            property: property of object
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        if not self.state_change_ignore:
            my_object = self.scene.eucl[type]
            if secondary_property is None:
                self.scene.eucl[type][property] = vlist[value]
            else:
                self.scene.eucl[type][property][secondary_property] = vlist[value]
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
            fill_fields(self)
            self.ui.tabWidget.setFocus()

    def axe_le_line_stroke_custom_editing_finished(self, type, property, label_to_set):
        """
        SUMMARY
            protocol of axes custom dash text LineEdit when editing is finished

        PARAMETERS
            type: type of object ("points", "segments", ...)
            property: property of object
            label_to_set: reference of the label of the LineEdit

        RETURNS
            None
        """
        point = self.scene.eucl[type]
        if not label_to_set.hasFocus():
            try:
                lengths = list(map(lambda x: int(x), label_to_set.text().split(' ')))
                if len(lengths) % 2 != 0:
                    throw_error = 1/0
                point[property] = lengths
                self.scene.compile_tkz_and_render()
                self.scene.compute_mapped_points()
                self.scene.add_new_undo_item()
            except:
                lengths_str = ''
                for num in point[property]:
                    lengths_str += "%s " % str(num)
                lengths_str = lengths_str[:-1]
                label_to_set.setText(lengths_str)
        else:
            self.ui.tabWidget.setFocus()

    def axe_le_text_editing_finished(self, text_edit, type, property, secondary_property=None):
        """
        SUMMARY
            protocol of axes text LineEdit when editing is finished

        PARAMETERS
            text_edit: reference to TextEdit object
            type: type of object ("points", "segments", ...)
            property: property of object
            secondary_property: if applicable it is a secondary property of the
            item returned by the property

        RETURNS
            None
        """
        if secondary_property is None:
            my_object = self.scene.eucl[type]
            my_property = property
        else:
            my_object = self.scene.eucl[type][property]
            my_property = secondary_property

        if not text_edit.hasFocus():
            try:
                my_object[my_property] = text_edit.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                text_edit.setText(my_object[my_property])
        else:
            self.ui.tabWidget.setFocus()




    def rad_anglo_right_clicked(self):
        """
        SUMMARY
            protocol of angle type Anglo-French right angle RadioButton when clicked

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.eucl["angles"][self.current_id]["right_angle"] = True
        self.scene.eucl["angles"][self.current_id]["type"] = DEFAULT_RIGHT_ANGLE_TYPE
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
    def rad_german_right_clicked(self):
        """
        SUMMARY
            protocol of angle type German right angle RadioButton when clicked

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.eucl["angles"][self.current_id]["right_angle"] = True
        self.scene.eucl["angles"][self.current_id]["type"] = 'german'
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
    def rad_arbitrary_clicked(self):
        """
        SUMMARY
            protocol of angle type arbitrary RadioButton when clicked

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.eucl["angles"][self.current_id]["right_angle"] = False
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def rad_polygon_clicked(self):
        """
        SUMMARY
            protocol of polygon RadioButton when clicked

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.eucl["polygons"][self.current_id]["type"] = 'polygon'
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
    def rad_linestring_clicked(self):
        """
        SUMMARY
            protocol of linestring RadioButton when clicked

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.eucl["polygons"][self.current_id]["type"] = 'linestring'
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def keyPressEvent(self,event):
        """
        SUMMARY
            signal for when a key is pressed in PropertiesDialog

        PARAMETERS
            nothing

        RETURNS
            None
        """
        # if undo is pressed update undo list, redo list, save_state,
        # undo redo save actions
        if event.matches(QtGui.QKeySequence.Undo):
            if len(self.scene.undo_history) > 1:
                self.scene.eucl = deepcopy(self.scene.undo_history[-2])
                self.scene.redo_history.append(self.scene.undo_history.pop())
                self.scene.compile_tkz_and_render()
                self.scene.compute_mapped_points()
                if len(self.scene.undo_history) == 1:
                    self.scene.actionUndo.setEnabled(False)
                self.scene.actionRedo.setEnabled(True)
                fill_fields(self)
                add_objects_to_combobox(self)
                self.scene.save_state = save_state(self.scene.save_state.opened_file, self.scene.save_state.unsaved_progress - 1)
                if self.scene.save_state.unsaved_progress == 0:
                    self.scene.actionSave.setEnabled(False)
                else:
                    self.scene.actionSave.setEnabled(True)
        # if redo is pressed update undo list, redo list, save_state,
        # undo redo save actions
        elif event.matches(QtGui.QKeySequence.Redo):
            if self.scene.redo_history != []:
                self.scene.eucl = deepcopy(self.scene.redo_history[-1])
                self.scene.undo_history.append(self.scene.redo_history.pop())
                self.scene.compile_tkz_and_render()
                self.scene.compute_mapped_points()
                if self.scene.redo_history == []:
                    self.scene.actionRedo.setEnabled(False)
                self.scene.actionUndo.setEnabled(True)
                fill_fields(self)
                add_objects_to_combobox(self)
                self.scene.save_state = save_state(self.scene.save_state.opened_file, self.scene.save_state.unsaved_progress + 1)
                if self.scene.save_state.unsaved_progress == 0:
                    self.scene.actionSave.setEnabled(False)
                else:
                    self.scene.actionSave.setEnabled(True)
        # this performs autocompile when f5 is pressed
        elif event.matches(QtGui.QKeySequence.Refresh):
            # we trick compile_tkz_and_render
            previous_autocompile = self.scene.autocompile
            self.scene.autocompile = True
            self.scene.compile_tkz_and_render()
            self.scene.autocompile = previous_autocompile
        # save
        elif event.matches(QtGui.QKeySequence.Save):
            Utils.save(self)
        # save as
        elif event.matches(QtGui.QKeySequence.SaveAs):
            Utils.save_as(self)
        # delete item
        elif event.matches(QtGui.QKeySequence.Delete):
            if self.tab_index == 0 and self.pt_cb_selector.currentRow() > 0:
                Utils.delete_point(self.scene.eucl, self.pt_cb_selector.currentRow(), self.scene.mapped_points)
                self.current_id = 0
                add_objects_to_combobox(self)
            elif self.tab_index == 1 and self.sg_cb_selector.currentRow() > 0:
                old_currentrow = self.sg_cb_selector.currentRow()
                self.sg_cb_selector.takeItem(self.sg_cb_selector.currentRow())
                if len(self.scene.eucl["segments"]) == 2:
                    del self.scene.eucl["segments"][1]
                else:
                    del self.scene.eucl["segments"][old_currentrow]
                self.current_id = self.sg_cb_selector.currentRow()
            elif self.tab_index == 2 and self.crc_cb_selector.currentRow() > 0:
                old_currentrow = self.crc_cb_selector.currentRow()
                self.crc_cb_selector.takeItem(self.crc_cb_selector.currentRow())
                if len(self.scene.eucl["circles"]) == 2:
                    del self.scene.eucl["circles"][1]
                else:
                    del self.scene.eucl["circles"][old_currentrow]
                self.current_id = self.crc_cb_selector.currentRow()
            elif self.tab_index == 3 and self.ang_cb_selector.currentRow() > 0:
                old_currentrow = self.ang_cb_selector.currentRow()
                self.ang_cb_selector.takeItem(self.ang_cb_selector.currentRow())
                if len(self.scene.eucl["angles"]) == 2:
                    del self.scene.eucl["angles"][1]
                else:
                    del self.scene.eucl["angles"][old_currentrow]
                self.current_id = self.ang_cb_selector.currentRow()
            elif self.tab_index == 4 and self.pol_cb_selector.currentRow() > 0:
                old_currentrow = self.pol_cb_selector.currentRow()
                self.pol_cb_selector.takeItem(self.pol_cb_selector.currentRow())
                if len(self.scene.eucl["polygons"]) == 2:
                    del self.scene.eucl["polygons"][1]
                else:
                    del self.scene.eucl["polygons"][old_currentrow]
                self.current_id = self.pol_cb_selector.currentRow()
            elif self.tab_index == 5 and self.fct_cb_selector.currentRow() > 0:
                old_currentrow = self.fct_cb_selector.currentRow()
                self.fct_cb_selector.takeItem(self.fct_cb_selector.currentRow())
                if len(self.scene.eucl["functions"]) == 2:
                    del self.scene.eucl["functions"][1]
                else:
                    del self.scene.eucl["functions"][old_currentrow]
                self.current_id = self.fct_cb_selector.currentRow()

            self.scene.compile_tkz_and_render()
            print("after compile")
            self.scene.compute_mapped_points()
            fill_fields(self)
            self.scene.add_new_undo_item()
            #add_objects_to_combobox(self)



    def set_le_latex_command_changed(self):
        """
        SUMMARY
            protocol of latex compile command text LineEdit when editing is finished,
            saves the change into file

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.settings["latex"] = self.ui.set_le_latex_command.text()
        with open('settings.json', 'w') as outfile:
            json.dump(self.scene.settings, outfile, indent=4)

    def set_le_pdf_to_jpg_command_changed(self):
        """
        SUMMARY
            protocol of pdf to jpg command text LineEdit when editing is finished,

        PARAMETERS
            nothing

        RETURNS
            None
        """
        self.scene.settings["pdf to jpg"] = self.ui.set_le_pdf_to_jpg_command.text()
        with open('settings.json', 'w') as outfile:
            json.dump(self.scene.settings, outfile, indent=4)

    def set_checkb_aspect_ratio_indicator_changed(self, state):
        """
        SUMMARY
            protocol of aspect ratio CheckButton when indicator changed,

        PARAMETERS
            state: state of the checkbutton

        RETURNS
            None
        """
        if state == QtCore.Qt.Unchecked:
            self.scene.aspect_ratio_indicator = False
        else:
            self.scene.aspect_ratio_indicator = True
        always_on_drawing_plan(self.scene)
        always_off_drawing_plan(self.scene)

    def set_le_aspect_ratio_editingFinished(self):
        """
        SUMMARY
            protocol of aspect ratio number LineEdit when editing is finished,

        PARAMETERS
            nothing

        RETURNS
            None
        """
        try:
            _ = eval(self.ui.set_le_aspect_ratio.text())
            self.scene.aspect_ratio = self.ui.set_le_aspect_ratio.text()
        except:
            self.ui.set_le_aspect_ratio.setText("16/9")
            self.scene.aspect_ratio = "16/9"
        always_on_drawing_plan(self.scene)
        always_off_drawing_plan(self.scene)

    def before_after_textChanged(self, my_object, last_property, text_edit):
        """
        SUMMARY
            protocol of before and/or after code text TextEdit when text is changed,

        PARAMETERS
            myobject: object to be modified (mutable object)
            last_property: last property of object we modify
            text_edit: reference to TextEdit

        RETURNS
            None
        """
        my_object[last_property] = text_edit.toPlainText()

    def set_pb_editingFinished_clicked(self, button):
        """
        SUMMARY
            protocol of before/after PushButton to signify the editing finished,
            and e.g. compile

        PARAMETERS
            button: reference to the PushButton

        RETURNS
            None
        """
        button.setFocus()
        self.scene.compile_tkz_and_render()
        if self.scene.undo_history[-1]["code_before"] == self.scene.eucl["code_before"] or\
        self.scene.undo_history[-1]["code_after"] == self.scene.eucl["code_after"]:
            self.scene.add_new_undo_item()
        always_on_drawing_plan(self.scene)
        always_off_drawing_plan(self.scene)

    def package_list_updated(self, newitem):
        """
        SUMMARY
            protocol of package list ListWidget when an item/row is changed,

        PARAMETERS
            newitem: unused, passed by signal

        RETURNS
            None
        """
        for i in range(self.ui.set_cb_selector.count()):
            self.scene.eucl["packages"][i] = self.ui.set_cb_selector.item(i).text()

    def add_new_package(self):
        """
        SUMMARY
            protocol to add new package,

        PARAMETERS
            nothing

        RETURNS
            None
        """
        selector = self.ui.set_cb_selector
        if selector.item(selector.count() - 1).text() != '':
            item = QtWidgets.QListWidgetItem('')
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            selector.addItem(item)
            selector.editItem(item)
            selector.verticalScrollBar().setValue(selector.verticalScrollBar().maximum())
            if selector.count() > len(self.scene.eucl["packages"]):
                self.scene.eucl["packages"].append('')

    def delete_package(self):
        """
        SUMMARY
            protocol to delete package,

        PARAMETERS
            nothing

        RETURNS
            None
        """
        current_row = self.ui.set_cb_selector.currentRow()
        if current_row > 5:
            self.ui.set_cb_selector.takeItem(current_row)
            del self.scene.eucl["packages"][current_row]


    def open_duck_dialog(self):
        """
        SUMMARY
            opens up the duck dialog,

        PARAMETERS
            nothing

        RETURNS
            None
        """
        dialog = DuckPropertiesDialog(self.scene, self.current_id)
        dialog.setFixedSize(779, 620)
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()
