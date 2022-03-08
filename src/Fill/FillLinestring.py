import Constant as c
from Colour import Colour
from Fill.FillMacros import (
    fill_colour,
    fill_fill_pattern,
    fill_decoration,
    fill_dash,
    fill_o_arrow,
    fill_d_arrow
)


def fill_linestring_fields(scene):
    colours = c.attribute_values(c.Colour)\
        + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'linestring':
        return
    linestring = scene.project_data.items[ids[0]].item

    scene.ui.linestring_def_str.setText(scene.project_data.items[ids[0]].definition_string())

    scene.ui.linestring_line_width_slider.setValue(10.0 * linestring["line"]["line_width"])
    scene.ui.linestring_line_width_spin.setValue(linestring["line"]["line_width"])

    fill_dash(scene, linestring["line"]["dash"], scene.ui.linestring_line_stroke, scene.ui.linestring_custom_dash)

    fill_colour(scene, linestring["line"]["colour"], colours,
        scene.ui.linestring_border_colour_name,
        scene.ui.linestring_border_colour_mix_name,
        scene.ui.linestring_border_colour_mixratio_spin,
        scene.ui.linestring_border_colour_mixratio_slider,
        scene.ui.linestring_border_colour_strength_spin,
        scene.ui.linestring_border_colour_strength_slider)

    fill_decoration(scene, linestring["line"]["decoration"],
        scene.ui.linestring_decoration_type,
        scene.ui.linestring_amplitude_spin, scene.ui.linestring_amplitude_slider,
        scene.ui.linestring_wavelength_spin, scene.ui.linestring_wavelength_slider,
        scene.ui.linestring_decoration_text)

    fill_o_arrow(scene, linestring,
        scene.ui.linestring_o_tip,
        scene.ui.linestring_o_side,
        scene.ui.linestring_o_reversed,
        scene.ui.linestring_o_length_spin,
        scene.ui.linestring_o_length_slider,
        scene.ui.linestring_o_width_spin,
        scene.ui.linestring_o_width_slider)

    fill_d_arrow(scene, linestring,
        scene.ui.linestring_d_tip,
        scene.ui.linestring_d_side,
        scene.ui.linestring_d_reversed,
        scene.ui.linestring_d_length_spin,
        scene.ui.linestring_d_length_slider,
        scene.ui.linestring_d_width_spin,
        scene.ui.linestring_d_width_slider)
