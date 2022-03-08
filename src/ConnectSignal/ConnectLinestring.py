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
    connect_dash,
    connect_o_arrow,
    connect_d_arrow
)


def connect_linestring(scene):
    scene.ui.linestring_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.linestring_line_width_spin))
    scene.ui.linestring_line_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    connect_dash(scene, ['line' 'dash'], scene.ui.linestring_line_stroke, scene.ui.linestring_custom_dash)

    connect_decoration(scene, ["line", "decoration"],
        scene.ui.linestring_decoration_type,
        scene.ui.linestring_amplitude_spin, scene.ui.linestring_amplitude_slider,
        scene.ui.linestring_wavelength_spin, scene.ui.linestring_wavelength_slider,
        scene.ui.linestring_decoration_text)

    connect_colour(scene, ['line', 'colour'],
        scene.ui.linestring_border_colour_name,
        scene.ui.linestring_border_colour_mix_name,
        scene.ui.linestring_border_colour_mixratio_spin,
        scene.ui.linestring_border_colour_mixratio_slider,
        scene.ui.linestring_border_colour_strength_spin,
        scene.ui.linestring_border_colour_strength_slider)

    connect_o_arrow(scene,
        scene.ui.linestring_o_tip,
        scene.ui.linestring_o_side,
        scene.ui.linestring_o_reversed,
        scene.ui.linestring_o_length_spin,
        scene.ui.linestring_o_length_slider,
        scene.ui.linestring_o_width_spin,
        scene.ui.linestring_o_width_slider)

    connect_d_arrow(scene,
        scene.ui.linestring_d_tip,
        scene.ui.linestring_d_side,
        scene.ui.linestring_d_reversed,
        scene.ui.linestring_d_length_spin,
        scene.ui.linestring_d_length_slider,
        scene.ui.linestring_d_width_spin,
        scene.ui.linestring_d_width_slider)

    scene.ui.linestring_def_str.editingFinished.connect(
        lambda : connect_def_str_lineedit_abstract(scene, scene.ui.linestring_def_str))
