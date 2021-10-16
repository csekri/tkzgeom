"""
this file contains the definition of the qui window for the property
settings for for various objects and other settings
"""


from PyQt5 import QtCore, QtWidgets, QtGui, uic
import sys, os, time, json
from copy import deepcopy
import numpy as np
from canvas_drawing import always_on_drawing_plan, always_off_drawing_plan

import son_of_j as soj
import duck_properties
from constants import *


current_id = 0

def connect_point_gui(self):
    self.ui.pt_cb_selector.currentRowChanged.connect(self.id_selected)

    self.ui.pt_hslider_size.valueChanged.connect(\
    lambda value : self.hslider_moved(value, "points", "size", self.ui.pt_label_size, 2))
    self.ui.pt_hslider_size.sliderReleased.connect(self.hslider_release)
    self.ui.pt_pb_default_size.clicked.connect(
    lambda : self.pb_default_checked("points", DEFAULT_POINT_SIZE,\
    "size", self.ui.pt_hslider_size, self.ui.pt_label_size, 2))

    self.ui.pt_checkb_show_label.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "points", "label", "show"))
    self.ui.pt_checkb_show_point.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "points", "show"))

    self.ui.pt_le_id.editingFinished.connect(self.pt_le_id_editing_finished)

    self.ui.pt_le_x.editingFinished.connect(
    lambda : self.le_number_edit("points", "x", self.ui.pt_le_x, True))
    self.ui.pt_le_y.editingFinished.connect(
    lambda : self.le_number_edit("points", "y", self.ui.pt_le_y, True))
    self.ui.pt_le_name.editingFinished.connect(self.pt_le_name_editing_finished)

    self.ui.pt_hslider_line_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "line_width", self.ui.pt_label_line_width, 5))
    self.ui.pt_hslider_line_width.sliderReleased.connect(self.hslider_release)
    self.ui.pt_pb_default_line_width.clicked.connect(
    lambda : self.pb_default_checked("points", DEFAULT_POINT_LINE_WIDTH,\
    "line_width", self.ui.pt_hslider_line_width, self.ui.pt_label_line_width, 5))

    self.ui.pt_hslider_label_angle.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "label", self.ui.pt_label_label_angle, 1, "angle"))
    self.ui.pt_hslider_label_angle.sliderReleased.connect(self.hslider_release)
    self.ui.pt_pb_default_label_angle.clicked.connect(
    lambda : self.pb_default_checked("points", DEFAULT_POINT_LABEL_ANGLE,\
    "label", self.ui.pt_hslider_label_angle, self.ui.pt_label_label_angle, 1, "angle"))

    self.ui.pt_hslider_label_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "label", self.ui.pt_label_label_distance, 100, "distance"))
    self.ui.pt_hslider_label_distance.sliderReleased.connect(self.hslider_release)
    self.ui.pt_pb_default_label_distance.clicked.connect(
    lambda : self.pb_default_checked("points", DEFAULT_POINT_LABEL_DISTANCE,\
    "label", self.ui.pt_hslider_label_distance, self.ui.pt_label_label_distance, 100, "distance"))

    self.ui.pt_cb_selector_label_anchor.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "points", DIRECTIONS, "label", "anchor"))

    self.ui.pt_cb_selector_fill_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "points", COLOURS, "fill_colour_name"))
    self.ui.pt_hslider_fill_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "fill_strength", self.ui.pt_label_fill_strength, 1))
    self.ui.pt_hslider_fill_strength.sliderReleased.connect(self.hslider_release)
    self.ui.pt_hslider_fill_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "fill_opacity", self.ui.pt_label_fill_opacity, 100))
    self.ui.pt_hslider_fill_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.pt_cb_selector_line_stroke.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "points", LINE_STROKES, "line_stroke"))
    self.ui.pt_le_line_stroke_custom.editingFinished.connect(
    lambda : self.le_line_stroke_custom_editing_finished("points", self.ui.pt_le_line_stroke_custom))

    self.ui.pt_cb_selector_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "points", COLOURS, "line_colour_name"))
    self.ui.pt_hslider_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "line_strength", self.ui.pt_label_line_strength, 1))
    self.ui.pt_hslider_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.pt_hslider_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "points", "line_opacity", self.ui.pt_label_line_opacity, 100))
    self.ui.pt_hslider_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.pt_pb_duck.clicked.connect(self.open_duck_dialog)

    self.ui.pt_le_line_ratio.editingFinished.connect(
    lambda : self.le_number_edit("points", "from", self.ui.pt_le_line_ratio, True, "ratio"))

    self.ui.pt_le_circle_angle.editingFinished.connect(
    lambda : self.le_number_edit("points", "from", self.ui.pt_le_circle_angle, True, "angle"))

    self.ui.pt_le_line_rotation_angle.editingFinished.connect(
    lambda : self.le_number_edit("points", "from", self.ui.pt_le_line_rotation_angle, True, "angle"))


def connect_segment_gui(self):
    self.ui.sg_cb_selector.currentRowChanged.connect(self.id_selected)
    self.ui.sg_checkb_show_segment.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "segments", "show"))
    self.ui.sg_checkb_show_label.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "segments", "label", "show"))
    self.ui.sg_cb_selector_line_stroke.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", LINE_STROKES, "line_stroke"))
    self.ui.sg_hslider_line_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "line_width", self.ui.sg_label_line_width, 5))
    self.ui.sg_hslider_line_width.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_line_width.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_LINE_WIDTH,\
    "line_width", self.ui.sg_hslider_line_width, self.ui.sg_label_line_width, 5))
    self.ui.sg_le_line_stroke_custom.editingFinished.connect(
    lambda : self.le_line_stroke_custom_editing_finished("segments", self.ui.sg_le_line_stroke_custom))
    self.ui.sg_le_name.editingFinished.connect(self.sg_le_name_editing_finished)
    self.ui.sg_cb_selector_label_anchor.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", DIRECTIONS, "label", "anchor"))

    self.ui.sg_hslider_label_position.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "label", self.ui.sg_label_label_position, 100, "position"))
    self.ui.sg_hslider_label_position.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_label_position.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_LABEL_POSITION,\
    "label", self.ui.sg_hslider_label_position, self.ui.sg_label_label_position, 100, "position"))

    self.ui.sg_hslider_label_angle.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "label", self.ui.sg_label_label_angle, 1, "angle"))
    self.ui.sg_hslider_label_angle.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_label_angle.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_LABEL_ANGLE,\
    "label", self.ui.sg_hslider_label_angle, self.ui.sg_label_label_angle, 1, "angle"))

    self.ui.sg_hslider_label_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "label", self.ui.sg_label_label_distance, 100, "distance"))
    self.ui.sg_hslider_label_distance.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_label_distance.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_LABEL_DISTANCE,\
    "label", self.ui.sg_hslider_label_distance, self.ui.sg_label_label_distance, 100, "distance"))

    self.ui.sg_cb_selector_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", COLOURS, "line_colour_name"))
    self.ui.sg_hslider_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "line_strength", self.ui.sg_label_line_strength, 1))
    self.ui.sg_hslider_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.sg_hslider_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "line_opacity", self.ui.sg_label_line_opacity, 100))
    self.ui.sg_hslider_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.sg_cb_selector_o_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.sg_hslider_o_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "o_arrow", self.ui.sg_label_o_arrow_length, 4, "length"))
    self.ui.sg_hslider_o_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.sg_hslider_o_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "o_arrow", self.ui.sg_label_o_arrow_width, 4, "width"))
    self.ui.sg_hslider_o_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.sg_cb_selector_o_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", ARROW_SIDES, "o_arrow", "side"))
    self.ui.sg_checkb_o_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "segments", "o_arrow", "reversed"))

    self.ui.sg_cb_selector_d_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", ARROW_TIPS, "d_arrow", "tip"))
    self.ui.sg_hslider_d_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "d_arrow", self.ui.sg_label_d_arrow_length, 4, "length"))
    self.ui.sg_hslider_d_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.sg_hslider_d_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "d_arrow", self.ui.sg_label_d_arrow_width, 4, "width"))
    self.ui.sg_hslider_d_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.sg_cb_selector_d_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", ARROW_SIDES, "d_arrow", "side"))
    self.ui.sg_checkb_d_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "segments", "d_arrow", "reversed"))

    self.ui.sg_hslider_mark_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "mark", self.ui.sg_label_mark_width, 5, "width"))
    self.ui.sg_hslider_mark_width.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_mark_width.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_MARK_WIDTH,\
    "mark", self.ui.sg_hslider_mark_width, self.ui.sg_label_mark_width, 4, "width"))
    self.ui.sg_hslider_mark_size.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "mark", self.ui.sg_label_mark_size, 2, "size"))
    self.ui.sg_hslider_mark_size.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_mark_size.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_MARK_SIZE,\
    "mark", self.ui.sg_hslider_mark_size, self.ui.sg_label_mark_size, 2, "size"))
    self.ui.sg_hslider_mark_position.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "mark", self.ui.sg_label_mark_position, 16, "position"))
    self.ui.sg_hslider_mark_position.sliderReleased.connect(self.hslider_release)
    self.ui.sg_pb_default_mark_position.clicked.connect(
    lambda : self.pb_default_checked("segments", DEFAULT_SEGMENT_MARK_POSITION,\
    "mark", self.ui.sg_hslider_mark_position, self.ui.sg_label_mark_position, 16, "position"))
    self.ui.sg_cb_selector_mark_symbol.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", SEGMENT_MARKERS, "mark", "symbol"))
    self.ui.sg_cb_selector_mark_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "segments", MARKER_COLOURS, "mark", "colour"))

    self.ui.sg_hslider_ext_o.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "extension", self.ui.sg_label_ext_o, 16, "origin"))
    self.ui.sg_hslider_ext_o.sliderReleased.connect(self.hslider_release)
    self.ui.sg_hslider_ext_d.valueChanged.connect(
    lambda value : self.hslider_moved(value, "segments", "extension", self.ui.sg_label_ext_d, 16, "destination"))
    self.ui.sg_hslider_ext_d.sliderReleased.connect(self.hslider_release)


def connect_circle_gui(self):
    self.ui.crc_cb_selector.currentRowChanged.connect(self.id_selected)
    self.ui.crc_checkb_show_circle.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "circles", "show"))
    self.ui.crc_checkb_show_label.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "circles", "label", "show"))
    self.ui.crc_hslider_line_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "line_width", self.ui.crc_label_line_width, 5))
    self.ui.crc_hslider_line_width.sliderReleased.connect(self.hslider_release)
    self.ui.crc_pb_default_line_width.clicked.connect(
    lambda : self.pb_default_checked("circles", DEFAULT_SEGMENT_LINE_WIDTH,\
    "line_width", self.ui.crc_hslider_line_width, self.ui.crc_label_line_width, 5))

    self.ui.crc_le_line_stroke_custom.editingFinished.connect(
    lambda : self.le_line_stroke_custom_editing_finished("circles", self.ui.crc_le_line_stroke_custom))
    self.ui.crc_cb_selector_line_stroke.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", LINE_STROKES, "line_stroke"))


    self.ui.crc_le_name.editingFinished.connect(self.crc_le_name_editing_finished)
    self.ui.crc_cb_selector_label_anchor.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", DIRECTIONS, "label", "anchor"))

    self.ui.crc_hslider_label_angle.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "label", self.ui.crc_label_label_angle, 1, "angle"))
    self.ui.crc_hslider_label_angle.sliderReleased.connect(self.hslider_release)
    self.ui.crc_pb_default_label_angle.clicked.connect(
    lambda : self.pb_default_checked("circles", DEFAULT_SEGMENT_LABEL_ANGLE,\
    "label", self.ui.crc_hslider_label_angle, self.ui.crc_label_label_angle, 1, "angle"))

    self.ui.crc_hslider_label_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "label", self.ui.crc_label_label_distance, 10, "distance"))
    self.ui.crc_hslider_label_distance.sliderReleased.connect(self.hslider_release)
    self.ui.crc_pb_default_label_distance.clicked.connect(
    lambda : self.pb_default_checked("circles", DEFAULT_CIRCLE_LABEL_DISTANCE,\
    "label", self.ui.crc_hslider_label_distance, self.ui.crc_label_label_distance, 10, "distance"))


    self.ui.crc_cb_selector_pattern_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", PATTERN_TYPES, "pattern", "type"))

    self.ui.crc_hslider_pattern_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "pattern", self.ui.crc_label_pattern_distance, 2, "distance"))
    self.ui.crc_hslider_pattern_distance.sliderReleased.connect(self.hslider_release)
    self.ui.crc_pb_default_pattern_distance.clicked.connect(
    lambda : self.pb_default_checked("circles", DEFAULT_PATTERN_DISTANCE,\
    "pattern", self.ui.crc_hslider_pattern_distance, self.ui.crc_label_pattern_distance, 2, "distance"))

    self.ui.crc_hslider_pattern_size.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "pattern", self.ui.crc_label_pattern_size, 5, "size"))
    self.ui.crc_hslider_pattern_size.sliderReleased.connect(self.hslider_release)
    self.ui.crc_pb_default_pattern_size.clicked.connect(
    lambda : self.pb_default_checked("circles", DEFAULT_PATTERN_SIZE,\
    "pattern", self.ui.crc_hslider_pattern_size, self.ui.crc_label_pattern_size, 5, "size"))

    self.ui.crc_hslider_pattern_rotation.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "pattern", self.ui.crc_label_pattern_rotation, 1, "rotation"))
    self.ui.crc_hslider_pattern_rotation.sliderReleased.connect(self.hslider_release)
    self.ui.crc_pb_default_pattern_rotation.clicked.connect(
    lambda : self.pb_default_checked("circles", DEFAULT_PATTERN_ROTATION,\
    "pattern", self.ui.crc_hslider_pattern_rotation, self.ui.crc_label_pattern_rotation, 1, "rotation"))

    self.ui.crc_hslider_pattern_xshift.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "pattern", self.ui.crc_label_pattern_xshift, 2, "xshift"))
    self.ui.crc_hslider_pattern_xshift.sliderReleased.connect(self.hslider_release)

    self.ui.crc_hslider_pattern_yshift.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "pattern", self.ui.crc_label_pattern_yshift, 2, "yshift"))
    self.ui.crc_hslider_pattern_yshift.sliderReleased.connect(self.hslider_release)

    self.ui.crc_cb_selector_fill_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", COLOURS, "fill_colour_name"))
    self.ui.crc_hslider_fill_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "fill_strength", self.ui.crc_label_fill_strength, 1))
    self.ui.crc_hslider_fill_strength.sliderReleased.connect(self.hslider_release)
    self.ui.crc_hslider_fill_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "fill_opacity", self.ui.crc_label_fill_opacity, 100))
    self.ui.crc_hslider_fill_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.crc_cb_selector_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", COLOURS, "line_colour_name"))
    self.ui.crc_hslider_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "line_strength", self.ui.crc_label_line_strength, 1))
    self.ui.crc_hslider_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.crc_hslider_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "line_opacity", self.ui.crc_label_line_opacity, 100))
    self.ui.crc_hslider_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.crc_cb_selector_o_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.crc_hslider_o_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "o_arrow", self.ui.crc_label_o_arrow_length, 4, "length"))
    self.ui.crc_hslider_o_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.crc_hslider_o_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "o_arrow", self.ui.crc_label_o_arrow_width, 4, "width"))
    self.ui.crc_hslider_o_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.crc_cb_selector_o_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", ARROW_SIDES, "o_arrow", "side"))
    self.ui.crc_checkb_o_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "circles", "o_arrow", "reversed"))

    self.ui.crc_cb_selector_d_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", ARROW_TIPS, "d_arrow", "tip"))
    self.ui.crc_hslider_d_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "d_arrow", self.ui.crc_label_d_arrow_length, 4, "length"))
    self.ui.crc_hslider_d_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.crc_hslider_d_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "circles", "d_arrow", self.ui.crc_label_d_arrow_width, 4, "width"))
    self.ui.crc_hslider_d_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.crc_cb_selector_d_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "circles", ARROW_SIDES, "d_arrow", "side"))
    self.ui.crc_checkb_d_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "circles", "d_arrow", "reversed"))


def connect_angle_gui(self):
    self.ui.ang_cb_selector.currentRowChanged.connect(self.id_selected)

    self.ui.ang_checkb_show_angle.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "angles", "show"))
    self.ui.ang_checkb_show_label.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "angles", "label", "show"))

    self.ui.ang_rad_anglo_right.clicked.connect(self.rad_anglo_right_clicked)
    self.ui.ang_rad_german_right.clicked.connect(self.rad_german_right_clicked)
    self.ui.ang_rad_arbitrary.clicked.connect(self.rad_arbitrary_clicked)

    self.ui.ang_hslider_line_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "line_width", self.ui.ang_label_line_width, 5))
    self.ui.ang_hslider_line_width.sliderReleased.connect(self.hslider_release)
    self.ui.ang_pb_default_line_width.clicked.connect(
    lambda : self.pb_default_checked("angles", DEFAULT_ANGLE_LINE_WIDTH,\
    "line_width", self.ui.ang_hslider_line_width, self.ui.ang_label_line_width, 5))

    self.ui.ang_hslider_radius.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "size", self.ui.ang_label_radius, 16))
    self.ui.ang_hslider_radius.sliderReleased.connect(self.hslider_release)

    self.ui.ang_le_name.editingFinished.connect(self.ang_le_name_editing_finished)

    self.ui.ang_hslider_label_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "label", self.ui.ang_label_label_distance, 100, "distance"))
    self.ui.ang_hslider_label_distance.sliderReleased.connect(self.hslider_release)
    self.ui.ang_pb_default_label_distance.clicked.connect(
    lambda : self.pb_default_checked("angles", DEFAULT_ANGLE_LABEL_DISTANCE,\
    "label", self.ui.ang_hslider_label_distance, self.ui.ang_label_label_distance, 100, "distance"))

    self.ui.ang_cb_selector_label_anchor.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", DIRECTIONS, "label", "anchor"))

    self.ui.ang_cb_selector_line_arc.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", ANGLE_ARC, "arc"))

    self.ui.ang_le_line_stroke_custom.editingFinished.connect(
    lambda : self.le_line_stroke_custom_editing_finished("angles", self.ui.ang_le_line_stroke_custom))
    self.ui.ang_cb_selector_line_stroke.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", LINE_STROKES, "line_stroke"))

    self.ui.ang_cb_selector_fill_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", MARKER_COLOURS, "fill_colour_name"))
    self.ui.ang_hslider_fill_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "fill_strength", self.ui.ang_label_fill_strength, 1))
    self.ui.ang_hslider_fill_strength.sliderReleased.connect(self.hslider_release)
    self.ui.ang_hslider_fill_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "fill_opacity", self.ui.ang_label_fill_opacity, 100))
    self.ui.ang_hslider_fill_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.ang_cb_selector_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", COLOURS, "line_colour_name"))
    self.ui.ang_hslider_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "line_strength", self.ui.ang_label_line_strength, 1))
    self.ui.ang_hslider_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.ang_hslider_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "line_opacity", self.ui.ang_label_line_opacity, 100))
    self.ui.ang_hslider_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.ang_cb_selector_o_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.ang_hslider_o_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "o_arrow", self.ui.ang_label_o_arrow_length, 4, "length"))
    self.ui.ang_hslider_o_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.ang_hslider_o_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "o_arrow", self.ui.ang_label_o_arrow_width, 4, "width"))
    self.ui.ang_hslider_o_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.ang_cb_selector_o_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", ARROW_SIDES, "o_arrow", "side"))
    self.ui.ang_checkb_o_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "angles", "o_arrow", "reversed"))

    self.ui.ang_cb_selector_d_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", ARROW_TIPS, "d_arrow", "tip"))
    self.ui.ang_hslider_d_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "d_arrow", self.ui.ang_label_d_arrow_length, 4, "length"))
    self.ui.ang_hslider_d_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.ang_hslider_d_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "d_arrow", self.ui.ang_label_d_arrow_width, 4, "width"))
    self.ui.ang_hslider_d_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.ang_cb_selector_d_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", ARROW_SIDES, "d_arrow", "side"))
    self.ui.ang_checkb_d_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "angles", "d_arrow", "reversed"))

    self.ui.ang_hslider_mark_size.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "mksize", self.ui.ang_label_mark_size, 2))
    self.ui.ang_hslider_mark_size.sliderReleased.connect(self.hslider_release)
    self.ui.ang_pb_default_mark_size.clicked.connect(
    lambda : self.pb_default_checked("angles", DEFAULT_SEGMENT_MARK_SIZE,\
    "mksize", self.ui.ang_hslider_mark_size, self.ui.ang_label_mark_size, 2))
    self.ui.ang_hslider_mark_position.valueChanged.connect(
    lambda value : self.hslider_moved(value, "angles", "mkpos", self.ui.ang_label_mark_position, 16))
    self.ui.ang_hslider_mark_position.sliderReleased.connect(self.hslider_release)
    self.ui.ang_pb_default_mark_position.clicked.connect(
    lambda : self.pb_default_checked("angles", DEFAULT_SEGMENT_MARK_POSITION,\
    "mkpos", self.ui.ang_hslider_mark_position, self.ui.ang_label_mark_position, 16))
    self.ui.ang_cb_selector_mark_symbol.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", SEGMENT_MARKERS, "mksymbol"))
    self.ui.ang_cb_selector_mark_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "angles", MARKER_COLOURS, "mkcolour"))


def connect_polygon_gui(self):
    self.ui.pol_cb_selector.currentRowChanged.connect(self.id_selected)
    self.ui.pol_rad_polygon.clicked.connect(self.rad_polygon_clicked)
    self.ui.pol_rad_linestring.clicked.connect(self.rad_linestring_clicked)
    self.ui.pol_checkb_show_object.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "polygons", "show"))

    self.ui.pol_hslider_line_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "line_width", self.ui.pol_label_line_width, 5))
    self.ui.pol_hslider_line_width.sliderReleased.connect(self.hslider_release)
    self.ui.pol_pb_default_line_width.clicked.connect(
    lambda : self.pb_default_checked("polygons", DEFAULT_SEGMENT_LINE_WIDTH,\
    "line_width", self.ui.pol_hslider_line_width, self.ui.pol_label_line_width, 5))

    self.ui.pol_le_line_stroke_custom.editingFinished.connect(
    lambda : self.le_line_stroke_custom_editing_finished("polygons", self.ui.pol_le_line_stroke_custom))
    self.ui.pol_cb_selector_line_stroke.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", LINE_STROKES, "line_stroke"))

    self.ui.pol_cb_selector_decoration.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", DECORATIONS, "decoration", "type"))

    self.ui.pol_hslider_amplitude.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "decoration", self.ui.pol_label_amplitude, 5, "amplitude"))
    self.ui.pol_hslider_amplitude.sliderReleased.connect(self.hslider_release)

    self.ui.pol_hslider_wave_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "decoration", self.ui.pol_label_wave_length, 5, "wave_length"))
    self.ui.pol_hslider_wave_length.sliderReleased.connect(self.hslider_release)

    self.ui.pol_le_decoration_text.editingFinished.connect(self.pol_le_decoration_text_editing_finished)

    self.ui.pol_cb_selector_strategy.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", STRATEGIES, "curve", "strategy"))

    self.ui.pol_hslider_out_angle.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "curve", self.ui.pol_label_out_angle, 1, "out_angle"))
    self.ui.pol_hslider_out_angle.sliderReleased.connect(self.hslider_release)

    self.ui.pol_hslider_in_angle.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "curve", self.ui.pol_label_in_angle, 1, "in_angle"))
    self.ui.pol_hslider_in_angle.sliderReleased.connect(self.hslider_release)

    self.ui.pol_hslider_bend_angle.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "curve", self.ui.pol_label_bend_angle, 1, "bend_angle"))
    self.ui.pol_hslider_bend_angle.sliderReleased.connect(self.hslider_release)

    self.ui.pol_hslider_corner.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "curve", self.ui.pol_label_corner, 1, "corner_radius"))
    self.ui.pol_hslider_corner.sliderReleased.connect(self.hslider_release)

    self.ui.pol_hslider_loop_size.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "curve", self.ui.pol_label_loop_size, 1, "loop_size"))
    self.ui.pol_hslider_loop_size.sliderReleased.connect(self.hslider_release)

    self.ui.pol_checkb_loop.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "polygons", "curve", "loop"))

    self.ui.pol_cb_selector_fill_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", COLOURS, "fill_colour_name"))
    self.ui.pol_hslider_fill_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "fill_strength", self.ui.pol_label_fill_strength, 1))
    self.ui.pol_hslider_fill_strength.sliderReleased.connect(self.hslider_release)
    self.ui.pol_hslider_fill_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "fill_opacity", self.ui.pol_label_fill_opacity, 100))
    self.ui.pol_hslider_fill_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.pol_cb_selector_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", COLOURS, "line_colour_name"))
    self.ui.pol_hslider_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "line_strength", self.ui.pol_label_line_strength, 1))
    self.ui.pol_hslider_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.pol_hslider_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "line_opacity", self.ui.pol_label_line_opacity, 100))
    self.ui.pol_hslider_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.pol_cb_selector_o_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.pol_hslider_o_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "o_arrow", self.ui.pol_label_o_arrow_length, 4, "length"))
    self.ui.pol_hslider_o_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.pol_hslider_o_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "o_arrow", self.ui.pol_label_o_arrow_width, 4, "width"))
    self.ui.pol_hslider_o_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.pol_cb_selector_o_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", ARROW_SIDES, "o_arrow", "side"))
    self.ui.pol_checkb_o_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "polygons", "o_arrow", "reversed"))

    self.ui.pol_cb_selector_d_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", ARROW_TIPS, "d_arrow", "tip"))
    self.ui.pol_hslider_d_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "d_arrow", self.ui.pol_label_d_arrow_length, 4, "length"))
    self.ui.pol_hslider_d_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.pol_hslider_d_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "d_arrow", self.ui.pol_label_d_arrow_width, 4, "width"))
    self.ui.pol_hslider_d_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.pol_cb_selector_d_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", ARROW_SIDES, "d_arrow", "side"))
    self.ui.pol_checkb_d_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "polygons", "d_arrow", "reversed"))

    self.ui.pol_cb_selector_pattern_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "polygons", PATTERN_TYPES, "pattern", "type"))

    self.ui.pol_hslider_pattern_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "pattern", self.ui.pol_label_pattern_distance, 2, "distance"))
    self.ui.pol_hslider_pattern_distance.sliderReleased.connect(self.hslider_release)
    self.ui.pol_pb_default_pattern_distance.clicked.connect(
    lambda : self.pb_default_checked("polygons", DEFAULT_PATTERN_DISTANCE,\
    "pattern", self.ui.pol_hslider_pattern_distance, self.ui.pol_label_pattern_distance, 2, "distance"))

    self.ui.pol_hslider_pattern_size.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "pattern", self.ui.pol_label_pattern_size, 5, "size"))
    self.ui.pol_hslider_pattern_size.sliderReleased.connect(self.hslider_release)
    self.ui.pol_pb_default_pattern_size.clicked.connect(
    lambda : self.pb_default_checked("polygons", DEFAULT_PATTERN_SIZE,\
    "pattern", self.ui.pol_hslider_pattern_size, self.ui.pol_label_pattern_size, 5, "size"))

    self.ui.pol_hslider_pattern_rotation.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "pattern", self.ui.pol_label_pattern_rotation, 1, "rotation"))
    self.ui.pol_hslider_pattern_rotation.sliderReleased.connect(self.hslider_release)
    self.ui.pol_pb_default_pattern_rotation.clicked.connect(
    lambda : self.pb_default_checked("polygons", DEFAULT_PATTERN_ROTATION,\
    "pattern", self.ui.pol_hslider_pattern_rotation, self.ui.pol_label_pattern_rotation, 1, "rotation"))

    self.ui.pol_hslider_pattern_xshift.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "pattern", self.ui.pol_label_pattern_xshift, 2, "xshift"))
    self.ui.pol_hslider_pattern_xshift.sliderReleased.connect(self.hslider_release)

    self.ui.pol_hslider_pattern_yshift.valueChanged.connect(
    lambda value : self.hslider_moved(value, "polygons", "pattern", self.ui.pol_label_pattern_yshift, 2, "yshift"))
    self.ui.pol_hslider_pattern_yshift.sliderReleased.connect(self.hslider_release)


def connect_function_gui(self):
    self.ui.fct_cb_selector.currentRowChanged.connect(self.id_selected)
    self.ui.fct_checkb_show_function.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "functions", "show"))

    self.ui.fct_cb_selector_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", COLOURS, "line_colour_name"))
    self.ui.fct_hslider_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "line_strength", self.ui.fct_label_line_strength, 1))
    self.ui.fct_hslider_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.fct_hslider_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "line_opacity", self.ui.fct_label_line_opacity, 100))
    self.ui.fct_hslider_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.fct_hslider_line_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "line_width", self.ui.fct_label_line_width, 5))
    self.ui.fct_hslider_line_width.sliderReleased.connect(self.hslider_release)
    self.ui.fct_pb_default_line_width.clicked.connect(
    lambda : self.pb_default_checked("functions", DEFAULT_SEGMENT_LINE_WIDTH,\
    "line_width", self.ui.fct_hslider_line_width, self.ui.fct_label_line_width, 5))

    self.ui.fct_le_line_stroke_custom.editingFinished.connect(
    lambda : self.le_line_stroke_custom_editing_finished("functions", self.ui.fct_le_line_stroke_custom))
    self.ui.fct_cb_selector_line_stroke.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", LINE_STROKES, "line_stroke"))

    self.ui.fct_hslider_samples.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "samples", self.ui.fct_label_samples, 1))
    self.ui.fct_hslider_samples.sliderReleased.connect(self.hslider_release)

    self.ui.fct_le_function_def.editingFinished.connect(self.fct_le_function_def_text_editing_finished)

    self.ui.fct_le_start.editingFinished.connect(
    lambda : self.le_number_edit("functions", "domain_start", self.ui.fct_le_start, True))
    self.ui.fct_le_end.editingFinished.connect(
    lambda : self.le_number_edit("functions", "domain_end", self.ui.fct_le_end, True))

    self.ui.fct_cb_selector_o_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.fct_hslider_o_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "o_arrow", self.ui.fct_label_o_arrow_length, 4, "length"))
    self.ui.fct_hslider_o_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.fct_hslider_o_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "o_arrow", self.ui.fct_label_o_arrow_width, 4, "width"))
    self.ui.fct_hslider_o_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.fct_cb_selector_o_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", ARROW_SIDES, "o_arrow", "side"))
    self.ui.fct_checkb_o_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "functions", "o_arrow", "reversed"))

    self.ui.fct_cb_selector_d_arrow_tip.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", ARROW_TIPS, "d_arrow", "tip"))
    self.ui.fct_hslider_d_arrow_length.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "d_arrow", self.ui.fct_label_d_arrow_length, 4, "length"))
    self.ui.fct_hslider_d_arrow_length.sliderReleased.connect(self.hslider_release)
    self.ui.fct_hslider_d_arrow_width.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "d_arrow", self.ui.fct_label_d_arrow_width, 4, "width"))
    self.ui.fct_hslider_d_arrow_width.sliderReleased.connect(self.hslider_release)
    self.ui.fct_cb_selector_d_arrow_side.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", ARROW_SIDES, "d_arrow", "side"))
    self.ui.fct_checkb_d_arrow_reversed.stateChanged.connect(
    lambda state: self.checkb_state_changed(state, "functions", "d_arrow", "reversed"))

    self.ui.fct_cb_selector_sum_type.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", FUNCTION_TYPES, "sum", "type"))

    self.ui.fct_le_sum_start.editingFinished.connect(
    lambda : self.le_number_edit("functions", "sum", self.ui.fct_le_sum_start, True, "start"))
    self.ui.fct_le_sum_end.editingFinished.connect(
    lambda : self.le_number_edit("functions", "sum", self.ui.fct_le_sum_end, True, "end"))
    self.ui.fct_hslider_sum_number.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "sum", self.ui.fct_label_sum_number, 1, "number"))
    self.ui.fct_hslider_sum_number.sliderReleased.connect(self.hslider_release)


    self.ui.fct_cb_selector_sum_fill_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", MARKER_COLOURS, "sum", "fill_colour_name"))
    self.ui.fct_hslider_sum_fill_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "sum", self.ui.fct_label_sum_fill_strength, 1, "fill_strength"))
    self.ui.fct_hslider_sum_fill_strength.sliderReleased.connect(self.hslider_release)
    self.ui.fct_hslider_sum_fill_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "sum", self.ui.fct_label_sum_fill_opacity, 100, "fill_opacity"))
    self.ui.fct_hslider_sum_fill_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.fct_cb_selector_sum_line_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", COLOURS, "sum", "line_colour_name"))
    self.ui.fct_hslider_sum_line_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "sum", self.ui.fct_label_sum_line_strength, 1, "line_strength"))
    self.ui.fct_hslider_sum_line_strength.sliderReleased.connect(self.hslider_release)
    self.ui.fct_hslider_sum_line_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "sum", self.ui.fct_label_sum_line_opacity, 100, "line_opacity"))
    self.ui.fct_hslider_sum_line_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.fct_cb_selector_pattern_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", PATTERN_TYPES, "pattern", "type"))

    self.ui.fct_hslider_pattern_distance.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "pattern", self.ui.fct_label_pattern_distance, 2, "distance"))
    self.ui.fct_hslider_pattern_distance.sliderReleased.connect(self.hslider_release)
    self.ui.fct_pb_default_pattern_distance.clicked.connect(
    lambda : self.pb_default_checked("functions", DEFAULT_PATTERN_DISTANCE,\
    "pattern", self.ui.fct_hslider_pattern_distance, self.ui.fct_label_pattern_distance, 2, "distance"))

    self.ui.fct_hslider_pattern_size.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "pattern", self.ui.fct_label_pattern_size, 5, "size"))
    self.ui.fct_hslider_pattern_size.sliderReleased.connect(self.hslider_release)
    # self.ui.fct_pb_default_pattern_size.clicked.connect(
    # lambda : self.pb_default_checked("functions", DEFAULT_PATTERN_SIZE,\
    # "pattern", self.ui.fct_hslider_pattern_size, self.ui.fct_label_pattern_size, 5, "size"))

    self.ui.fct_hslider_pattern_rotation.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "pattern", self.ui.fct_label_pattern_rotation, 1, "rotation"))
    self.ui.fct_hslider_pattern_rotation.sliderReleased.connect(self.hslider_release)

    self.ui.fct_hslider_pattern_xshift.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "pattern", self.ui.fct_label_pattern_xshift, 2, "xshift"))
    self.ui.fct_hslider_pattern_xshift.sliderReleased.connect(self.hslider_release)

    self.ui.fct_hslider_pattern_yshift.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "pattern", self.ui.fct_label_pattern_yshift, 2, "yshift"))
    self.ui.fct_hslider_pattern_yshift.sliderReleased.connect(self.hslider_release)

    self.ui.fct_cb_selector_fill_colour_name.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed(value, "functions", COLOURS, "fill_colour_name"))
    self.ui.fct_hslider_fill_strength.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "fill_strength", self.ui.fct_label_fill_strength, 1))
    self.ui.fct_hslider_fill_strength.sliderReleased.connect(self.hslider_release)
    self.ui.fct_hslider_fill_opacity.valueChanged.connect(
    lambda value : self.hslider_moved(value, "functions", "fill_opacity", self.ui.fct_label_fill_opacity, 100))
    self.ui.fct_hslider_fill_opacity.sliderReleased.connect(self.hslider_release)

    self.ui.fct_le_fill_start.editingFinished.connect(
    lambda : self.le_number_edit("functions", "area_start", self.ui.fct_le_fill_start, True))
    self.ui.fct_le_fill_end.editingFinished.connect(
    lambda : self.le_number_edit("functions", "area_end", self.ui.fct_le_fill_end, True))

    self.ui.fct_cb_selector_pattern_between.currentIndexChanged.connect(self.fct_cb_selector_pattern_between_idx_changed)


def connect_axes_gui(self):
    #GRID
    self.ui.axe_checkb_show_grid.stateChanged.connect(
    lambda state: self.axes_checkb(state, "grid", "show"))

    self.ui.axe_cb_selector_subdivisions_x.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "grid", list(range(1,11)), "sub_x"))

    self.ui.axe_cb_selector_subdivisions_y.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "grid", list(range(1,11)), "sub_y"))


    self.ui.axe_hslider_grid_line_opacity.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "grid", "line_opacity", self.ui.axe_label_grid_line_opacity, 100))
    self.ui.axe_hslider_grid_line_opacity.sliderReleased.connect(self.axe_hslider_release)

    self.ui.axe_hslider_grid_line_width.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "grid", "line_width", self.ui.axe_label_grid_line_width, 5))
    self.ui.axe_hslider_grid_line_width.sliderReleased.connect(self.axe_hslider_release)

    self.ui.axe_cb_selector_grid_line_colour_name.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "grid", COLOURS, "line_colour_name"))

    self.ui.axe_le_divisions_line_stroke_custom.editingFinished.connect(
    lambda : self.axe_le_line_stroke_custom_editing_finished("grid", "line_stroke_custom", self.ui.axe_le_divisions_line_stroke_custom))
    self.ui.axe_cb_selector_divisions_line_stroke.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "grid", LINE_STROKES, "line_stroke"))

    self.ui.axe_le_subdivisions_line_stroke_custom.editingFinished.connect(
    lambda : self.axe_le_line_stroke_custom_editing_finished("grid", "sub_line_stroke_custom", self.ui.axe_le_subdivisions_line_stroke_custom))
    self.ui.axe_cb_selector_subdivisions_line_stroke.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "grid", LINE_STROKES, "sub_line_stroke"))

    #AXES

    self.ui.axe_cb_selector_label_font_size.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis", FONT_SIZES, "labels", "size"))
    self.ui.axe_cb_selector_axes_line_colour_name.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis", COLOURS, "line_colour_name"))
    self.ui.axe_cb_selector_label_colour_name.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis", COLOURS, "labels", "colour"))
    self.ui.axe_hslider_axes_line_strength.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis", "line_strength", self.ui.axe_label_axes_line_strength, 1))
    self.ui.axe_hslider_axes_line_strength.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_axes_line_width.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis", "line_width", self.ui.axe_label_axes_line_width, 5))
    self.ui.axe_hslider_axes_line_width.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_rotate_x_labels.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis", "labels", self.ui.axe_label_rotate_x_labels, 1, "x_rotate"))
    self.ui.axe_hslider_rotate_x_labels.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_axes_x_below.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis", "labels", self.ui.axe_label_axes_x_below, 5, "x_below"))
    self.ui.axe_hslider_axes_x_below.sliderReleased.connect(self.axe_hslider_release)

    #AXES X

    self.ui.axe_checkb_show_x_axis.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_x", "show"))
    self.ui.axe_le_name_x.editingFinished.connect(
    lambda : self.axe_le_text_editing_finished(self.ui.axe_le_name_x, "axis_x", "label", "text"))
    self.ui.axe_cb_selector_label_anchor_x.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_x", DIRECTIONS, "label", "anchor"))
    self.ui.axe_hslider_label_distance_x.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_x", "label", self.ui.axe_label_label_distance_x, 100, "distance"))
    self.ui.axe_hslider_label_distance_x.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_checkb_show_x_labels.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_x", "labels", "show"))
    self.ui.axe_cb_selector_x_arrow_tip.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_x", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.axe_hslider_x_arrow_length.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_x", "o_arrow", self.ui.axe_label_x_arrow_length, 4, "length"))
    self.ui.axe_hslider_x_arrow_length.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_x_arrow_width.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_x", "o_arrow", self.ui.axe_label_x_arrow_width, 4, "width"))
    self.ui.axe_hslider_x_arrow_width.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_cb_selector_x_arrow_side.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_x", ARROW_SIDES, "o_arrow", "side"))
    self.ui.axe_checkb_x_arrow_reversed.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_x", "o_arrow", "reversed"))
    self.ui.axe_cb_selector_x_arrow_orient.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_x", TRUE_FALSE, "o_arrow", "direction"))
    self.ui.axe_checkb_ticks_x.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_x", "is_tick"))
    self.ui.axe_checkb_numprint_x.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_x", "is_numprint"))
    self.ui.axe_checkb_orig_x.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_x", "is_orig"))
    self.ui.axe_cb_selector_trig_x.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_x", FRACTIONS, "trig"))
    self.ui.axe_cb_selector_frac_x.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_x", FRACTIONS, "frac"))
    self.ui.axe_hslider_x_tick_up.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_x", "tick_up", self.ui.axe_label_x_tick_up, 5))
    self.ui.axe_hslider_x_tick_up.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_x_tick_down.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_x", "tick_down", self.ui.axe_label_x_tick_down, 5))
    self.ui.axe_hslider_x_tick_down.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_x_tick_width.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_x", "tick_width", self.ui.axe_label_x_tick_width, 5))
    self.ui.axe_hslider_x_tick_width.sliderReleased.connect(self.axe_hslider_release)

    #AXES Y

    self.ui.axe_checkb_show_y_axis.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_y", "show"))
    self.ui.axe_le_name_y.editingFinished.connect(
    lambda : self.axe_le_text_editing_finished(self.ui.axe_le_name_y, "axis_y", "label", "text"))
    self.ui.axe_cb_selector_label_anchor_y.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_y", DIRECTIONS, "label", "anchor"))
    self.ui.axe_hslider_label_distance_y.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_y", "label", self.ui.axe_label_label_distance_y, 100, "distance"))
    self.ui.axe_hslider_label_distance_y.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_checkb_show_y_labels.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_y", "labels", "show"))
    self.ui.axe_cb_selector_y_arrow_tip.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_y", ARROW_TIPS, "o_arrow", "tip"))
    self.ui.axe_hslider_y_arrow_length.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_y", "o_arrow", self.ui.axe_label_y_arrow_length, 4, "length"))
    self.ui.axe_hslider_y_arrow_length.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_y_arrow_width.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_y", "o_arrow", self.ui.axe_label_y_arrow_width, 4, "width"))
    self.ui.axe_hslider_y_arrow_width.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_cb_selector_y_arrow_side.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_y", ARROW_SIDES, "o_arrow", "side"))
    self.ui.axe_checkb_y_arrow_reversed.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_y", "o_arrow", "reversed"))
    self.ui.axe_cb_selector_y_arrow_orient.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_y", TRUE_FALSE, "o_arrow", "direction"))
    self.ui.axe_checkb_ticks_y.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_y", "is_tick"))
    self.ui.axe_checkb_numprint_y.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_y", "is_numprint"))
    self.ui.axe_checkb_orig_y.stateChanged.connect(
    lambda state: self.axes_checkb(state, "axis_y", "is_orig"))
    self.ui.axe_cb_selector_trig_y.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_y", FRACTIONS, "trig"))
    self.ui.axe_cb_selector_frac_y.currentIndexChanged.connect(
    lambda value : self.axe_cb_selector_current_idx_changed(value, "axis_y", FRACTIONS, "frac"))
    self.ui.axe_hslider_y_tick_left.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_y", "tick_up", self.ui.axe_label_y_tick_left, 5))
    self.ui.axe_hslider_y_tick_left.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_y_tick_right.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_y", "tick_down", self.ui.axe_label_y_tick_right, 5))
    self.ui.axe_hslider_y_tick_right.sliderReleased.connect(self.axe_hslider_release)
    self.ui.axe_hslider_y_tick_width.valueChanged.connect(
    lambda value : self.axe_hslider_moved(value, "axis_y", "tick_width", self.ui.axe_label_y_tick_width, 5))
    self.ui.axe_hslider_y_tick_width.sliderReleased.connect(self.axe_hslider_release)


def connect_settings_gui(self):
    eucl = self.scene.eucl
    self.ui.set_le_latex_command.editingFinished.connect(self.set_le_latex_command_changed)
    self.ui.set_le_pdf_to_jpg_command.editingFinished.connect(self.set_le_pdf_to_jpg_command_changed)
    self.ui.set_checkb_aspect_ratio_indicator.stateChanged.connect(self.set_checkb_aspect_ratio_indicator_changed)
    self.ui.set_le_aspect_ratio.editingFinished.connect(self.set_le_aspect_ratio_editingFinished)

    self.ui.set_cb_selector_bg_colour.currentIndexChanged.connect(
    lambda value : self.cb_selector_current_idx_changed_new(eucl, "bg_colour_name", MIX_COLOURS[value]))
    self.ui.set_hslider_bg_colour_strength.valueChanged.connect(
    lambda value : self.hslider_moved_new(eucl, "bg_colour_strength", value, self.ui.set_label_bg_colour_strength, 1))
    self.ui.set_hslider_bg_colour_strength.sliderReleased.connect(self.hslider_release_new)
    self.ui.set_edit_before.textChanged.connect(lambda : self.before_after_textChanged(eucl, "code_before", self.ui.set_edit_before))
    self.ui.set_edit_after.textChanged.connect(lambda : self.before_after_textChanged(eucl, "code_after", self.ui.set_edit_after))
    self.ui.set_pb_editingFinished.clicked.connect(lambda : self.set_pb_editingFinished_clicked(self.ui.set_pb_editingFinished))

    self.ui.set_cb_selector.itemChanged.connect(self.package_list_updated)
    self.ui.set_pb_new_package.clicked.connect(self.add_new_package)
    self.ui.set_pb_delete_package.clicked.connect(self.delete_package)



def add_objects_to_combobox(dialog):
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

def circle_text(eucl, circle_id):
    circle = soj.get_item_from_id(eucl, circle_id, "c")
    if circle["type"] == "circum_circle":
        return "circumscribed circle of %s" % (circle["points"]["A"]+circle["points"]["B"]+circle["points"]["C"])
    if circle["type"] == "two_point_circle":
        return "circle centred at %s with radius %s" % (circle["points"]["O"], circle["points"]["A"]+circle["points"]["O"])
    if circle["type"] == "inscribed_circle":
        return "inscribed circle of %s" % (circle["points"]["A"]+circle["points"]["B"]+circle["points"]["C"])
    if circle["type"] == "arc":
        return "arc with centre %s between %s and %s" % (circle["points"]["A"], circle["points"]["A"], circle["points"]["B"])
    if circle["type"] == "sector":
        return "sector with centre %s between %s and %s" % (circle["points"]["A"], circle["points"]["A"], circle["points"]["B"])

def fill_point_fields(dialog):
    def make_text(point, eucl):
        if point["id"] == 'pt_default':
            return ''
        text = POINT_TEXT_DICT[point["from"]["type"]]
        if point["from"]["type"] == "free":
            pass
        elif point["from"]["type"] == "intersection_ll":
            text = text.replace('#1', point["from"]["A"] + point["from"]["B"])
            text = text.replace('#2', point["from"]["C"] + point["from"]["D"])
        elif point["from"]["type"] == "intersection_lc":
            text = text.replace('#1', point["from"]["A"] + point["from"]["B"])
            text = text.replace('#2', circle_text(eucl, point["from"]["circle"]))
        elif point["from"]["type"] == "circle_midpoint":
            text = text.replace('#1', circle_text(eucl, point["from"]["circle"]))
        elif point["from"]["type"] == "segment_midpoint":
            text = text.replace('#1', point["from"]["A"] + point["from"]["B"])
        elif point["from"]["type"] == "point_on_line":
            text = text.replace('#1', point["from"]["A"])
            text = text.replace('#2', point["from"]["ratio"])
            text = text.replace('#3', point["from"]["B"])
        elif point["from"]["type"] == "point_on_circle":
            text = text.replace('#1', circle_text(eucl, point["from"]["circle"]))
            text = text.replace('#2', point["from"]["angle"])
        elif point["from"]["type"] == "projection_point":
            text = text.replace('#1', point["from"]["P"])
            text = text.replace('#2', point["from"]["A"]+point["from"]["B"])
        elif point["from"]["type"] == "bisector_point":
            text = text.replace('#1', point["from"]["A"]+point["from"]["B"]+point["from"]["C"])
        elif point["from"]["type"] == "translation_point":
            text = text.replace('#1', point["from"]["P"])
            text = text.replace('#2', point["from"]["A"]+point["from"]["B"])
        elif point["from"]["type"] == "orthogonal_point":
            text = text.replace('#1', point["from"]["A"]+point["from"]["B"])
            text = text.replace('#2', point["from"]["A"])
        elif point["from"]["type"] == "rotation":
            text = text.replace('#1', point["from"]["B"])
            text = text.replace('#2', point["from"]["angle"])
            text = text.replace('#3', point["from"]["A"])

        return text

    point = dialog.scene.eucl["points"][dialog.current_id]

    dialog.ui.pt_le_id.setText(point["id"])
    dialog.ui.pt_le_name.setText(point["label"]["text"])
    if point["show"] == True:
        dialog.ui.pt_checkb_show_point.setChecked(True)
    else:
        dialog.ui.pt_checkb_show_point.setChecked(False)
    if point["label"]["show"] == True:
        dialog.ui.pt_checkb_show_label.setChecked(True)
        dialog.ui.pt_groupBox_label.setEnabled(True)
    else:
        dialog.ui.pt_checkb_show_label.setChecked(False)
        dialog.ui.pt_groupBox_label.setEnabled(False)
    dialog.ui.pt_hslider_size.setValue(point["size"]*2)
    dialog.ui.pt_label_size.setText(str(point["size"]))

    dialog.ui.pt_le_x.setText("%s" % point["x"])
    dialog.ui.pt_le_y.setText("%s" % point["y"])

    if point["from"]["type"] != "free":
        dialog.ui.pt_le_x.setEnabled(False)
        dialog.ui.pt_le_y.setEnabled(False)
    else:
        dialog.ui.pt_le_x.setEnabled(True)
        dialog.ui.pt_le_y.setEnabled(True)

    dialog.ui.pt_hslider_line_width.setValue(point["line_width"]*5)
    dialog.ui.pt_label_line_width.setText(str(point["line_width"]))

    dialog.ui.pt_hslider_label_angle.setValue(point["label"]["angle"])
    dialog.ui.pt_label_label_angle.setText(str(point["label"]["angle"]))

    dialog.ui.pt_hslider_label_distance.setValue(point["label"]["distance"]*100)
    dialog.ui.pt_label_label_distance.setText(str(point["label"]["distance"]))

    dialog.state_change_ignore = True
    dialog.ui.pt_cb_selector_label_anchor.setCurrentIndex(DIRECTIONS.index(point["label"]["anchor"]))
    dialog.ui.pt_cb_selector_fill_colour_name.setCurrentIndex(COLOURS.index(point["fill_colour_name"]))
    dialog.ui.pt_cb_selector_line_colour_name.setCurrentIndex(COLOURS.index(point["line_colour_name"]))
    dialog.ui.pt_cb_selector_line_stroke.setCurrentIndex(LINE_STROKES.index(point["line_stroke"]))
    dialog.state_change_ignore = False

    dialog.ui.pt_hslider_fill_strength.setValue(point["fill_strength"])
    dialog.ui.pt_label_fill_strength.setText(str(point["fill_strength"]))
    dialog.ui.pt_hslider_fill_opacity.setValue(point["fill_opacity"]*100)
    dialog.ui.pt_label_fill_opacity.setText(str(point["fill_opacity"]))

    dialog.ui.pt_hslider_line_strength.setValue(point["line_strength"])
    dialog.ui.pt_label_line_strength.setText(str(point["line_strength"]))
    dialog.ui.pt_hslider_line_opacity.setValue(point["line_opacity"]*100)
    dialog.ui.pt_label_line_opacity.setText(str(point["line_opacity"]))

    if point["line_stroke"] != "custom":
        dialog.pt_le_line_stroke_custom.setEnabled(False)
    else:
        dialog.pt_le_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in point["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.pt_le_line_stroke_custom.setText(lengths_str)

    if point["from"]["type"] != "point_on_line":
        dialog.ui.pt_le_line_ratio.setEnabled(False)
    else:
        dialog.ui.pt_le_line_ratio.setEnabled(True)
        dialog.ui.pt_le_line_ratio.setText(point["from"]["ratio"])

    if point["from"]["type"] != "point_on_circle":
        dialog.ui.pt_le_circle_angle.setEnabled(False)
    else:
        dialog.ui.pt_le_circle_angle.setEnabled(True)
        dialog.ui.pt_le_circle_angle.setText(point["from"]["angle"])

    if point["from"]["type"] != "rotation":
        dialog.ui.pt_le_line_rotation_angle.setEnabled(False)
    else:
        dialog.ui.pt_le_line_rotation_angle.setEnabled(True)
        dialog.ui.pt_le_line_rotation_angle.setText(point["from"]["angle"])

    dialog.ui.textBrowser.setText(make_text(point, dialog.scene.eucl))



def fill_segment_fields(dialog):
    segment = dialog.scene.eucl["segments"][dialog.current_id]
    dialog.ui.sg_label_id.setText(str(segment["id"]))
    dialog.ui.sg_label_origin_id.setText(segment["points"]["from"])
    dialog.ui.sg_label_dest_id.setText(segment["points"]["to"])

    if segment["show"] == True:
        dialog.ui.sg_checkb_show_segment.setChecked(True)
    else:
        dialog.ui.sg_checkb_show_segment.setChecked(False)
    if segment["label"]["show"] == True:
        dialog.ui.sg_checkb_show_label.setChecked(True)
        dialog.ui.sg_groupBox_label.setEnabled(True)
    else:
        dialog.ui.sg_checkb_show_label.setChecked(False)
        dialog.ui.sg_groupBox_label.setEnabled(False)

    dialog.ui.sg_hslider_line_width.setValue(segment["line_width"]*5)
    dialog.ui.sg_label_line_width.setText(str(segment["line_width"]))

    dialog.state_change_ignore = True
    dialog.ui.sg_cb_selector_line_stroke.setCurrentIndex(LINE_STROKES.index(segment["line_stroke"]))
    dialog.ui.sg_cb_selector_label_anchor.setCurrentIndex(DIRECTIONS.index(segment["label"]["anchor"]))
    dialog.ui.sg_cb_selector_line_colour_name.setCurrentIndex(COLOURS.index(segment["line_colour_name"]))
    dialog.ui.sg_cb_selector_o_arrow_tip.setCurrentIndex(ARROW_TIPS.index(segment["o_arrow"]["tip"]))
    dialog.ui.sg_cb_selector_o_arrow_side.setCurrentIndex(ARROW_SIDES.index(segment["o_arrow"]["side"]))
    dialog.ui.sg_cb_selector_d_arrow_tip.setCurrentIndex(ARROW_TIPS.index(segment["d_arrow"]["tip"]))
    dialog.ui.sg_cb_selector_d_arrow_side.setCurrentIndex(ARROW_SIDES.index(segment["d_arrow"]["side"]))
    dialog.ui.sg_cb_selector_mark_symbol.setCurrentIndex(SEGMENT_MARKERS.index(segment["mark"]["symbol"]))
    dialog.ui.sg_cb_selector_mark_colour_name.setCurrentIndex(MARKER_COLOURS.index(segment["mark"]["colour"]))
    dialog.state_change_ignore = False

    if segment["line_stroke"] != "custom":
        dialog.sg_le_line_stroke_custom.setEnabled(False)
    else:
        dialog.sg_le_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in segment["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.sg_le_line_stroke_custom.setText(lengths_str)
    dialog.ui.sg_le_name.setText(segment["label"]["text"])

    dialog.ui.sg_hslider_label_position.setValue(segment["label"]["position"]*100)
    dialog.ui.sg_label_label_position.setText(str(segment["label"]["position"]))

    dialog.ui.sg_hslider_label_angle.setValue(segment["label"]["angle"])
    dialog.ui.sg_label_label_angle.setText(str(segment["label"]["angle"]))

    dialog.ui.sg_hslider_label_distance.setValue(segment["label"]["distance"]*100)
    dialog.ui.sg_label_label_distance.setText(str(segment["label"]["distance"]))

    dialog.ui.sg_hslider_line_strength.setValue(segment["line_strength"])
    dialog.ui.sg_label_line_strength.setText(str(segment["line_strength"]))
    dialog.ui.sg_hslider_line_opacity.setValue(segment["line_opacity"]*100)
    dialog.ui.sg_label_line_opacity.setText(str(segment["line_opacity"]))

    dialog.ui.sg_hslider_o_arrow_length.setValue(segment["o_arrow"]["length"]*4)
    dialog.ui.sg_label_o_arrow_length.setText(str(segment["o_arrow"]["length"]))

    dialog.ui.sg_hslider_o_arrow_width.setValue(segment["o_arrow"]["width"]*4)
    dialog.ui.sg_label_o_arrow_width.setText(str(segment["o_arrow"]["width"]))

    if segment["o_arrow"]["reversed"] == True:
        dialog.ui.sg_checkb_o_arrow_reversed.setChecked(True)
    else:
        dialog.ui.sg_checkb_o_arrow_reversed.setChecked(False)

    dialog.ui.sg_hslider_d_arrow_length.setValue(segment["d_arrow"]["length"]*4)
    dialog.ui.sg_label_d_arrow_length.setText(str(segment["d_arrow"]["length"]))

    dialog.ui.sg_hslider_d_arrow_width.setValue(segment["d_arrow"]["width"]*4)
    dialog.ui.sg_label_d_arrow_width.setText(str(segment["d_arrow"]["width"]))

    if segment["d_arrow"]["reversed"] == True:
        dialog.ui.sg_checkb_d_arrow_reversed.setChecked(True)
    else:
        dialog.ui.sg_checkb_d_arrow_reversed.setChecked(False)

    dialog.ui.sg_hslider_mark_width.setValue(segment["mark"]["width"]*5)
    dialog.ui.sg_label_mark_width.setText(str(segment["mark"]["width"]))
    dialog.ui.sg_hslider_mark_size.setValue(segment["mark"]["size"]*2)
    dialog.ui.sg_label_mark_size.setText(str(segment["mark"]["size"]))
    dialog.ui.sg_hslider_mark_position.setValue(segment["mark"]["position"]*16)
    dialog.ui.sg_label_mark_position.setText(str(segment["mark"]["position"]))

    dialog.ui.sg_hslider_ext_o.setValue(segment["extension"]["origin"]*16)
    dialog.ui.sg_label_ext_o.setText(str(segment["extension"]["origin"]))
    dialog.ui.sg_hslider_ext_d.setValue(segment["extension"]["destination"]*16)
    dialog.ui.sg_label_ext_d.setText(str(segment["extension"]["destination"]))


def fill_angle_fields(dialog):
    angle = dialog.scene.eucl["angles"][dialog.current_id]

    dialog.ui.ang_label_id.setText(str(angle["id"]))

    if angle["show"] == True:
        dialog.ui.ang_checkb_show_angle.setChecked(True)
    else:
        dialog.ui.ang_checkb_show_angle.setChecked(False)
    if angle["label"]["show"] == True:
        dialog.ui.ang_checkb_show_label.setChecked(True)
        dialog.ui.ang_groupBox_label.setEnabled(True)
    else:
        dialog.ui.ang_checkb_show_label.setChecked(False)
        dialog.ui.ang_groupBox_label.setEnabled(False)

    if not angle["right_angle"]:
        dialog.ui.ang_rad_arbitrary.toggle()
    else:
        if angle["type"] == DEFAULT_RIGHT_ANGLE_TYPE:
            dialog.ui.ang_rad_anglo_right.toggle()
        else:
            dialog.ui.ang_rad_german_right.toggle()

    dialog.ui.ang_hslider_line_width.setValue(angle["line_width"]*5)
    dialog.ui.ang_label_line_width.setText(str(angle["line_width"]))

    dialog.ui.ang_hslider_radius.setValue(angle["size"]*16)
    dialog.ui.ang_label_radius.setText(str(angle["size"]))


    dialog.ui.ang_hslider_label_distance.setValue(angle["label"]["distance"]*100)
    dialog.ui.ang_label_label_distance.setText(str(angle["label"]["distance"]))

    dialog.state_change_ignore = True
    dialog.ui.ang_cb_selector_label_anchor.setCurrentIndex(DIRECTIONS.index(angle["label"]["anchor"]))
    dialog.ui.ang_cb_selector_line_arc.setCurrentIndex(ANGLE_ARC.index(angle["arc"]))
    dialog.ui.ang_cb_selector_line_colour_name.setCurrentIndex(COLOURS.index(angle["line_colour_name"]))
    dialog.ui.ang_cb_selector_fill_colour_name.setCurrentIndex(MARKER_COLOURS.index(angle["fill_colour_name"]))
    dialog.ui.ang_cb_selector_line_stroke.setCurrentIndex(LINE_STROKES.index(angle["line_stroke"]))
    dialog.ui.ang_cb_selector_o_arrow_tip.setCurrentIndex(ARROW_TIPS.index(angle["o_arrow"]["tip"]))
    dialog.ui.ang_cb_selector_o_arrow_side.setCurrentIndex(ARROW_SIDES.index(angle["o_arrow"]["side"]))
    dialog.ui.ang_cb_selector_d_arrow_tip.setCurrentIndex(ARROW_TIPS.index(angle["d_arrow"]["tip"]))
    dialog.ui.ang_cb_selector_d_arrow_side.setCurrentIndex(ARROW_SIDES.index(angle["d_arrow"]["side"]))
    dialog.ui.ang_cb_selector_mark_symbol.setCurrentIndex(SEGMENT_MARKERS.index(angle["mksymbol"]))
    dialog.ui.ang_cb_selector_mark_colour_name.setCurrentIndex(MARKER_COLOURS.index(angle["mkcolour"]))
    dialog.state_change_ignore = False

    dialog.ui.ang_le_name.setText(angle["label"]["text"])
    if angle["line_stroke"] != "custom":
        dialog.ang_le_line_stroke_custom.setEnabled(False)
    else:
        dialog.ang_le_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in angle["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.ang_le_line_stroke_custom.setText(lengths_str)

    dialog.ui.ang_hslider_fill_strength.setValue(angle["fill_strength"])
    dialog.ui.ang_label_fill_strength.setText(str(angle["fill_strength"]))
    dialog.ui.ang_hslider_fill_opacity.setValue(angle["fill_opacity"]*100)
    dialog.ui.ang_label_fill_opacity.setText(str(angle["fill_opacity"]))

    dialog.ui.ang_hslider_line_strength.setValue(angle["line_strength"])
    dialog.ui.ang_label_line_strength.setText(str(angle["line_strength"]))
    dialog.ui.ang_hslider_line_opacity.setValue(angle["line_opacity"]*100)
    dialog.ui.ang_label_line_opacity.setText(str(angle["line_opacity"]))

    dialog.ui.ang_hslider_o_arrow_length.setValue(angle["o_arrow"]["length"]*4)
    dialog.ui.ang_label_o_arrow_length.setText(str(angle["o_arrow"]["length"]))
    dialog.ui.ang_hslider_o_arrow_width.setValue(angle["o_arrow"]["width"]*4)
    dialog.ui.ang_label_o_arrow_width.setText(str(angle["o_arrow"]["width"]))
    if angle["o_arrow"]["reversed"] == True:
        dialog.ui.ang_checkb_o_arrow_reversed.setChecked(True)
    else:
        dialog.ui.ang_checkb_o_arrow_reversed.setChecked(False)

    dialog.ui.ang_hslider_d_arrow_length.setValue(angle["d_arrow"]["length"]*4)
    dialog.ui.ang_label_d_arrow_length.setText(str(angle["d_arrow"]["length"]))
    dialog.ui.ang_hslider_d_arrow_width.setValue(angle["d_arrow"]["width"]*4)
    dialog.ui.ang_label_d_arrow_width.setText(str(angle["d_arrow"]["width"]))
    if angle["d_arrow"]["reversed"] == True:
        dialog.ui.ang_checkb_d_arrow_reversed.setChecked(True)
    else:
        dialog.ui.ang_checkb_d_arrow_reversed.setChecked(False)

    dialog.ui.ang_hslider_mark_size.setValue(angle["mksize"]*2)
    dialog.ui.ang_label_mark_size.setText(str(angle["mksize"]))
    dialog.ui.ang_hslider_mark_position.setValue(angle["mkpos"]*16)
    dialog.ui.ang_label_mark_position.setText(str(angle["mkpos"]))


def fill_circle_fields(dialog):
    circle = dialog.scene.eucl["circles"][dialog.current_id]
    dialog.ui.crc_label_id.setText(str(circle["id"]))

    if circle["type"] == 'arc':
        dialog.ui.crc_groupBox_o_arrow.setEnabled(True)
        dialog.ui.crc_groupBox_d_arrow.setEnabled(True)
    else:
        dialog.ui.crc_groupBox_o_arrow.setEnabled(False)
        dialog.ui.crc_groupBox_d_arrow.setEnabled(False)

    if circle["show"] == True:
        dialog.ui.crc_checkb_show_circle.setChecked(True)
    else:
        dialog.ui.crc_checkb_show_circle.setChecked(False)
    if circle["label"]["show"] == True:
        dialog.ui.crc_checkb_show_label.setChecked(True)
        dialog.ui.crc_groupBox_label.setEnabled(True)
    else:
        dialog.ui.crc_checkb_show_label.setChecked(False)
        dialog.ui.crc_groupBox_label.setEnabled(False)

    dialog.ui.crc_hslider_line_width.setValue(circle["line_width"]*5)
    dialog.ui.crc_label_line_width.setText(str(circle["line_width"]))

    dialog.state_change_ignore = True
    dialog.ui.crc_cb_selector_line_stroke.setCurrentIndex(LINE_STROKES.index(circle["line_stroke"]))
    dialog.ui.crc_cb_selector_label_anchor.setCurrentIndex(DIRECTIONS.index(circle["label"]["anchor"]))
    dialog.ui.crc_cb_selector_pattern_name.setCurrentIndex(PATTERN_TYPES.index(circle["pattern"]["type"]))
    dialog.ui.crc_cb_selector_fill_colour_name.setCurrentIndex(COLOURS.index(circle["fill_colour_name"]))
    dialog.ui.crc_cb_selector_line_colour_name.setCurrentIndex(COLOURS.index(circle["line_colour_name"]))
    if circle["type"] == 'arc':
        dialog.ui.crc_cb_selector_o_arrow_tip.setCurrentIndex(ARROW_TIPS.index(circle["o_arrow"]["tip"]))
        dialog.ui.crc_cb_selector_o_arrow_side.setCurrentIndex(ARROW_SIDES.index(circle["o_arrow"]["side"]))
        dialog.ui.crc_cb_selector_d_arrow_tip.setCurrentIndex(ARROW_TIPS.index(circle["d_arrow"]["tip"]))
        dialog.ui.crc_cb_selector_d_arrow_side.setCurrentIndex(ARROW_SIDES.index(circle["d_arrow"]["side"]))
    dialog.state_change_ignore = False

    if circle["line_stroke"] != "custom":
        dialog.crc_le_line_stroke_custom.setEnabled(False)
    else:
        dialog.crc_le_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in circle["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.crc_le_line_stroke_custom.setText(lengths_str)

    dialog.ui.crc_le_name.setText(circle["label"]["text"])


    dialog.ui.crc_hslider_label_angle.setValue(circle["label"]["angle"])
    dialog.ui.crc_label_label_angle.setText(str(circle["label"]["angle"]))

    dialog.ui.crc_hslider_label_distance.setValue(circle["label"]["distance"]*10)
    dialog.ui.crc_label_label_distance.setText(str(circle["label"]["distance"]))

    dialog.ui.crc_hslider_pattern_distance.setValue(circle["pattern"]["distance"]*2)
    dialog.ui.crc_label_pattern_distance.setText(str(circle["pattern"]["distance"]))

    dialog.ui.crc_hslider_pattern_size.setValue(circle["pattern"]["size"]*5)
    dialog.ui.crc_label_pattern_size.setText(str(circle["pattern"]["size"]))

    dialog.ui.crc_hslider_pattern_rotation.setValue(circle["pattern"]["rotation"])
    dialog.ui.crc_label_pattern_rotation.setText(str(circle["pattern"]["rotation"]))

    dialog.ui.crc_hslider_pattern_xshift.setValue(circle["pattern"]["xshift"]*2)
    dialog.ui.crc_label_pattern_xshift.setText(str(circle["pattern"]["xshift"]))

    dialog.ui.crc_hslider_pattern_yshift.setValue(circle["pattern"]["yshift"]*2)
    dialog.ui.crc_label_pattern_yshift.setText(str(circle["pattern"]["yshift"]))

    dialog.ui.crc_hslider_fill_strength.setValue(circle["fill_strength"])
    dialog.ui.crc_label_fill_strength.setText(str(circle["fill_strength"]))
    dialog.ui.crc_hslider_fill_opacity.setValue(circle["fill_opacity"]*100)
    dialog.ui.crc_label_fill_opacity.setText(str(circle["fill_opacity"]))

    dialog.ui.crc_hslider_line_strength.setValue(circle["line_strength"])
    dialog.ui.crc_label_line_strength.setText(str(circle["line_strength"]))
    dialog.ui.crc_hslider_line_opacity.setValue(circle["line_opacity"]*100)
    dialog.ui.crc_label_line_opacity.setText(str(circle["line_opacity"]))

    if circle["type"] in ['arc']:
        dialog.ui.crc_hslider_o_arrow_length.setValue(circle["o_arrow"]["length"]*4)
        dialog.ui.crc_label_o_arrow_length.setText(str(circle["o_arrow"]["length"]))
        dialog.ui.crc_hslider_o_arrow_width.setValue(circle["o_arrow"]["width"]*4)
        dialog.ui.crc_label_o_arrow_width.setText(str(circle["o_arrow"]["width"]))
        if circle["o_arrow"]["reversed"] == True:
            dialog.ui.crc_checkb_o_arrow_reversed.setChecked(True)
        else:
            dialog.ui.crc_checkb_o_arrow_reversed.setChecked(False)
        dialog.ui.crc_hslider_d_arrow_length.setValue(circle["d_arrow"]["length"]*4)
        dialog.ui.crc_label_d_arrow_length.setText(str(circle["d_arrow"]["length"]))
        dialog.ui.crc_hslider_d_arrow_width.setValue(circle["d_arrow"]["width"]*4)
        dialog.ui.crc_label_d_arrow_width.setText(str(circle["d_arrow"]["width"]))
        if circle["d_arrow"]["reversed"] == True:
            dialog.ui.crc_checkb_d_arrow_reversed.setChecked(True)
        else:
            dialog.ui.crc_checkb_d_arrow_reversed.setChecked(False)

    dialog.ui.textBrowser_2.setText(circle_text(dialog.scene.eucl, circle["id"]))


def fill_polygon_fields(dialog):
    polygon = dialog.scene.eucl["polygons"][dialog.current_id]
    if polygon["type"] == 'polygon':
        dialog.ui.pol_rad_polygon.toggle()
    elif polygon["type"] == 'linestring':
        dialog.ui.pol_rad_linestring.toggle()

    if polygon["show"] == True:
        dialog.ui.pol_checkb_show_object.setChecked(True)
    else:
        dialog.ui.pol_checkb_show_object.setChecked(False)

    dialog.state_change_ignore = True
    dialog.ui.pol_cb_selector_line_stroke.setCurrentIndex(LINE_STROKES.index(polygon["line_stroke"]))
    dialog.ui.pol_cb_selector_decoration.setCurrentIndex(DECORATIONS.index(polygon["decoration"]["type"]))
    if polygon["curve"]["strategy"] != 'smooth':
        dialog.ui.pol_cb_selector_strategy.setCurrentIndex(STRATEGIES.index(polygon["curve"]["strategy"]))

    dialog.ui.pol_cb_selector_fill_colour_name.setCurrentIndex(COLOURS.index(polygon["fill_colour_name"]))
    dialog.ui.pol_cb_selector_line_colour_name.setCurrentIndex(COLOURS.index(polygon["line_colour_name"]))
    dialog.ui.pol_cb_selector_o_arrow_tip.setCurrentIndex(ARROW_TIPS.index(polygon["o_arrow"]["tip"]))
    dialog.ui.pol_cb_selector_o_arrow_side.setCurrentIndex(ARROW_SIDES.index(polygon["o_arrow"]["side"]))
    dialog.ui.pol_cb_selector_d_arrow_tip.setCurrentIndex(ARROW_TIPS.index(polygon["d_arrow"]["tip"]))
    dialog.ui.pol_cb_selector_d_arrow_side.setCurrentIndex(ARROW_SIDES.index(polygon["d_arrow"]["side"]))
    dialog.ui.pol_cb_selector_pattern_name.setCurrentIndex(PATTERN_TYPES.index(polygon["pattern"]["type"]))
    dialog.state_change_ignore = False

    dialog.ui.pol_hslider_line_width.setValue(polygon["line_width"]*5)
    dialog.ui.pol_label_line_width.setText(str(polygon["line_width"]))

    if polygon["line_stroke"] != "custom":
        dialog.pol_le_line_stroke_custom.setEnabled(False)
    else:
        dialog.pol_le_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in polygon["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.pol_le_line_stroke_custom.setText(lengths_str)

    dialog.ui.pol_hslider_amplitude.setValue(polygon["decoration"]["amplitude"]*5)
    dialog.ui.pol_label_amplitude.setText(str(polygon["decoration"]["amplitude"]))

    dialog.ui.pol_hslider_wave_length.setValue(polygon["decoration"]["wave_length"]*5)
    dialog.ui.pol_label_wave_length.setText(str(polygon["decoration"]["wave_length"]))

    dialog.ui.pol_le_decoration_text.setText(polygon["decoration"]["text"])

    dialog.ui.pol_hslider_out_angle.setValue(polygon["curve"]["out_angle"])
    dialog.ui.pol_label_out_angle.setText(str(polygon["curve"]["out_angle"]))

    dialog.ui.pol_hslider_in_angle.setValue(polygon["curve"]["in_angle"])
    dialog.ui.pol_label_in_angle.setText(str(polygon["curve"]["in_angle"]))

    dialog.ui.pol_hslider_bend_angle.setValue(polygon["curve"]["bend_angle"])
    dialog.ui.pol_label_bend_angle.setText(str(polygon["curve"]["bend_angle"]))

    dialog.ui.pol_hslider_corner.setValue(polygon["curve"]["corner_radius"])
    dialog.ui.pol_label_corner.setText(str(polygon["curve"]["corner_radius"]))

    dialog.ui.pol_hslider_loop_size.setValue(polygon["curve"]["loop_size"])
    dialog.ui.pol_label_loop_size.setText(str(polygon["curve"]["loop_size"]))

    if polygon["curve"]["loop"] == True:
        dialog.ui.pol_checkb_loop.setChecked(True)
    else:
        dialog.ui.pol_checkb_loop.setChecked(False)

    dialog.ui.pol_hslider_fill_strength.setValue(polygon["fill_strength"])
    dialog.ui.pol_label_fill_strength.setText(str(polygon["fill_strength"]))
    dialog.ui.pol_hslider_fill_opacity.setValue(polygon["fill_opacity"]*100)
    dialog.ui.pol_label_fill_opacity.setText(str(polygon["fill_opacity"]))

    dialog.ui.pol_hslider_line_strength.setValue(polygon["line_strength"])
    dialog.ui.pol_label_line_strength.setText(str(polygon["line_strength"]))
    dialog.ui.pol_hslider_line_opacity.setValue(polygon["line_opacity"]*100)
    dialog.ui.pol_label_line_opacity.setText(str(polygon["line_opacity"]))

    dialog.ui.pol_hslider_o_arrow_length.setValue(polygon["o_arrow"]["length"]*4)
    dialog.ui.pol_label_o_arrow_length.setText(str(polygon["o_arrow"]["length"]))
    dialog.ui.pol_hslider_o_arrow_width.setValue(polygon["o_arrow"]["width"]*4)
    dialog.ui.pol_label_o_arrow_width.setText(str(polygon["o_arrow"]["width"]))
    if polygon["o_arrow"]["reversed"] == True:
        dialog.ui.pol_checkb_o_arrow_reversed.setChecked(True)
    else:
        dialog.ui.pol_checkb_o_arrow_reversed.setChecked(False)
    dialog.ui.pol_hslider_d_arrow_length.setValue(polygon["d_arrow"]["length"]*4)
    dialog.ui.pol_label_d_arrow_length.setText(str(polygon["d_arrow"]["length"]))
    dialog.ui.pol_hslider_d_arrow_width.setValue(polygon["d_arrow"]["width"]*4)
    dialog.ui.pol_label_d_arrow_width.setText(str(polygon["d_arrow"]["width"]))
    if polygon["d_arrow"]["reversed"] == True:
        dialog.ui.pol_checkb_d_arrow_reversed.setChecked(True)
    else:
        dialog.ui.pol_checkb_d_arrow_reversed.setChecked(False)

    dialog.ui.pol_hslider_pattern_distance.setValue(polygon["pattern"]["distance"]*2)
    dialog.ui.pol_label_pattern_distance.setText(str(polygon["pattern"]["distance"]))

    dialog.ui.pol_hslider_pattern_size.setValue(polygon["pattern"]["size"]*5)
    dialog.ui.pol_label_pattern_size.setText(str(polygon["pattern"]["size"]))

    dialog.ui.pol_hslider_pattern_rotation.setValue(polygon["pattern"]["rotation"])
    dialog.ui.pol_label_pattern_rotation.setText(str(polygon["pattern"]["rotation"]))

    dialog.ui.pol_hslider_pattern_xshift.setValue(polygon["pattern"]["xshift"]*2)
    dialog.ui.pol_label_pattern_xshift.setText(str(polygon["pattern"]["xshift"]))

    dialog.ui.pol_hslider_pattern_yshift.setValue(polygon["pattern"]["yshift"]*2)
    dialog.ui.pol_label_pattern_yshift.setText(str(polygon["pattern"]["yshift"]))


def fill_function_fields(dialog):
    function = dialog.scene.eucl["functions"][dialog.current_id]

    dialog.ui.fct_label_id.setText(str(function["id"]))
    if function["show"] == True:
        dialog.ui.fct_checkb_show_function.setChecked(True)
    else:
        dialog.ui.fct_checkb_show_function.setChecked(False)

    if function["type"] in ['polar', 'parametric']:
        dialog.ui.sum_group.setEnabled(False)
    else:
        dialog.ui.sum_group.setEnabled(True)

    dialog.state_change_ignore = True
    dialog.ui.fct_cb_selector_line_stroke.setCurrentIndex(LINE_STROKES.index(function["line_stroke"]))
    dialog.ui.fct_cb_selector_sum_type.setCurrentIndex(FUNCTION_TYPES.index(function["sum"]["type"]))
    dialog.ui.fct_cb_selector_sum_fill_colour_name.setCurrentIndex(MARKER_COLOURS.index(function["sum"]["fill_colour_name"]))
    dialog.ui.fct_cb_selector_sum_line_colour_name.setCurrentIndex(COLOURS.index(function["sum"]["line_colour_name"]))
    dialog.ui.fct_cb_selector_line_colour_name.setCurrentIndex(COLOURS.index(function["line_colour_name"]))
    dialog.ui.fct_cb_selector_fill_colour_name.setCurrentIndex(COLOURS.index(function["fill_colour_name"]))
    dialog.ui.fct_cb_selector_o_arrow_tip.setCurrentIndex(ARROW_TIPS.index(function["o_arrow"]["tip"]))
    dialog.ui.fct_cb_selector_o_arrow_side.setCurrentIndex(ARROW_SIDES.index(function["o_arrow"]["side"]))
    dialog.ui.fct_cb_selector_d_arrow_tip.setCurrentIndex(ARROW_TIPS.index(function["d_arrow"]["tip"]))
    dialog.ui.fct_cb_selector_d_arrow_side.setCurrentIndex(ARROW_SIDES.index(function["d_arrow"]["side"]))
    dialog.ui.fct_cb_selector_pattern_name.setCurrentIndex(PATTERN_TYPES.index(function["pattern"]["type"]))
    dialog.ui.fct_cb_selector_pattern_between.clear()
    if function["type"] == 'yfx':
        func_between_items = [-1]
        dialog.ui.fct_cb_selector_pattern_between.addItem('none')
        for func in dialog.scene.eucl["functions"]:
            if func["type"] == 'yfx' and func["id"] != 'fct_default' and func["id"] != function["id"]:
                dialog.ui.fct_cb_selector_pattern_between.addItem(str(func["def"]))
                func_between_items.append(func["id"])
        if function["id"] != 'fct_default':
            dialog.ui.fct_cb_selector_pattern_between.setCurrentIndex(func_between_items.index(function["between"]))
    dialog.state_change_ignore = False




    dialog.ui.fct_hslider_line_strength.setValue(function["line_strength"])
    dialog.ui.fct_label_line_strength.setText(str(function["line_strength"]))
    dialog.ui.fct_hslider_line_opacity.setValue(function["line_opacity"]*100)
    dialog.ui.fct_label_line_opacity.setText(str(function["line_opacity"]))

    dialog.ui.fct_hslider_fill_strength.setValue(function["fill_strength"])
    dialog.ui.fct_label_fill_strength.setText(str(function["fill_strength"]))
    dialog.ui.fct_hslider_fill_opacity.setValue(function["fill_opacity"]*100)
    dialog.ui.fct_label_fill_opacity.setText(str(function["fill_opacity"]))

    dialog.ui.fct_hslider_line_width.setValue(function["line_width"]*5)
    dialog.ui.fct_label_line_width.setText(str(function["line_width"]))

    dialog.ui.fct_hslider_samples.setValue(function["samples"])
    dialog.ui.fct_label_samples.setText(str(function["samples"]))

    if function["line_stroke"] != "custom":
        dialog.fct_le_line_stroke_custom.setEnabled(False)
    else:
        dialog.fct_le_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in function["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.fct_le_line_stroke_custom.setText(lengths_str)

    dialog.ui.fct_le_function_def.setText(function["def"])
    dialog.ui.fct_le_start.setText("%s" % function["domain_start"])
    dialog.ui.fct_le_end.setText("%s" % function["domain_end"])

    dialog.ui.fct_hslider_o_arrow_length.setValue(function["o_arrow"]["length"]*4)
    dialog.ui.fct_label_o_arrow_length.setText(str(function["o_arrow"]["length"]))
    dialog.ui.fct_hslider_o_arrow_width.setValue(function["o_arrow"]["width"]*4)
    dialog.ui.fct_label_o_arrow_width.setText(str(function["o_arrow"]["width"]))
    if function["o_arrow"]["reversed"] == True:
        dialog.ui.fct_checkb_o_arrow_reversed.setChecked(True)
    else:
        dialog.ui.fct_checkb_o_arrow_reversed.setChecked(False)
    dialog.ui.fct_hslider_d_arrow_length.setValue(function["d_arrow"]["length"]*4)
    dialog.ui.fct_label_d_arrow_length.setText(str(function["d_arrow"]["length"]))
    dialog.ui.fct_hslider_d_arrow_width.setValue(function["d_arrow"]["width"]*4)
    dialog.ui.fct_label_d_arrow_width.setText(str(function["d_arrow"]["width"]))
    if function["d_arrow"]["reversed"] == True:
        dialog.ui.fct_checkb_d_arrow_reversed.setChecked(True)
    else:
        dialog.ui.fct_checkb_d_arrow_reversed.setChecked(False)

    dialog.ui.fct_le_sum_start.setText("%s" % function["sum"]["start"])
    dialog.ui.fct_le_sum_end.setText("%s" % function["sum"]["end"])

    dialog.ui.fct_hslider_sum_number.setValue(function["sum"]["number"])
    dialog.ui.fct_label_sum_number.setText(str(function["sum"]["number"]))

    dialog.ui.fct_hslider_sum_fill_strength.setValue(function["sum"]["fill_strength"])
    dialog.ui.fct_label_sum_fill_strength.setText(str(function["sum"]["fill_strength"]))
    dialog.ui.fct_hslider_sum_fill_opacity.setValue(function["sum"]["fill_opacity"]*100)
    dialog.ui.fct_label_sum_fill_opacity.setText(str(function["sum"]["fill_opacity"]))

    dialog.ui.fct_hslider_sum_line_strength.setValue(function["sum"]["line_strength"])
    dialog.ui.fct_label_sum_line_strength.setText(str(function["sum"]["line_strength"]))
    dialog.ui.fct_hslider_sum_line_opacity.setValue(function["sum"]["line_opacity"]*100)
    dialog.ui.fct_label_sum_line_opacity.setText(str(function["sum"]["line_opacity"]))

    dialog.ui.fct_hslider_pattern_distance.setValue(function["pattern"]["distance"]*2)
    dialog.ui.fct_label_pattern_distance.setText(str(function["pattern"]["distance"]))

    dialog.ui.fct_hslider_pattern_size.setValue(function["pattern"]["size"]*5)
    dialog.ui.fct_label_pattern_size.setText(str(function["pattern"]["size"]))

    dialog.ui.fct_hslider_pattern_rotation.setValue(function["pattern"]["rotation"])
    dialog.ui.fct_label_pattern_rotation.setText(str(function["pattern"]["rotation"]))

    dialog.ui.fct_hslider_pattern_xshift.setValue(function["pattern"]["xshift"]*2)
    dialog.ui.fct_label_pattern_xshift.setText(str(function["pattern"]["xshift"]))

    dialog.ui.fct_hslider_pattern_yshift.setValue(function["pattern"]["yshift"]*2)
    dialog.ui.fct_label_pattern_yshift.setText(str(function["pattern"]["yshift"]))

    dialog.ui.fct_le_fill_start.setText("%s" % function["area_start"])
    dialog.ui.fct_le_fill_end.setText("%s" % function["area_end"])


def fill_axes_fields(dialog):
    grid = dialog.scene.eucl["grid"]
    axis = dialog.scene.eucl["axis"]
    axis_x = dialog.scene.eucl["axis_x"]
    axis_y = dialog.scene.eucl["axis_y"]

    #GRID

    if grid["show"] == True:
        dialog.ui.axe_checkb_show_grid.setChecked(True)
    else:
        dialog.ui.axe_checkb_show_grid.setChecked(False)

    dialog.state_change_ignore = True
    dialog.ui.axe_cb_selector_subdivisions_x.setCurrentIndex(list(range(1,11)).index(grid["sub_x"]))
    dialog.ui.axe_cb_selector_subdivisions_y.setCurrentIndex(list(range(1,11)).index(grid["sub_y"]))
    dialog.ui.axe_cb_selector_grid_line_colour_name.setCurrentIndex(COLOURS.index(grid["line_colour_name"]))
    dialog.ui.axe_cb_selector_divisions_line_stroke.setCurrentIndex(LINE_STROKES.index(grid["line_stroke"]))
    dialog.ui.axe_cb_selector_subdivisions_line_stroke.setCurrentIndex(LINE_STROKES.index(grid["sub_line_stroke"]))

    dialog.ui.axe_cb_selector_axes_line_colour_name.setCurrentIndex(COLOURS.index(axis["line_colour_name"]))
    dialog.ui.axe_cb_selector_label_font_size.setCurrentIndex(FONT_SIZES.index(axis["labels"]["size"]))

    dialog.ui.axe_cb_selector_label_anchor_x.setCurrentIndex(DIRECTIONS.index(axis_x["label"]["anchor"]))
    dialog.ui.axe_cb_selector_x_arrow_tip.setCurrentIndex(ARROW_TIPS.index(axis_x["o_arrow"]["tip"]))
    dialog.ui.axe_cb_selector_x_arrow_side.setCurrentIndex(ARROW_SIDES.index(axis_x["o_arrow"]["side"]))
    dialog.ui.axe_cb_selector_x_arrow_orient.setCurrentIndex(TRUE_FALSE.index(axis_x["o_arrow"]["direction"]))
    dialog.ui.axe_cb_selector_trig_x.setCurrentIndex(FRACTIONS.index(axis_x["trig"]))
    dialog.ui.axe_cb_selector_frac_x.setCurrentIndex(FRACTIONS.index(axis_x["frac"]))

    dialog.ui.axe_cb_selector_label_anchor_y.setCurrentIndex(DIRECTIONS.index(axis_y["label"]["anchor"]))
    dialog.ui.axe_cb_selector_y_arrow_tip.setCurrentIndex(ARROW_TIPS.index(axis_y["o_arrow"]["tip"]))
    dialog.ui.axe_cb_selector_y_arrow_side.setCurrentIndex(ARROW_SIDES.index(axis_y["o_arrow"]["side"]))
    dialog.ui.axe_cb_selector_y_arrow_orient.setCurrentIndex(TRUE_FALSE.index(axis_y["o_arrow"]["direction"]))
    dialog.ui.axe_cb_selector_trig_y.setCurrentIndex(FRACTIONS.index(axis_y["trig"]))
    dialog.ui.axe_cb_selector_frac_y.setCurrentIndex(FRACTIONS.index(axis_y["frac"]))
    dialog.state_change_ignore = False

    dialog.ui.axe_hslider_grid_line_opacity.setValue(grid["line_opacity"]*100)
    dialog.ui.axe_label_grid_line_opacity.setText(str(grid["line_opacity"]))

    dialog.ui.axe_hslider_grid_line_width.setValue(grid["line_width"]*5)
    dialog.ui.axe_label_grid_line_width.setText(str(grid["line_width"]))

    if grid["line_stroke"] != "custom":
        dialog.axe_le_divisions_line_stroke_custom.setEnabled(False)
    else:
        dialog.axe_le_divisions_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in grid["line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.axe_le_divisions_line_stroke_custom.setText(lengths_str)

    if grid["line_stroke"] != "custom":
        dialog.axe_le_subdivisions_line_stroke_custom.setEnabled(False)
    else:
        dialog.axe_le_subdivisions_line_stroke_custom.setEnabled(True)
    lengths_str = ''
    for num in grid["sub_line_stroke_custom"]:
        lengths_str += "%s " % str(num)
    lengths_str = lengths_str[:-1]
    dialog.ui.axe_le_subdivisions_line_stroke_custom.setText(lengths_str)

    #AXES

    dialog.ui.axe_hslider_axes_line_strength.setValue(axis["line_strength"])
    dialog.ui.axe_label_axes_line_strength.setText(str(axis["line_strength"]))
    dialog.ui.axe_hslider_axes_line_width.setValue(axis["line_width"]*5)
    dialog.ui.axe_label_axes_line_width.setText(str(axis["line_width"]))
    dialog.ui.axe_hslider_rotate_x_labels.setValue(axis["labels"]["x_rotate"])
    dialog.ui.axe_label_rotate_x_labels.setText(str(axis["labels"]["x_rotate"]))
    dialog.ui.axe_hslider_axes_x_below.setValue(axis["labels"]["x_below"]*5)
    dialog.ui.axe_label_axes_x_below.setText(str(axis["labels"]["x_below"]))

    #AXES X

    if axis_x["show"] == True:
        dialog.ui.axe_checkb_show_x_axis.setChecked(True)
    else:
        dialog.ui.axe_checkb_show_x_axis.setChecked(False)
    if axis_x["is_tick"] == True:
        dialog.ui.axe_checkb_ticks_x.setChecked(True)
    else:
        dialog.ui.axe_checkb_ticks_x.setChecked(False)
    if axis_x["is_numprint"] == True:
        dialog.ui.axe_checkb_numprint_x.setChecked(True)
    else:
        dialog.ui.axe_checkb_numprint_x.setChecked(False)
    if axis_x["is_orig"] == True:
        dialog.ui.axe_checkb_orig_x.setChecked(True)
    else:
        dialog.ui.axe_checkb_orig_x.setChecked(False)
    dialog.ui.axe_le_name_x.setText(axis_x["label"]["text"])
    dialog.ui.axe_hslider_label_distance_x.setValue(axis_x["label"]["distance"]*100)
    dialog.ui.axe_label_label_distance_x.setText(str(axis_x["label"]["distance"]))
    if axis_x["labels"]["show"] == True:
        dialog.ui.axe_checkb_show_x_labels.setChecked(True)
    else:
        dialog.ui.axe_checkb_show_x_labels.setChecked(False)
    dialog.ui.axe_hslider_x_arrow_length.setValue(axis_x["o_arrow"]["length"]*4)
    dialog.ui.axe_label_x_arrow_length.setText(str(axis_x["o_arrow"]["length"]))
    dialog.ui.axe_hslider_x_arrow_width.setValue(axis_x["o_arrow"]["width"]*4)
    dialog.ui.axe_label_x_arrow_width.setText(str(axis_x["o_arrow"]["width"]))
    if axis_x["o_arrow"]["reversed"] == True:
        dialog.ui.axe_checkb_x_arrow_reversed.setChecked(True)
    else:
        dialog.ui.axe_checkb_x_arrow_reversed.setChecked(False)
    dialog.ui.axe_hslider_x_tick_up.setValue(axis_x["tick_up"]*5)
    dialog.ui.axe_label_x_tick_up.setText(str(axis_x["tick_up"]))
    dialog.ui.axe_hslider_x_tick_down.setValue(axis_x["tick_down"]*5)
    dialog.ui.axe_label_x_tick_down.setText(str(axis_x["tick_down"]))
    dialog.ui.axe_hslider_x_tick_width.setValue(axis_x["tick_width"]*5)
    dialog.ui.axe_label_x_tick_width.setText(str(axis_x["tick_width"]))

    #AXES Y

    if axis_y["show"] == True:
        dialog.ui.axe_checkb_show_y_axis.setChecked(True)
    else:
        dialog.ui.axe_checkb_show_y_axis.setChecked(False)
    if axis_y["is_tick"] == True:
        dialog.ui.axe_checkb_ticks_y.setChecked(True)
    else:
        dialog.ui.axe_checkb_ticks_y.setChecked(False)
    if axis_y["is_numprint"] == True:
        dialog.ui.axe_checkb_numprint_y.setChecked(True)
    else:
        dialog.ui.axe_checkb_numprint_y.setChecked(False)
    if axis_y["is_orig"] == True:
        dialog.ui.axe_checkb_orig_y.setChecked(True)
    else:
        dialog.ui.axe_checkb_orig_y.setChecked(False)
    dialog.ui.axe_le_name_y.setText(axis_y["label"]["text"])
    dialog.ui.axe_hslider_label_distance_y.setValue(axis_y["label"]["distance"]*100)
    dialog.ui.axe_label_label_distance_y.setText(str(axis_y["label"]["distance"]))
    if axis_y["labels"]["show"] == True:
        dialog.ui.axe_checkb_show_y_labels.setChecked(True)
    else:
        dialog.ui.axe_checkb_show_y_labels.setChecked(False)
    dialog.ui.axe_hslider_y_arrow_length.setValue(axis_y["o_arrow"]["length"]*4)
    dialog.ui.axe_label_y_arrow_length.setText(str(axis_y["o_arrow"]["length"]))
    dialog.ui.axe_hslider_y_arrow_width.setValue(axis_y["o_arrow"]["width"]*4)
    dialog.ui.axe_label_y_arrow_width.setText(str(axis_y["o_arrow"]["width"]))
    if axis_y["o_arrow"]["reversed"] == True:
        dialog.ui.axe_checkb_y_arrow_reversed.setChecked(True)
    else:
        dialog.ui.axe_checkb_y_arrow_reversed.setChecked(False)
    dialog.ui.axe_hslider_y_tick_left.setValue(axis_y["tick_up"]*5)
    dialog.ui.axe_label_y_tick_left.setText(str(axis_y["tick_up"]))
    dialog.ui.axe_hslider_y_tick_right.setValue(axis_y["tick_down"]*5)
    dialog.ui.axe_label_y_tick_right.setText(str(axis_y["tick_down"]))
    dialog.ui.axe_hslider_y_tick_width.setValue(axis_y["tick_width"]*5)
    dialog.ui.axe_label_y_tick_width.setText(str(axis_y["tick_width"]))


def fill_settings_fields(dialog):
    eucl = dialog.scene.eucl
    settings = dialog.scene.settings
    dialog.ui.set_le_latex_command.setText(settings['latex'])
    dialog.ui.set_le_pdf_to_jpg_command.setText(settings['pdf to jpg'])
    dialog.ui.set_le_aspect_ratio.setText(dialog.scene.aspect_ratio)
    if dialog.scene.aspect_ratio_indicator:
        dialog.ui.set_checkb_aspect_ratio_indicator.setChecked(True)
    else:
        dialog.ui.set_checkb_aspect_ratio_indicator.setChecked(False)
    dialog.state_change_ignore = True
    dialog.ui.set_cb_selector_bg_colour.setCurrentIndex(MIX_COLOURS.index(eucl["bg_colour_name"]))
    dialog.state_change_ignore = False
    dialog.ui.set_hslider_bg_colour_strength.setValue(eucl["bg_colour_strength"])
    dialog.ui.set_label_bg_colour_strength.setText(str(eucl["bg_colour_strength"]))
    dialog.ui.set_edit_before.setText(eucl["code_before"])
    dialog.ui.set_edit_after.setText(eucl["code_after"])




def fill_fields(dialog):
    if dialog.tab_index == 0:
        fill_point_fields(dialog)
    elif dialog.tab_index == 1:
        fill_segment_fields(dialog)
    elif dialog.tab_index == 2:
        fill_circle_fields(dialog)
    elif dialog.tab_index == 3:
        fill_angle_fields(dialog)
    elif dialog.tab_index == 4:
        fill_polygon_fields(dialog)
    elif dialog.tab_index == 5:
        fill_function_fields(dialog)
    elif dialog.tab_index == 7:
        fill_axes_fields(dialog)
    elif dialog.tab_index == 8:
        fill_settings_fields(dialog)


class PropertiesDialog(QtWidgets.QDialog):
    def __init__ (self, scene):
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
        if not self.state_change_ignore:
            my_object[last_property] = selected_value
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
            fill_fields(self)
            self.ui.tabWidget.setFocus()

    def hslider_moved_new(self, my_object, last_property, value, label_to_set, factor=1):
        my_object[last_property] = value/factor
        label_to_set.setText(str(value/factor))

    def hslider_release_new(self):
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.ui.tabWidget.setFocus()





    def id_selected(self, value):
        self.current_id = value
        fill_fields(self)

    def pt_le_id_editing_finished(self):
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
                if soj.point_change_id(self.scene.eucl, point["id"], self.ui.pt_le_id.text(), self.scene.mapped_points) != False:
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

    def axe_hslider_moved(self, value, type, property, label_to_set, factor=1, secondary_property=None):
        my_object = self.scene.eucl[type]
        if secondary_property is None:
            my_object[property] = value/factor
        else:
            my_object[property][secondary_property] = value/factor
        label_to_set.setText(str(value/factor))

    def axe_hslider_release(self):
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.ui.tabWidget.setFocus()

    def axe_cb_selector_current_idx_changed(self, value, type, vlist, property, secondary_property=None):
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
        self.scene.eucl["angles"][self.current_id]["right_angle"] = True
        self.scene.eucl["angles"][self.current_id]["type"] = DEFAULT_RIGHT_ANGLE_TYPE
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
    def rad_german_right_clicked(self):
        self.scene.eucl["angles"][self.current_id]["right_angle"] = True
        self.scene.eucl["angles"][self.current_id]["type"] = 'german'
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
    def rad_arbitrary_clicked(self):
        self.scene.eucl["angles"][self.current_id]["right_angle"] = False
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def rad_polygon_clicked(self):
        self.scene.eucl["polygons"][self.current_id]["type"] = 'polygon'
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
    def rad_linestring_clicked(self):
        self.scene.eucl["polygons"][self.current_id]["type"] = 'linestring'
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()

    def keyPressEvent(self,event):
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
        # this performs autocompile when f5 is pressed
        elif event.matches(QtGui.QKeySequence.Refresh):
            previous_autocompile = self.scene.autocompile
            self.scene.autocompile = True
            self.scene.compile_tkz_and_render()
            self.scene.autocompile = previous_autocompile
        elif event.matches(QtGui.QKeySequence.Save):
            soj.save_eucl_file('data.json', self.scene.eucl)
        elif event.matches(QtGui.QKeySequence.Delete):
            if self.tab_index == 0 and self.pt_cb_selector.currentRow() > 0:
                soj.delete_point(self.scene.eucl, self.pt_cb_selector.currentRow(), self.scene.mapped_points)
                self.current_id = 0
                add_objects_to_combobox(self)
                print("here")
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
        self.scene.settings["latex"] = self.ui.set_le_latex_command.text()
        with open('settings.txt', 'w') as outfile:
            json.dump(self.scene.settings, outfile, indent=4)

    def set_le_pdf_to_jpg_command_changed(self):
        self.scene.settings["pdf to jpg"] = self.ui.set_le_pdf_to_jpg_command.text()
        with open('settings.txt', 'w') as outfile:
            json.dump(self.scene.settings, outfile, indent=4)

    def set_checkb_aspect_ratio_indicator_changed(self, state):
        if state == QtCore.Qt.Unchecked:
            self.scene.aspect_ratio_indicator = False
        else:
            self.scene.aspect_ratio_indicator = True
        always_on_drawing_plan(self.scene)
        always_off_drawing_plan(self.scene)

    def set_le_aspect_ratio_editingFinished(self):
        try:
            _ = eval(self.ui.set_le_aspect_ratio.text())
            self.scene.aspect_ratio = self.ui.set_le_aspect_ratio.text()
        except:
            self.ui.set_le_aspect_ratio.setText("16/9")
            self.scene.aspect_ratio = "16/9"
        always_on_drawing_plan(self.scene)
        always_off_drawing_plan(self.scene)

    def before_after_textChanged(self, my_object, last_property, text_edit):
        my_object[last_property] = text_edit.toPlainText()

    def set_pb_editingFinished_clicked(self, button):
        button.setFocus()
        self.scene.compile_tkz_and_render()
        if self.scene.undo_history[-1]["code_before"] == self.scene.eucl["code_before"] or\
        self.scene.undo_history[-1]["code_after"] == self.scene.eucl["code_after"]:
            self.scene.add_new_undo_item()
        always_on_drawing_plan(self.scene)
        always_off_drawing_plan(self.scene)

    def package_list_updated(self, newitem):
        for i in range(self.ui.set_cb_selector.count()):
            self.scene.eucl["packages"][i] = self.ui.set_cb_selector.item(i).text()

    def add_new_package(self):
        selector = self.ui.set_cb_selector
        if selector.item(selector.count() - 1).text() != '':
            item = QtWidgets.QListWidgetItem('')
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            selector.addItem(item)
            if selector.count() > len(self.scene.eucl["packages"]):
                self.scene.eucl["packages"].append('')

    def delete_package(self):
        current_row = self.ui.set_cb_selector.currentRow()
        if current_row > 5:
            self.ui.set_cb_selector.takeItem(current_row)
            del self.scene.eucl["packages"][current_row]


    def open_duck_dialog(self):
        dialog = duck_properties.DuckPropertiesDialog(self.scene, self.current_id)
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()


#
