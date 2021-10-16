"""
this file contains the definition of the qui window for the property
settings for ducks
"""

from PyQt5 import QtCore, QtWidgets, QtGui, uic
import sys, os, time
from copy import deepcopy
import son_of_j as soj
import colour
from constants import *


#fill QT interface with the correct values
def fill_fields(dialog):
    point = dialog.scene.eucl["points"][dialog.pt_idx]
    if point["duck"]["show"] == True:
        dialog.ui.duck_show.setChecked(True)
    else:
        dialog.ui.duck_show.setChecked(False)
    if point["duck"]["type"] == 'random':
        dialog.all_group_enabled_disabled(False)
        dialog.ui.body_group.setEnabled(True)
        dialog.checkb_enabled_disabled(False)
        dialog.ui.rad_random.setChecked(True)
    if point["duck"]["type"] == 'special':
        dialog.all_group_enabled_disabled(False)
        dialog.ui.special_group.setEnabled(True)
        dialog.ui.body_group.setEnabled(True)
        dialog.checkb_enabled_disabled(False)
        dialog.ui.rad_special.setChecked(True)
    if point["duck"]["type"] == 'custom':
        dialog.all_group_enabled_disabled(True)
        dialog.ui.special_group.setEnabled(False)
        dialog.ui.chess_group.setEnabled(False)
        dialog.checkb_enabled_disabled(True)
        dialog.checkb_checked()
        dialog.ui.rad_custom.setChecked(True)
    if point["duck"]["type"] == 'chess':
        dialog.all_group_enabled_disabled(False)
        dialog.ui.chess_group.setEnabled(True)
        dialog.ui.body_group.setEnabled(True)
        dialog.checkb_enabled_disabled(False)
        dialog.ui.rad_chess.setChecked(True)

    if dialog.pt_idx == 0:
        dialog.all_group_enabled_disabled(False)
        dialog.ui.body_group.setEnabled(True)
        dialog.checkb_enabled_disabled(False)

    dialog.ui.special_combo.setCurrentIndex(DUCK_SPECIAL.index(point["duck"]["special"]))
    dialog.ui.chess_combo.setCurrentIndex(DUCK_CHESS.index(point["duck"]["chess"]))

    dialog.ui.bill_combo.setCurrentIndex(DUCK_BILLS.index(point["duck"]["bill"]))
    dialog.ui.hair_combo.setCurrentIndex(DUCK_HAIRS.index(point["duck"]["hair"]))
    dialog.ui.glasses_combo.setCurrentIndex(DUCK_GLASSESS.index(point["duck"]["glasses"]))
    dialog.ui.hat_combo.setCurrentIndex(DUCK_HATS.index(point["duck"]["hat"]))
    dialog.ui.necklace_combo.setCurrentIndex(DUCK_NECKLACES.index(point["duck"]["necklace"]))
    dialog.ui.accessories_combo.setCurrentIndex(DUCK_ACCESSORIES.index(point["duck"]["accessories"]))
    dialog.ui.bubble_combo.setCurrentIndex(DUCK_SPEECH.index(point["duck"]["thought"]))

    dialog.ui.size_hslider.setValue(point["duck"]["size"]*10)
    dialog.ui.size_label.setText(str(point["duck"]["size"]))

    dialog.ui.le_bubble_text.setText(point["duck"]["thought_text"])
    dialog.ui.le_signpost_text.setText(point["duck"]["accessories_text"])


    duck = point["duck"]

    if not duck["clothing"]["show"]:
        dialog.ui.duck_clothing.setChecked(False)
    else:
        dialog.ui.duck_clothing.setChecked(True)
    if duck["water"][0] == 'F':
        dialog.ui.duck_water.setChecked(False)
    else:
        dialog.ui.duck_water.setChecked(True)
    if duck["eyebrows"][0] == 'F':
        dialog.ui.duck_eyebrows.setChecked(False)
    else:
        dialog.ui.duck_eyebrows.setChecked(True)
    if duck["beard"][0] == 'F':
        dialog.ui.duck_beard.setChecked(False)
    else:
        dialog.ui.duck_beard.setChecked(True)
    if duck["buttons"][0] == 'F':
        dialog.ui.duck_buttons.setChecked(False)
    else:
        dialog.ui.duck_buttons.setChecked(True)
    if duck["lapel"][0] == 'F':
        dialog.ui.duck_lapel.setChecked(False)
    else:
        dialog.ui.duck_lapel.setChecked(True)
    if duck["horsetail"][0] == 'F':
        dialog.ui.duck_horse_tail.setChecked(False)
    else:
        dialog.ui.duck_horse_tail.setChecked(True)


    if duck["clothing"]["tshirt"][0] == 'F':
        dialog.ui.duck_tshirt.setChecked(False)
    else:
        dialog.ui.duck_tshirt.setChecked(True)
    if duck["clothing"]["jacket"][0] == 'F':
        dialog.ui.duck_jacket.setChecked(False)
    else:
        dialog.ui.duck_jacket.setChecked(True)
    if duck["clothing"]["tie"][0] == 'F':
        dialog.ui.duck_tie.setChecked(False)
    else:
        dialog.ui.duck_tie.setChecked(True)
    if duck["clothing"]["bowtie"][0] == 'F':
        dialog.ui.duck_bowtie.setChecked(False)
    else:
        dialog.ui.duck_bowtie.setChecked(True)
    if duck["clothing"]["aodai"][0] == 'F':
        dialog.ui.duck_aodai.setChecked(False)
    else:
        dialog.ui.duck_aodai.setChecked(True)
    if duck["clothing"]["cape"][0] == 'F':
        dialog.ui.duck_cape.setChecked(False)
    else:
        dialog.ui.duck_cape.setChecked(True)

    if dialog.ui.accessories_combo.currentIndex() in [2, 3]:
        dialog.ui.le_signpost_text.setEnabled(True)
        dialog.ui.label_signpost.setEnabled(True)
    else:
        dialog.ui.le_signpost_text.setEnabled(False)
        dialog.ui.label_signpost.setEnabled(False)

    if duck["accessories"] in DUCK_EXTRA:
        dialog.ui.label_accessories_extra.setEnabled(True)
        dialog.ui.pb_accessories_extra.setEnabled(True)
        dialog.ui.label_accessories_extra.setText('extra   ' + DUCK_EXTRA[duck["accessories"]])
    else:
        dialog.ui.label_accessories_extra.setEnabled(False)
        dialog.ui.pb_accessories_extra.setEnabled(False)
        dialog.ui.label_accessories_extra.setText('extra')

    if duck["hat"] in DUCK_EXTRA:
        dialog.ui.label_hat_extra.setEnabled(True)
        dialog.ui.pb_hat_extra.setEnabled(True)
        dialog.ui.label_hat_extra.setText('extra   ' + DUCK_EXTRA[duck["hat"]])
    else:
        dialog.ui.label_hat_extra.setEnabled(False)
        dialog.ui.pb_hat_extra.setEnabled(False)
        dialog.ui.label_hat_extra.setText('extra')






# class for the duck window
class DuckPropertiesDialog(QtWidgets.QDialog):
    def __init__ (self, scene, pt_idx):
        super(DuckPropertiesDialog, self).__init__ ()
        self.ui = uic.loadUi('layouts/duck_dialog.ui', self)
        self.setWindowTitle("Duck properties")
        self.scene = scene
        self.pt_idx = pt_idx

        fill_fields(self)
        duck = self.scene.eucl["points"][self.pt_idx]["duck"]

        self.ui.duck_show.stateChanged.connect(
        lambda state: self.checkb_state_changed(state, duck, "show"))

        self.ui.rad_random.clicked.connect(self.rad_random_clicked)
        self.ui.rad_special.clicked.connect(self.rad_special_clicked)
        self.ui.rad_custom.clicked.connect(self.rad_custom_clicked)
        self.ui.rad_chess.clicked.connect(self.rad_chess_clicked)
        self.ui.special_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_SPECIAL, duck, "special"))
        self.ui.chess_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_CHESS, duck, "chess"))
        self.ui.bill_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_BILLS, duck, "bill"))
        self.ui.hair_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_HAIRS, duck, "hair"))
        self.ui.glasses_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_GLASSESS, duck, "glasses"))
        self.ui.hat_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_HATS, duck, "hat"))
        self.ui.necklace_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_NECKLACES, duck, "necklace"))
        self.ui.accessories_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_ACCESSORIES, duck, "accessories"))

        self.ui.duck_clothing.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "show"))
        self.ui.duck_water.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck, "water"))
        self.ui.duck_eyebrows.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck, "eyebrows"))
        self.ui.duck_beard.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck, "beard"))
        self.ui.duck_buttons.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck, "buttons"))
        self.ui.duck_lapel.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck, "lapel"))
        self.ui.duck_horse_tail.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck, "horsetail"))
        self.ui.duck_tshirt.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "tshirt"))
        self.ui.duck_jacket.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "jacket"))
        self.ui.duck_tie.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "tie"))
        self.ui.duck_bowtie.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "bowtie"))
        self.ui.duck_aodai.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "aodai"))
        self.ui.duck_cape.stateChanged.connect(
        lambda state : self.checkb_state_changed(state, duck["clothing"], "cape"))

        self.ui.size_hslider.valueChanged.connect(
        lambda value : self.hslider_moved(value, duck, "size", self.ui.size_label, 10))
        self.ui.size_hslider.sliderReleased.connect(self.hslider_released)

        self.ui.pb_bill.clicked.connect(
        lambda : self.colour_open(duck, "bill_colour"))
        self.ui.pb_hair.clicked.connect(
        lambda : self.colour_open(duck, "hair_colour"))
        self.ui.pb_glasses.clicked.connect(
        lambda : self.colour_open(duck, "glasses_colour"))
        self.ui.pb_hat.clicked.connect(
        lambda : self.colour_open(duck, "hat_colour"))
        self.ui.pb_hat_extra.clicked.connect(
        lambda : self.colour_open(duck, "hat_extra_colour"))
        self.ui.pb_accessories.clicked.connect(
        lambda : self.colour_open(duck, "accessories_colour"))
        self.ui.pb_accessories_extra.clicked.connect(
        lambda : self.colour_open(duck, "accessories_extra_colour"))
        self.ui.pb_necklace.clicked.connect(
        lambda : self.colour_open(duck, "necklace_colour"))
        self.ui.pb_body.clicked.connect(
        lambda : self.colour_open(duck, "body_colour"))
        self.ui.pb_tshirt.clicked.connect(
        lambda : self.colour_open(duck["clothing"], "tshirt"))
        self.ui.pb_jacket.clicked.connect(
        lambda : self.colour_open(duck["clothing"], "jacket"))
        self.ui.pb_tie.clicked.connect(
        lambda : self.colour_open(duck["clothing"], "tie"))
        self.ui.pb_bowtie.clicked.connect(
        lambda : self.colour_open(duck["clothing"], "bowtie"))
        self.ui.pb_aodai.clicked.connect(
        lambda : self.colour_open(duck["clothing"], "aodai"))
        self.ui.pb_cape.clicked.connect(
        lambda : self.colour_open(duck["clothing"], "cape"))
        self.ui.pb_water.clicked.connect(
        lambda : self.colour_open(duck, "water"))
        self.ui.pb_eyebrows.clicked.connect(
        lambda : self.colour_open(duck, "eyebrows"))
        self.ui.pb_beard.clicked.connect(
        lambda : self.colour_open(duck, "beard"))
        self.ui.pb_buttons.clicked.connect(
        lambda : self.colour_open(duck, "buttons"))
        self.ui.pb_lapel.clicked.connect(
        lambda : self.colour_open(duck, "lapel"))
        self.ui.pb_horse_tail.clicked.connect(
        lambda : self.colour_open(duck, "horsetail"))
        self.ui.pb_bubble.clicked.connect(
        lambda : self.colour_open(duck, "thought_colour"))

        self.ui.le_signpost_text.editingFinished.connect(self.le_signpost_text_editing_finished)
        self.ui.le_bubble_text.editingFinished.connect(self.le_bubble_text_editing_finished)

        self.ui.bubble_combo.currentIndexChanged.connect(
        lambda value : self.cb_selector_current_idx_changed(value, DUCK_SPEECH, duck, "thought"))

    def keyPressEvent(self,event):
        # performs autocompile when f5 is pressed
        if event.matches(QtGui.QKeySequence.Refresh):
            previous_autocompile = self.scene.autocompile
            self.scene.autocompile = True
            self.scene.compile_tkz_and_render()
            self.scene.autocompile = previous_autocompile
        elif event.matches(QtGui.QKeySequence.Save):
            soj.save_eucl_file('data.json', self.scene.eucl)



    def checkb_state_changed(self, state, my_object, property):
        if state == QtCore.Qt.Unchecked:
            if self.pt_idx == 0 and property == 'show':
                for point in self.scene.eucl["points"]:
                    point["duck"]["show"] = False
            if property in ["water", "eyebrows", "beard", "buttons", "lapel", "horsetail",\
                            "tshirt", "jacket", "tie", "bowtie", "aodai", "cape"]:
                my_object[property] = 'F' + my_object[property][1:]
            else:
                my_object[property] = False
            fill_fields(self)
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        elif state == QtCore.Qt.Checked:
            if self.pt_idx == 0 and property == 'show':
                for point in self.scene.eucl["points"]:
                    point["duck"]["show"] = True
            if property in ["water", "eyebrows", "beard", "buttons", "lapel", "horsetail",\
                            "tshirt", "jacket", "tie", "bowtie", "aodai", "cape"]:
                my_object[property] = 'T' + my_object[property][1:]
            else:
                my_object[property] = True
            fill_fields(self)
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()

    def rad_random_clicked(self):
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                point["duck"]["type"] = 'random'
        self.scene.eucl["points"][self.pt_idx]["duck"]["type"] = 'random'
        fill_fields(self)
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()


    def rad_special_clicked(self):
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                point["duck"]["type"] = 'special'
        self.scene.eucl["points"][self.pt_idx]["duck"]["type"] = 'special'
        fill_fields(self)
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def rad_chess_clicked(self):
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                point["duck"]["type"] = 'chess'
        self.scene.eucl["points"][self.pt_idx]["duck"]["type"] = 'chess'
        fill_fields(self)
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def rad_custom_clicked(self):
        if self.pt_idx == 0:
            for point in self.scene.eucl["points"]:
                point["duck"]["type"] = 'custom'
        self.scene.eucl["points"][self.pt_idx]["duck"]["type"] = 'custom'
        fill_fields(self)
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def checkb_checked(self):
        duck = self.scene.eucl["points"][self.pt_idx]["duck"]
        if not duck["clothing"]["show"]:
            self.ui.clothing_group.setEnabled(False)
        else:
            self.ui.clothing_group.setEnabled(True)
        if duck["water"][0] == 'F':
            self.ui.water_group.setEnabled(False)
        else:
            self.ui.water_group.setEnabled(True)
        if duck["eyebrows"][0] == 'F':
            self.ui.eyebrows_group.setEnabled(False)
        else:
            self.ui.eyebrows_group.setEnabled(True)
        if duck["beard"][0] == 'F':
            self.ui.beard_group.setEnabled(False)
        else:
            self.ui.beard_group.setEnabled(True)
        if duck["buttons"][0] == 'F':
            self.ui.buttons_group.setEnabled(False)
        else:
            self.ui.buttons_group.setEnabled(True)
        if duck["lapel"][0] == 'F':
            self.ui.lapel_group.setEnabled(False)
        else:
            self.ui.lapel_group.setEnabled(True)

        if duck["horsetail"][0] == 'F':
            self.ui.horse_tail_group.setEnabled(False)
        else:
            self.ui.horse_tail_group.setEnabled(True)

    def checkb_enabled_disabled(self, boolean):
        self.ui.duck_clothing.setEnabled(boolean)
        self.ui.duck_water.setEnabled(boolean)
        self.ui.duck_eyebrows.setEnabled(boolean)
        self.ui.duck_beard.setEnabled(boolean)
        self.ui.duck_buttons.setEnabled(boolean)
        self.ui.duck_lapel.setEnabled(boolean)
        self.ui.duck_horse_tail.setEnabled(boolean)

    def all_group_enabled_disabled(self, boolean):
        self.ui.bill_group.setEnabled(boolean)
        self.ui.hair_group.setEnabled(boolean)
        self.ui.glasses_group.setEnabled(boolean)
        self.ui.clothing_group.setEnabled(boolean)
        self.ui.water_group.setEnabled(boolean)
        self.ui.eyebrows_group.setEnabled(boolean)
        self.ui.beard_group.setEnabled(boolean)
        self.ui.buttons_group.setEnabled(boolean)
        self.ui.lapel_group.setEnabled(boolean)
        self.ui.horse_tail_group.setEnabled(boolean)
        self.ui.necklace_group.setEnabled(boolean)
        self.ui.hat_group.setEnabled(boolean)
        self.ui.accessories_group.setEnabled(boolean)
        self.ui.special_group.setEnabled(boolean)
        self.ui.chess_group.setEnabled(boolean)
        self.ui.thought_group.setEnabled(boolean)
        self.ui.body_group.setEnabled(boolean)

    def cb_selector_current_idx_changed(self, value, vlist, my_object, property):
        my_object[property] = vlist[value]
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        fill_fields(self)

    def hslider_moved(self, value, my_object, property, label_to_set, factor=1):
        if self.pt_idx == 0 and property == 'size':
            for point in self.scene.eucl["points"]:
                point["duck"]["size"] = value/factor
        my_object[property] = value/factor
        label_to_set.setText('%2.2f' % (value/factor))

    def hslider_released(self):
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def le_signpost_text_editing_finished(self):
        duck = self.scene.eucl["points"][self.pt_idx]["duck"]
        if not self.ui.le_signpost_text.hasFocus():
            try:
                duck["accessories_text"] = self.ui.le_signpost_text.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.le_signpost_text.setText(duck["accessories_text"])
        else:
            self.ui.duck_show.setFocus()

    def le_bubble_text_editing_finished(self):
        duck = self.scene.eucl["points"][self.pt_idx]["duck"]
        if not self.ui.le_bubble_text.hasFocus():
            try:
                duck["thought_text"] = self.ui.le_bubble_text.text()
                self.scene.compile_tkz_and_render()
                self.scene.add_new_undo_item()
            except:
                self.ui.le_bubble_text.setText(duck["thought_text"])
        else:
            self.ui.duck_show.setFocus()

    def colour_open(self, my_object, property):
        dialog_colour = colour.ColourDialog(self.scene, self.pt_idx, my_object, property)
        dialog_colour.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog_colour.exec_()


#
