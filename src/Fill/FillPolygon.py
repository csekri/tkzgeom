import Constant as c
from Colour import Colour
from Fill.FillMacros import (
    fill_colour,
    fill_fill_pattern,
    fill_decoration,
    fill_dash,
    fill_strategy
)


def fill_polygon_fields(scene):
    """Fill all widgets in the polygon tab."""
    colours = c.attribute_values(c.Colour)\
        + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'polygon':
        return
    polygon = scene.project_data.items[ids[0]].item

    scene.ui.polygon_def_str.setText(scene.project_data.items[ids[0]].definition_string())
    scene.ui.polygon_name.setText(polygon["id"])

    scene.ui.polygon_line_width_slider.setValue(int(10.0 * polygon["line"]["line_width"]))
    scene.ui.polygon_line_width_spin.setValue(int(polygon["line"]["line_width"]))

    fill_colour(scene, polygon["fill"]["colour"], colours,
        scene.ui.polygon_marker_colour_name,
        scene.ui.polygon_marker_colour_mix_name,
        scene.ui.polygon_marker_colour_mixratio_spin,
        scene.ui.polygon_marker_colour_mixratio_slider,
        scene.ui.polygon_marker_colour_strength_spin,
        scene.ui.polygon_marker_colour_strength_slider)

    fill_dash(scene, polygon["line"]["dash"], scene.ui.polygon_line_stroke, scene.ui.polygon_custom_dash)

    fill_fill_pattern(scene, polygon["fill"]["pattern"],
        scene.ui.polygon_pattern_type,
        scene.ui.polygon_pattern_distance_spin,
        scene.ui.polygon_pattern_distance_slider,
        scene.ui.polygon_pattern_size_spin,
        scene.ui.polygon_pattern_size_slider,
        scene.ui.polygon_pattern_rotation_spin,
        scene.ui.polygon_pattern_rotation_slider,
        scene.ui.polygon_pattern_xshift_spin,
        scene.ui.polygon_pattern_xshift_slider,
        scene.ui.polygon_pattern_yshift_spin,
        scene.ui.polygon_pattern_yshift_slider)

    fill_colour(scene, polygon["line"]["colour"], colours,
        scene.ui.polygon_border_colour_name,
        scene.ui.polygon_border_colour_mix_name,
        scene.ui.polygon_border_colour_mixratio_spin,
        scene.ui.polygon_border_colour_mixratio_slider,
        scene.ui.polygon_border_colour_strength_spin,
        scene.ui.polygon_border_colour_strength_slider)

    fill_decoration(scene, polygon["line"]["decoration"],
        scene.ui.polygon_decoration_type,
        scene.ui.polygon_amplitude_spin, scene.ui.polygon_amplitude_slider,
        scene.ui.polygon_wavelength_spin, scene.ui.polygon_wavelength_slider,
        scene.ui.polygon_decoration_text)

    fill_strategy(scene, polygon,
        scene.ui.polygon_tabWidget,
        scene.ui.polygon_connect_link,
        scene.ui.polygon_rounded_corners_spin, scene.ui.polygon_rounded_corners_slider,
        scene.ui.polygon_o_angle_spin, scene.ui.polygon_o_angle_slider,
        scene.ui.polygon_d_angle_spin, scene.ui.polygon_d_angle_slider,
        scene.ui.polygon_bend_direction,
        scene.ui.polygon_bend_angle_spin, scene.ui.polygon_bend_angle_slider,
        scene.ui.polygon_smooth_tension_spin, scene.ui.polygon_smooth_tension_slider)
