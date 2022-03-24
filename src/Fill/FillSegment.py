import Constant as c
from Colour import Colour
from Fill.FillMacros import (
    fill_o_arrow,
    fill_d_arrow,
    fill_colour,
    fill_dash
)


def fill_segment_fields(scene):
    """Fill all widgets in the segment tab."""
    colours = c.attribute_values(c.Colour)\
        + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'segment':
        return
    segment = scene.project_data.items[ids[0]].item

    scene.ui.segment_def_str.setText(scene.project_data.items[ids[0]].definition_string())
    scene.ui.segment_line_width_slider.setValue(10.0 * segment["line"]["line_width"])
    scene.ui.segment_line_width_spin.setValue(segment["line"]["line_width"])

    scene.skip_combobox_changes = True
    scene.ui.segment_o_connect_to.setCurrentIndex(c.attribute_values(c.LineConnectTo).index(segment["line"]["o_connect_to"]))
    scene.ui.segment_d_connect_to.setCurrentIndex(c.attribute_values(c.LineConnectTo).index(segment["line"]["d_connect_to"]))
    scene.ui.segment_marker_symbol.setCurrentIndex(c.attribute_values(c.SegmentMarkerType).index(segment["marker"]["symbol"]))
    scene.skip_combobox_changes = False

    scene.ui.segment_double_distance_slider.setValue(10.0 * segment["line"]["double"]["distance"])
    scene.ui.segment_double_distance_spin.setValue(segment["line"]["double"]["distance"])

    scene.ui.segment_o_extension_slider.setValue(66.6+33.3*segment["line"]["o_extension"])
    scene.ui.segment_o_extension_spin.setValue(segment["line"]["o_extension"])

    scene.ui.segment_d_extension_slider.setValue(33.3*segment["line"]["d_extension"])
    scene.ui.segment_d_extension_spin.setValue(segment["line"]["d_extension"])

    scene.ui.segment_marker_width_slider.setValue(10.0*segment["marker"]["width"])
    scene.ui.segment_marker_width_spin.setValue(segment["marker"]["width"])

    scene.ui.segment_marker_size_slider.setValue(10.0*segment["marker"]["size"])
    scene.ui.segment_marker_size_spin.setValue(segment["marker"]["size"])

    scene.ui.segment_marker_position_slider.setValue(100.0*segment["marker"]["position"])
    scene.ui.segment_marker_position_spin.setValue(segment["marker"]["position"])

    fill_o_arrow(scene, segment,
        scene.ui.segment_o_tip,
        scene.ui.segment_o_side,
        scene.ui.segment_o_reversed,
        scene.ui.segment_o_length_spin,
        scene.ui.segment_o_length_slider,
        scene.ui.segment_o_width_spin,
        scene.ui.segment_o_width_slider)

    fill_d_arrow(scene, segment,
        scene.ui.segment_d_tip,
        scene.ui.segment_d_side,
        scene.ui.segment_d_reversed,
        scene.ui.segment_d_length_spin,
        scene.ui.segment_d_length_slider,
        scene.ui.segment_d_width_spin,
        scene.ui.segment_d_width_slider)

    fill_dash(scene, segment["line"]["dash"], scene.ui.segment_line_stroke, scene.ui.segment_custom_dash)

    fill_colour(scene, segment["line"]["colour"], colours,
        scene.ui.segment_colour_name,
        scene.ui.segment_colour_mix_name,
        scene.ui.segment_colour_mixratio_spin,
        scene.ui.segment_colour_mixratio_slider,
        scene.ui.segment_colour_strength_spin,
        scene.ui.segment_colour_strength_slider)

    fill_colour(scene, segment["line"]["double"]["colour"], colours,
        scene.ui.segment_double_colour_name,
        scene.ui.segment_double_colour_mix_name,
        scene.ui.segment_double_colour_mixratio_spin,
        scene.ui.segment_double_colour_mixratio_slider,
        scene.ui.segment_double_colour_strength_spin,
        scene.ui.segment_double_colour_strength_slider)
