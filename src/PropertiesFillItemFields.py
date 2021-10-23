from Constants import *
from AddNewItem import get_item_from_id

def __circle_text(eucl, circle_id):
    """
    SUMMARY
        returns string which explains in English the definition of the given circle

    PARAMETERS
        eucl: project data
        circle_id: id of the circle in question

    RETURNS
        str
    """
    circle = get_item_from_id(eucl, circle_id, "c")
    if circle["id"] == 'crc_default':
        return ''
    text = CIRCLE_TEXT_DICT[circle["type"]]
    if circle["type"] == "circum_circle":
        text = text.replace('#1', circle["points"]["A"]+circle["points"]["B"]+circle["points"]["C"])
    elif circle["type"] == "two_point_circle":
        text = text.replace('#1', circle["points"]["O"])
        text = text.replace('#2', circle["points"]["A"]+circle["points"]["O"])
    elif circle["type"] == "inscribed_circle":
        text = text.replace('#1', circle["points"]["A"]+circle["points"]["B"]+circle["points"]["C"])
    elif circle["type"] == "arc":
        text = text.replace('#1', circle["points"]["O"])
        text = text.replace('#2', circle["points"]["A"])
        text = text.replace('#3', circle["points"]["B"])
    else: # circle["type"] == "sector":
        text = text.replace('#1', circle["points"]["O"])
        text = text.replace('#2', circle["points"]["A"])
        text = text.replace('#3', circle["points"]["B"])
    return text

def fill_point_fields(dialog):
    """
    SUMMARY
        fills all point widget fields with data for a given point

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
    def make_text(eucl, point):
        """
        SUMMARY
            returns string which explains in English the definition of the given point

        PARAMETERS
            eucl: project data
            point: point object in question

        RETURNS
            str
        """
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
            text = text.replace('#2', __circle_text(eucl, point["from"]["circle"]))
        elif point["from"]["type"] == "circle_midpoint":
            text = text.replace('#1', __circle_text(eucl, point["from"]["circle"]))
        elif point["from"]["type"] == "segment_midpoint":
            text = text.replace('#1', point["from"]["A"] + point["from"]["B"])
        elif point["from"]["type"] == "point_on_line":
            text = text.replace('#1', point["from"]["A"])
            text = text.replace('#2', point["from"]["ratio"])
            text = text.replace('#3', point["from"]["B"])
        elif point["from"]["type"] == "point_on_circle":
            text = text.replace('#1', __circle_text(eucl, point["from"]["circle"]))
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

    dialog.ui.textBrowser.setText(make_text(dialog.scene.eucl, point))



def fill_segment_fields(dialog):
    """
    SUMMARY
        fills all segment widget fields with data for a given segment

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
    """
    SUMMARY
        fills all angle widget fields with data for a given angle

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
    """
    SUMMARY
        fills all circle widget fields with data for a given circle

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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

    dialog.ui.textBrowser_2.setText(__circle_text(dialog.scene.eucl, circle["id"]))


def fill_polygon_fields(dialog):
    """
    SUMMARY
        fills all polygon widget fields with data for a given polygon

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
    """
    SUMMARY
        fills all function widget fields with data for a given function

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
    """
    SUMMARY
        fills all axes widget fields with data for a given axes

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
    """
    SUMMARY
        fills all settings widget fields with data

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
    """
    SUMMARY
        fills all widgets conditioned on the current tab index

    PARAMETERS
        dialog: PropertiesDialog

    RETURNS
        None
    """
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
