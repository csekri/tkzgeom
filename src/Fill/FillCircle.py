import Constant as c
from Colour import Colour
from Fill.FillMacros import (
    fill_fill_pattern,
    fill_d_arrow,
    fill_colour,
    fill_dash
)


def fill_circle_fields(scene):
    colours = c.attribute_values(c.Colour)\
        + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'circle':
        return
    circle = scene.project_data.items[ids[0]].item

    scene.ui.circle_def_str.setText(scene.project_data.items[ids[0]].definition_string())

    fill_fill_pattern(scene, circle["fill"]["pattern"],
        scene.ui.circle_pattern_type,
        scene.ui.circle_pattern_distance_spin,
        scene.ui.circle_pattern_distance_slider,
        scene.ui.circle_pattern_size_spin,
        scene.ui.circle_pattern_size_slider,
        scene.ui.circle_pattern_rotation_spin,
        scene.ui.circle_pattern_rotation_slider,
        scene.ui.circle_pattern_xshift_spin,
        scene.ui.circle_pattern_xshift_slider,
        scene.ui.circle_pattern_yshift_spin,
        scene.ui.circle_pattern_yshift_slider)

    fill_colour(scene, circle["fill"]["colour"], colours,
        scene.ui.circle_marker_colour_name,
        scene.ui.circle_marker_colour_mix_name,
        scene.ui.circle_marker_colour_mixratio_spin,
        scene.ui.circle_marker_colour_mixratio_slider,
        scene.ui.circle_marker_colour_strength_spin,
        scene.ui.circle_marker_colour_strength_slider)

    fill_colour(scene, circle["line"]["colour"], colours,
        scene.ui.circle_border_colour_name,
        scene.ui.circle_border_colour_mix_name,
        scene.ui.circle_border_colour_mixratio_spin,
        scene.ui.circle_border_colour_mixratio_slider,
        scene.ui.circle_border_colour_strength_spin,
        scene.ui.circle_border_colour_strength_slider)

    fill_colour(scene, circle["line"]["double"]["colour"], colours,
        scene.ui.circle_double_colour_name,
        scene.ui.circle_double_colour_mix_name,
        scene.ui.circle_double_colour_mixratio_spin,
        scene.ui.circle_double_colour_mixratio_slider,
        scene.ui.circle_double_colour_strength_spin,
        scene.ui.circle_double_colour_strength_slider)

    fill_dash(scene, circle["line"]["dash"], scene.ui.circle_line_stroke, scene.ui.circle_custom_dash)

    scene.ui.circle_double_distance_slider.setValue(10.0 * circle["line"]["double"]["distance"])
    scene.ui.circle_double_distance_spin.setValue(circle["line"]["double"]["distance"])
