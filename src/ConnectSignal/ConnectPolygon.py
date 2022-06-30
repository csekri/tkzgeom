from ConnectSignal.Lambda import (
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_def_str_lineedit_abstract,
    connect_name_change_abstract,
    connect_spinbox_editing_finished_abstract,
    connect_spinbox_value_changed_abstract
)

from ConnectSignal.ConnectMacros import (
    connect_colour,
    connect_fill_pattern,
    connect_decoration,
    connect_dash,
    connect_strategy
)


def connect_polygon(scene):
    """Connect signals in the polygon tab."""
    scene.ui.polygon_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.polygon_line_width_spin))
    scene.ui.polygon_line_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.polygon_line_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line'], 'line_width', scene.ui.polygon_line_width_spin))
    scene.ui.polygon_line_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    connect_colour(
        scene, ['fill', 'colour'],
        scene.ui.polygon_marker_colour_name,
        scene.ui.polygon_marker_colour_mix_name,
        scene.ui.polygon_marker_colour_mixratio_spin,
        scene.ui.polygon_marker_colour_mixratio_slider,
        scene.ui.polygon_marker_colour_strength_spin,
        scene.ui.polygon_marker_colour_strength_slider)

    connect_dash(scene, ['line' 'dash'], scene.ui.polygon_line_stroke, scene.ui.polygon_custom_dash)

    connect_fill_pattern(
        scene, ['fill', 'pattern'],
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

    connect_decoration(
        scene, ["line", "decoration"],
        scene.ui.polygon_decoration_type,
        scene.ui.polygon_amplitude_spin, scene.ui.polygon_amplitude_slider,
        scene.ui.polygon_wavelength_spin, scene.ui.polygon_wavelength_slider,
        scene.ui.polygon_decoration_text)

    connect_colour(
        scene, ['line', 'colour'],
        scene.ui.polygon_border_colour_name,
        scene.ui.polygon_border_colour_mix_name,
        scene.ui.polygon_border_colour_mixratio_spin,
        scene.ui.polygon_border_colour_mixratio_slider,
        scene.ui.polygon_border_colour_strength_spin,
        scene.ui.polygon_border_colour_strength_slider)

    connect_strategy(
        scene, ['line', 'strategy'],
        scene.ui.polygon_tabWidget,
        scene.ui.polygon_connect_link,
        scene.ui.polygon_rounded_corners_spin, scene.ui.polygon_rounded_corners_slider,
        scene.ui.polygon_o_angle_spin, scene.ui.polygon_o_angle_slider,
        scene.ui.polygon_d_angle_spin, scene.ui.polygon_d_angle_slider,
        scene.ui.polygon_bend_direction,
        scene.ui.polygon_bend_angle_spin, scene.ui.polygon_bend_angle_slider,
        scene.ui.polygon_smooth_tension_spin, scene.ui.polygon_smooth_tension_slider)

    scene.ui.polygon_def_str.editingFinished.connect(
        lambda: connect_def_str_lineedit_abstract(scene, scene.ui.polygon_def_str))
    scene.ui.polygon_name.editingFinished.connect(
        lambda: connect_name_change_abstract(scene.ui.polygon_name, scene))
