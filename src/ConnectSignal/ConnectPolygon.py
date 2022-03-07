import Constant as c
from ConnectSignal.Lambda import (
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract,
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_dash_lineedit_abstract,
    connect_lineedit_abstract,
    connect_def_str_lineedit_abstract
)

from ConnectSignal.ConnectMacros import (
    connect_colour,
    connect_fill_pattern,
    connect_decoration,
    connect_dash
)


def connect_polygon(scene):
    scene.ui.polygon_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.polygon_line_width_spin))
    scene.ui.polygon_line_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    connect_colour(scene, ['fill', 'colour'],
        scene.ui.polygon_marker_colour_name,
        scene.ui.polygon_marker_colour_mix_name,
        scene.ui.polygon_marker_colour_mixratio_spin,
        scene.ui.polygon_marker_colour_mixratio_slider,
        scene.ui.polygon_marker_colour_strength_spin,
        scene.ui.polygon_marker_colour_strength_slider)

    connect_dash(scene, ['line' 'dash'], scene.ui.polygon_line_stroke, scene.ui.polygon_custom_dash)

    connect_fill_pattern(scene, ['fill', 'pattern'],
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

    connect_decoration(scene, ["line", "decoration"],
        scene.ui.polygon_decoration_type,
        scene.ui.polygon_amplitude_spin, scene.ui.polygon_amplitude_slider,
        scene.ui.polygon_wavelength_spin, scene.ui.polygon_wavelength_slider,
        scene.ui.polygon_decoration_text)

    connect_colour(scene, ['line', 'colour'],
        scene.ui.polygon_border_colour_name,
        scene.ui.polygon_border_colour_mix_name,
        scene.ui.polygon_border_colour_mixratio_spin,
        scene.ui.polygon_border_colour_mixratio_slider,
        scene.ui.polygon_border_colour_strength_spin,
        scene.ui.polygon_border_colour_strength_slider)

    scene.ui.polygon_def_str.editingFinished.connect(
        lambda : connect_def_str_lineedit_abstract(scene, scene.ui.polygon_def_str))
