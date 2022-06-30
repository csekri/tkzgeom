import Constant as c
from ConnectSignal.Lambda import (
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_def_str_lineedit_abstract,
    connect_name_change_abstract
)

from ConnectSignal.ConnectMacros import (
    connect_colour,
    connect_decoration,
    connect_dash,
    connect_o_arrow,
    connect_d_arrow,
    connect_strategy,
    connect_spinbox_editing_finished_abstract,
    connect_spinbox_value_changed_abstract
)


def connect_linestring(scene):
    """Connect signals in the linestring tab."""
    scene.ui.linestring_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.linestring_line_width_spin))
    scene.ui.linestring_line_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.linestring_line_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line'], 'line_width', scene.ui.linestring_line_width_spin))
    scene.ui.linestring_line_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.linestring_connect_to.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line'], 'connect_to', c.attribute_values(c.LineConnectTo)))

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

    connect_strategy(scene, ['line', 'strategy'],
        scene.ui.linestring_tabWidget,
        scene.ui.linestring_connect_link,
        scene.ui.linestring_rounded_corners_spin, scene.ui.linestring_rounded_corners_slider,
        scene.ui.linestring_o_angle_spin, scene.ui.linestring_o_angle_slider,
        scene.ui.linestring_d_angle_spin, scene.ui.linestring_d_angle_slider,
        scene.ui.linestring_bend_direction,
        scene.ui.linestring_bend_angle_spin, scene.ui.linestring_bend_angle_slider,
        scene.ui.linestring_smooth_tension_spin, scene.ui.linestring_smooth_tension_slider)

    scene.ui.linestring_loop_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line', 'strategy'], 'loop_size', lambda x: x/10.0, scene.ui.linestring_loop_size_spin))
    scene.ui.linestring_loop_size_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.linestring_loop_size_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line', 'strategy'], 'loop_size', scene.ui.linestring_loop_size_spin))
    scene.ui.linestring_loop_size_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.linestring_loop.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['line', 'strategy'], 'loop'))

    scene.ui.linestring_o_arrow_bending.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['o_arrow'], 'bending'))

    scene.ui.linestring_d_arrow_bending.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['d_arrow'], 'bending'))

    scene.ui.linestring_def_str.editingFinished.connect(
        lambda: connect_def_str_lineedit_abstract(scene, scene.ui.linestring_def_str))
    scene.ui.linestring_name.editingFinished.connect(
        lambda: connect_name_change_abstract(scene.ui.linestring_name, scene))
