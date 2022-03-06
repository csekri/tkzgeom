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

from ConnectSignal.ConnectMacros import connect_colour
from ConnectSignal.Lambda import connect_def_str_lineedit_abstract


def connect_circle(scene):
    # scene.ui.point_line_width_slider.sliderMoved.connect(
    #     lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda x: x/10.0, scene.ui.point_line_width_spin))
    # scene.ui.point_line_width_slider.sliderReleased.connect(
    #     lambda : connect_slider_released_abstract(scene))
    #
    # scene.ui.point_custom_dash.editingFinished.connect(
    #     lambda : connect_dash_lineedit_abstract(scene, ['line', 'dash'], 'custom_pattern', scene.ui.point_custom_dash))
    #
    # scene.ui.point_line_stroke.currentIndexChanged.connect(
    #     lambda x: connect_combobox_abstract(x, scene, ['line', 'dash'], 'stroke', c.attribute_values(c.Line_Stroke)))

    # connect_colour(scene, ['fill', 'colour'],
    #     scene.ui.point_marker_colour_name,
    #     scene.ui.point_marker_colour_mix_name,
    #     scene.ui.point_marker_colour_mixratio_spin,
    #     scene.ui.point_marker_colour_mixratio_slider,
    #     scene.ui.point_marker_colour_strength_spin,
    #     scene.ui.point_marker_colour_strength_slider)
    #
    # connect_colour(scene, ['line', 'colour'],
    #     scene.ui.point_border_colour_name,
    #     scene.ui.point_border_colour_mix_name,
    #     scene.ui.point_border_colour_mixratio_spin,
    #     scene.ui.point_border_colour_mixratio_slider,
    #     scene.ui.point_border_colour_strength_spin,
    #     scene.ui.point_border_colour_strength_slider)

    scene.ui.circle_def_str.editingFinished.connect(
        lambda : connect_def_str_lineedit_abstract(scene, scene.ui.circle_def_str))
