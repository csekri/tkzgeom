import Constant as c
from ConnectSignal.Lambda import (
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract,
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_dash_lineedit_abstract,
    connect_lineedit_abstract
)

from ConnectSignal.ConnectMacros import (
    connect_colour,
    connect_fill_pattern,
    connect_dash,
    connect_o_arrow,
    connect_d_arrow
)
from ConnectSignal.Lambda import connect_def_str_lineedit_abstract


def connect_circle(scene):
    scene.ui.circle_def_str.editingFinished.connect(
        lambda : connect_def_str_lineedit_abstract(scene, scene.ui.circle_def_str))

    scene.ui.circle_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.circle_line_width_spin))
    scene.ui.circle_line_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.circle_double_distance_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line', 'double'], 'distance', lambda x: x/10.0, scene.ui.circle_double_distance_spin))
    scene.ui.circle_double_distance_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    connect_fill_pattern(scene, ['fill', 'pattern'],
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

    connect_colour(scene, ['fill', 'colour'],
        scene.ui.circle_marker_colour_name,
        scene.ui.circle_marker_colour_mix_name,
        scene.ui.circle_marker_colour_mixratio_spin,
        scene.ui.circle_marker_colour_mixratio_slider,
        scene.ui.circle_marker_colour_strength_spin,
        scene.ui.circle_marker_colour_strength_slider)

    connect_colour(scene, ['line', 'colour'],
        scene.ui.circle_border_colour_name,
        scene.ui.circle_border_colour_mix_name,
        scene.ui.circle_border_colour_mixratio_spin,
        scene.ui.circle_border_colour_mixratio_slider,
        scene.ui.circle_border_colour_strength_spin,
        scene.ui.circle_border_colour_strength_slider)

    connect_colour(scene, ['line', 'double', 'colour'],
        scene.ui.circle_double_colour_name,
        scene.ui.circle_double_colour_mix_name,
        scene.ui.circle_double_colour_mixratio_spin,
        scene.ui.circle_double_colour_mixratio_slider,
        scene.ui.circle_double_colour_strength_spin,
        scene.ui.circle_double_colour_strength_slider)

    connect_o_arrow(scene,
        scene.ui.circle_o_tip,
        scene.ui.circle_o_side,
        scene.ui.circle_o_reversed,
        scene.ui.circle_o_length_spin,
        scene.ui.circle_o_length_slider,
        scene.ui.circle_o_width_spin,
        scene.ui.circle_o_width_slider)

    connect_d_arrow(scene,
        scene.ui.circle_d_tip,
        scene.ui.circle_d_side,
        scene.ui.circle_d_reversed,
        scene.ui.circle_d_length_spin,
        scene.ui.circle_d_length_slider,
        scene.ui.circle_d_width_spin,
        scene.ui.circle_d_width_slider)

    connect_dash(scene, ['line' 'dash'], scene.ui.circle_line_stroke, scene.ui.circle_custom_dash)