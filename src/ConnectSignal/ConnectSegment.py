import Constant as c
from ConnectSignal.Lambda import (
    connect_combobox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_def_str_lineedit_abstract,
    connect_name_change_abstract,
    connect_checkbox_abstract
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
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.segment_line_width_spin))
    scene.ui.segment_line_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.segment_double_distance_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line', 'double'], 'distance', lambda x: x/10.0, scene.ui.segment_double_distance_spin))
    scene.ui.segment_double_distance_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.segment_o_extension_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'o_extension', lambda x: x/33.3-2.0, scene.ui.segment_o_extension_spin))
    scene.ui.segment_o_extension_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.segment_d_extension_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'd_extension', lambda x: x/33.3, scene.ui.segment_d_extension_spin))
    scene.ui.segment_d_extension_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.segment_o_connect_to.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line'], 'o_connect_to', c.attribute_values(c.LineConnectTo)))
    scene.ui.segment_d_connect_to.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line'], 'd_connect_to', c.attribute_values(c.LineConnectTo)))

    scene.ui.segment_marker_symbol.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['marker'], 'symbol', c.attribute_values(c.SegmentMarkerType)))

    scene.ui.segment_marker_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'width', lambda x: x/10.0, scene.ui.segment_marker_width_spin))
    scene.ui.segment_marker_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.segment_marker_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'size', lambda x: x/10.0, scene.ui.segment_marker_size_spin))
    scene.ui.segment_marker_size_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.segment_marker_position_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'position', lambda x: x/100.0, scene.ui.segment_marker_position_spin))
    scene.ui.segment_marker_position_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    connect_o_arrow(scene,
        scene.ui.segment_o_tip,
        scene.ui.segment_o_side,
        scene.ui.segment_o_reversed,
        scene.ui.segment_o_length_spin,
        scene.ui.segment_o_length_slider,
        scene.ui.segment_o_width_spin,
        scene.ui.segment_o_width_slider)

    connect_d_arrow(scene,
        scene.ui.segment_d_tip,
        scene.ui.segment_d_side,
        scene.ui.segment_d_reversed,
        scene.ui.segment_d_length_spin,
        scene.ui.segment_d_length_slider,
        scene.ui.segment_d_width_spin,
        scene.ui.segment_d_width_slider)

    connect_dash(scene, ['line' 'dash'], scene.ui.segment_line_stroke, scene.ui.segment_custom_dash)

    connect_colour(scene, ['line', 'colour'],
        scene.ui.segment_colour_name,
        scene.ui.segment_colour_mix_name,
        scene.ui.segment_colour_mixratio_spin,
        scene.ui.segment_colour_mixratio_slider,
        scene.ui.segment_colour_strength_spin,
        scene.ui.segment_colour_strength_slider)

    connect_colour(scene, ['line', 'double', 'colour'],
        scene.ui.segment_double_colour_name,
        scene.ui.segment_double_colour_mix_name,
        scene.ui.segment_double_colour_mixratio_spin,
        scene.ui.segment_double_colour_mixratio_slider,
        scene.ui.segment_double_colour_strength_spin,
        scene.ui.segment_double_colour_strength_slider)

    scene.ui.segment_def_str.editingFinished.connect(
        lambda : connect_def_str_lineedit_abstract(scene, scene.ui.segment_def_str))
