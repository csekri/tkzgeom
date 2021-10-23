from Constants import *

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
