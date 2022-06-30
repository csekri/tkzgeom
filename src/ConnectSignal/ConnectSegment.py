import Constant as c
from ConnectSignal.Lambda import (
    connect_combobox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_def_str_lineedit_abstract,
    connect_name_change_abstract,
    connect_checkbox_abstract,
    connect_spinbox_value_changed_abstract,
    connect_spinbox_editing_finished_abstract
)

from ConnectSignal.ConnectMacros import (
    connect_o_arrow,
    connect_d_arrow,
    connect_colour,
    connect_dash
)


def connect_segment(scene):
    """Connect signals in the segment tab."""
    scene.ui.segment_name.editingFinished.connect(
        lambda: connect_name_change_abstract(scene.ui.segment_name, scene))

    scene.ui.segment_show.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, [], 'show'))

    scene.ui.segment_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda y: y/10.0, scene.ui.segment_line_width_spin))
    scene.ui.segment_line_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.segment_line_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line'], 'line_width', scene.ui.segment_line_width_spin))
    scene.ui.segment_line_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.segment_double_distance_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line', 'double'], 'distance', lambda y: y/10.0, scene.ui.segment_double_distance_spin))
    scene.ui.segment_double_distance_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.segment_double_distance_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line', 'double'], 'distance', scene.ui.segment_double_distance_spin))
    scene.ui.segment_double_distance_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.segment_o_extension_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'o_extension', lambda y: y/33.3-2.0, scene.ui.segment_o_extension_spin))
    scene.ui.segment_o_extension_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.segment_o_extension_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line'], 'o_extension', scene.ui.segment_o_extension_spin))
    scene.ui.segment_o_extension_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.segment_d_extension_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'd_extension', lambda y: y/33.3, scene.ui.segment_d_extension_spin))
    scene.ui.segment_d_extension_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))

    scene.ui.segment_o_connect_to.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line'], 'o_connect_to', c.attribute_values(c.LineConnectTo)))
    scene.ui.segment_d_connect_to.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line'], 'd_connect_to', c.attribute_values(c.LineConnectTo)))

    scene.ui.segment_marker_symbol.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['marker'], 'symbol', c.attribute_values(c.SegmentMarkerType)))

    scene.ui.segment_marker_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'width', lambda y: y/10.0, scene.ui.segment_marker_width_spin))
    scene.ui.segment_marker_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.segment_marker_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'width', scene.ui.segment_marker_width_spin))
    scene.ui.segment_marker_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.segment_marker_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'size', lambda y: y/10.0, scene.ui.segment_marker_size_spin))
    scene.ui.segment_marker_size_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.segment_marker_size_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'size', scene.ui.segment_marker_size_spin))
    scene.ui.segment_marker_size_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.segment_marker_position_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'position', lambda y: y/100.0, scene.ui.segment_marker_position_spin))
    scene.ui.segment_marker_position_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.segment_marker_position_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'size', scene.ui.segment_marker_position_spin))
    scene.ui.segment_marker_position_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    connect_o_arrow(
        scene,
        scene.ui.segment_o_tip,
        scene.ui.segment_o_side,
        scene.ui.segment_o_reversed,
        scene.ui.segment_o_length_spin,
        scene.ui.segment_o_length_slider,
        scene.ui.segment_o_width_spin,
        scene.ui.segment_o_width_slider)

    connect_d_arrow(
        scene,
        scene.ui.segment_d_tip,
        scene.ui.segment_d_side,
        scene.ui.segment_d_reversed,
        scene.ui.segment_d_length_spin,
        scene.ui.segment_d_length_slider,
        scene.ui.segment_d_width_spin,
        scene.ui.segment_d_width_slider)

    connect_dash(scene, ['line' 'dash'], scene.ui.segment_line_stroke, scene.ui.segment_custom_dash)

    connect_colour(
        scene,
        ['line', 'colour'],
        scene.ui.segment_colour_name,
        scene.ui.segment_colour_mix_name,
        scene.ui.segment_colour_mixratio_spin,
        scene.ui.segment_colour_mixratio_slider,
        scene.ui.segment_colour_strength_spin,
        scene.ui.segment_colour_strength_slider)

    connect_colour(
        scene,
        ['line', 'double', 'colour'],
        scene.ui.segment_double_colour_name,
        scene.ui.segment_double_colour_mix_name,
        scene.ui.segment_double_colour_mixratio_spin,
        scene.ui.segment_double_colour_mixratio_slider,
        scene.ui.segment_double_colour_strength_spin,
        scene.ui.segment_double_colour_strength_slider)

    scene.ui.segment_def_str.editingFinished.connect(
        lambda: connect_def_str_lineedit_abstract(scene, scene.ui.segment_def_str))
