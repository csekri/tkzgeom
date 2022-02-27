import Constant as c
from Colour import Colour
from Fill.FillMacros import (
    fill_o_arrow,
    fill_d_arrow,
    fill_colour)

def fill_segment_fields(scene):
    colours = c.attribute_values(c.Colour)\
        + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'segment':
        return
    segment = scene.project_data.items[ids[0]].item

    scene.ui.segment_line_width_slider.setValue(10.0 * segment["line"]["line_width"])
    scene.ui.segment_line_width_spin.setValue(segment["line"]["line_width"])

    scene.skip_combobox_changes = True
    scene.ui.segment_line_stroke.setCurrentIndex(c.attribute_values(c.Line_Stroke).index(segment["line"]["dash"]["stroke"]))
    scene.skip_combobox_changes = False

    scene.ui.segment_custom_dash.setText(' '.join(map(str, segment["line"]["dash"]["custom_pattern"])))

    scene.ui.segment_double_distance_slider.setValue(10.0 * segment["line"]["double"]["distance"])
    scene.ui.segment_double_distance_spin.setValue(segment["line"]["double"]["distance"])

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

    fill_colour(scene, segment["line"]["colour"], colours,
        scene.ui.segment_colour_name,
        scene.ui.segment_colour_mix_name,
        scene.ui.segment_colour_mixratio_spin,
        scene.ui.segment_colour_mixratio_slider,
        scene.ui.segment_colour_strength_spin,
        scene.ui.segment_colour_strength_slider)
