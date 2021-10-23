"""
contains functions for the color picker dialog
"""

from PyQt5 import QtWidgets, QtGui, uic

from Constants import *


# converts a setup in the dialog to tikz colour code
def colour2tkz(principal_colour, pc_strength, mix_colour, mix_strength, show=None):
    if show is None:
        if principal_colour == 'default':
            return 'default'
        if mix_colour == 'none':
            return '%s!%s' % (principal_colour, pc_strength)
        if mix_colour != 'none':
            return '%s!%s!%s!%s' % (principal_colour, pc_strength, mix_colour, mix_strength)
    else:
        my_bool = 'T-' if show else 'F-'
        if principal_colour == 'default':
            return my_bool + 'default'
        if mix_colour == 'none':
            return my_bool + ('%s!%s' % (principal_colour, pc_strength))
        if mix_colour != 'none':
            return my_bool + ('%s!%s!%s!%s' % (principal_colour, pc_strength, mix_colour, mix_strength))


# a simple parser that does the inverse of `colour2tkz`
def tkz2colour(tkz_str):
    if tkz_str[0] in ['F', 'T']:
        my_bool = True if tkz_str[0] == 'T' else False
        splitted = tkz_str[2:].split('!')
        if len(splitted) == 1:
            return ['default', 100, 'none', 100, my_bool]
        if len(splitted) == 2:
            return [splitted[0], int(splitted[1]), 'none', 100, my_bool]
        if len(splitted) == 4:
            return [splitted[0], int(splitted[1]), splitted[2], int(splitted[3]), my_bool]
    else:
        splitted = tkz_str.split('!')
        if len(splitted) == 1:
            return ['default', 100, 'none', 100]
        if len(splitted) == 2:
            return [splitted[0], int(splitted[1]), 'none', 100]
        if len(splitted) == 4:
            return [splitted[0], int(splitted[1]), splitted[2], int(splitted[3])]



# sets qt objects to their correct state representing the current eucl item
def fill_fields(dialog):
    if dialog.my_object[dialog.property][0] in ['F', 'T']:
        principal_colour, pc_strength, mix_colour, mix_strength, _ = tkz2colour(dialog.my_object[dialog.property])
    else:
        principal_colour, pc_strength, mix_colour, mix_strength = tkz2colour(dialog.my_object[dialog.property])
    dialog.ui.cb_selector_fill_colour_name.setCurrentIndex(PRINCIPAL_COLOURS.index(principal_colour))
    dialog.ui.cb_selector_fill_colour_mix_name.setCurrentIndex(MIX_COLOURS.index(mix_colour))
    dialog.ui.hslider_strength.setValue(pc_strength)
    dialog.ui.label_strength.setText(str(pc_strength))
    dialog.ui.hslider_mix_strength.setValue(mix_strength)
    dialog.ui.label_mix_strength.setText(str(mix_strength))


# the class implementing a colour picker dialog
class ColourDialog(QtWidgets.QDialog):
    def __init__ (self, scene, pt_idx, my_object, property):
        super(ColourDialog, self).__init__ ()
        self.ui = uic.loadUi('layouts/colour_dialog.ui', self)
        self.setWindowTitle("Colour")
        self.scene = scene
        self.pt_idx = pt_idx
        self.my_object = my_object
        self.property = property

        fill_fields(self)

        self.ui.cb_selector_fill_colour_name.currentIndexChanged.connect(
        lambda value : self.cb_selector_principal_current_idx_changed(value, PRINCIPAL_COLOURS, self.my_object, self.property))
        self.ui.cb_selector_fill_colour_mix_name.currentIndexChanged.connect(
        lambda value : self.cb_selector_mix_current_idx_changed(value, MIX_COLOURS, self.my_object, self.property))

        self.ui.hslider_strength.valueChanged.connect(
        lambda value : self.hslider_principal_moved(value, my_object, property, self.ui.label_strength))
        self.ui.hslider_strength.sliderReleased.connect(self.hslider_released)

        self.ui.hslider_mix_strength.valueChanged.connect(
        lambda value : self.hslider_mix_moved(value, my_object, property, self.ui.label_mix_strength))
        self.ui.hslider_mix_strength.sliderReleased.connect(self.hslider_released)

    def keyPressEvent(self,event):
        # performs autocompile when f5 is pressed
        if event.matches(QtGui.QKeySequence.Refresh):
            previous_autocompile = self.scene.autocompile
            self.scene.autocompile = True
            self.scene.compile_tkz_and_render()
            self.scene.autocompile = previous_autocompile


    def cb_selector_principal_current_idx_changed(self, value, vlist, my_object, property):
        vector = tkz2colour(self.my_object[self.property])
        vector[0] = vlist[value]
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                if len(vector) == 4:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
                else:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        else:
            if len(vector) == 4:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
            else:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        fill_fields(self)

    def cb_selector_mix_current_idx_changed(self, value, vlist, my_object, property):
        vector = tkz2colour(self.my_object[self.property])
        vector[2] = vlist[value]
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                if len(vector) == 4:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
                else:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        else:
            if len(vector) == 4:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
            else:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        fill_fields(self)

    def hslider_principal_moved(self, value, my_object, property, label_to_set):
        vector = tkz2colour(self.my_object[self.property])
        vector[1] = value
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                if len(vector) == 4:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
                else:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        else:
            if len(vector) == 4:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
            else:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        label_to_set.setText('%d' % (value))

    def hslider_mix_moved(self, value, my_object, property, label_to_set):
        vector = tkz2colour(self.my_object[self.property])
        vector[3] = value
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                if len(vector) == 4:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
                else:
                    point["duck"][self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        else:
            if len(vector) == 4:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3])
            else:
                self.my_object[self.property] = colour2tkz(vector[0], vector[1], vector[2], vector[3], vector[4])
        label_to_set.setText('%d' % (value))

    def hslider_released(self):
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
