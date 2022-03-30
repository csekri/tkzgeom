import Constant as c
from Colour import Colour
from Fill.FillMacros import (
    fill_colour,
    fill_decoration,
    fill_dash,
    fill_o_arrow,
    fill_d_arrow,
    fill_strategy
)


def fill_linestring_fields(scene):
    """Fill all widgets in the linestring tab."""
    colours = c.attribute_values(c.Colour)\
        + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'linestring':
        return
    linestring = scene.project_data.items[ids[0]].item

    scene.ui.linestring_def_str.setText(scene.project_data.items[ids[0]].definition_string())
    scene.ui.linestring_name.setText(linestring["id"])

    scene.ui.linestring_line_width_slider.setValue(10.0 * linestring["line"]["line_width"])
    scene.ui.linestring_line_width_spin.setValue(linestring["line"]["line_width"])

    scene.skip_combobox_changes = True
    scene.ui.linestring_connect_to.setCurrentIndex(c.attribute_values(c.LineConnectTo).index(linestring["line"]["connect_to"]))
    scene.skip_combobox_changes = False

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

    fill_strategy(scene, linestring,
        scene.ui.linestring_tabWidget,
        scene.ui.linestring_connect_link,
        scene.ui.linestring_rounded_corners_spin, scene.ui.linestring_rounded_corners_slider,
        scene.ui.linestring_o_angle_spin, scene.ui.linestring_o_angle_slider,
        scene.ui.linestring_d_angle_spin, scene.ui.linestring_d_angle_slider,
        scene.ui.linestring_bend_direction,
        scene.ui.linestring_bend_angle_spin, scene.ui.linestring_bend_angle_slider,
        scene.ui.linestring_smooth_tension_spin, scene.ui.linestring_smooth_tension_slider)

    scene.ui.linestring_loop_size_slider.setValue(10.0 * linestring["line"]["strategy"]["loop_size"])
    scene.ui.linestring_loop_size_spin.setValue(linestring["line"]["strategy"]["loop_size"])

    scene.skip_checkox_changes = True
    scene.ui.linestring_loop.setChecked(linestring["line"]["strategy"]["loop"])
    scene.ui.linestring_o_arrow_bending.setChecked(linestring["o_arrow"]["bending"])
    scene.ui.linestring_d_arrow_bending.setChecked(linestring["d_arrow"]["bending"])
    scene.skip_checkox_changes = False
