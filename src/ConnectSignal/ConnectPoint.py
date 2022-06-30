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
    connect_name_change_abstract,
    connect_spinbox_value_changed_abstract,
    connect_spinbox_editing_finished_abstract
)

from ConnectSignal.ConnectMacros import connect_colour, connect_dash
from ConnectSignal.Lambda import connect_def_str_lineedit_abstract


def connect_point(scene):
    """Connect signals in the point tab."""
    scene.ui.point_name.editingFinished.connect(
        lambda: connect_name_change_abstract(scene.ui.point_name, scene))
    scene.ui.plainTextEdit.textChanged.connect(
        lambda: connect_plain_text_edit_abstract(scene, ['marker'], 'text', scene.ui.plainTextEdit))
    scene.ui.point_apply_text_change.clicked.connect(
        lambda: connect_text_edit_pushbutton_apply_abstract(scene))

    scene.ui.point_show.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, [], 'show'))

    scene.ui.point_marker_shape.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['marker'], 'shape', c.attribute_values(c.MarkerShape)))

    scene.ui.point_show_label.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['label'], 'show'))

    scene.ui.point_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'size', lambda y: y, scene.ui.point_size_spin))
    scene.ui.point_size_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_size_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'size', scene.ui.point_size_spin))
    scene.ui.point_size_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_shape_number_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'shape_number', lambda y: y,
                                                scene.ui.point_shape_number_spin))
    scene.ui.point_shape_number_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_shape_number_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'shape_number', scene.ui.point_shape_number_spin))
    scene.ui.point_shape_number_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_inner_sep_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'inner_sep', lambda y: y,
                                                scene.ui.point_inner_sep_spin))
    scene.ui.point_inner_sep_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_inner_sep_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'inner_sep', scene.ui.point_inner_sep_spin))
    scene.ui.point_inner_sep_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_ratio_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'ratio', lambda y: 0.5 + y / 20,
                                                scene.ui.point_ratio_spin))
    scene.ui.point_ratio_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_ratio_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'ratio', scene.ui.point_ratio_spin))
    scene.ui.point_ratio_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_text_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'text_width', lambda y: y,
                                                scene.ui.point_text_width_spin))
    scene.ui.point_text_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_text_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'text_width', scene.ui.point_text_width_spin))
    scene.ui.point_text_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_line_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['line'], 'line_width', lambda y: y / 10.0,
                                                scene.ui.point_line_width_spin))
    scene.ui.point_line_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_line_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['line'], 'line_width', scene.ui.point_line_width_spin))
    scene.ui.point_line_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_custom_dash.editingFinished.connect(
        lambda: connect_dash_lineedit_abstract(scene, ['line', 'dash'], 'custom_pattern', scene.ui.point_custom_dash))

    scene.ui.point_line_stroke.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line', 'dash'], 'stroke', c.attribute_values(c.LineStroke)))

    scene.ui.point_label_text.editingFinished.connect(
        lambda: connect_lineedit_abstract(scene, ['label'], 'text', scene.ui.point_label_text))

    scene.ui.point_anchor.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['label'], 'anchor', c.attribute_values(c.Direction)))

    scene.ui.point_offset_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['label'], 'offset', lambda y: y - 10,
                                                scene.ui.point_offset_spin))
    scene.ui.point_offset_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_offset_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['label'], 'offset', scene.ui.point_offset_spin))
    scene.ui.point_offset_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    scene.ui.point_rounded_corners_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'rounded_corners', lambda y: y / 4,
                                                scene.ui.point_rounded_corners_spin))
    scene.ui.point_rounded_corners_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    scene.ui.point_rounded_corners_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['marker'], 'rounded_corners', scene.ui.point_rounded_corners_spin))
    scene.ui.point_rounded_corners_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    connect_colour(scene, ['fill', 'colour'],
                   scene.ui.point_marker_colour_name,
                   scene.ui.point_marker_colour_mix_name,
                   scene.ui.point_marker_colour_mixratio_spin,
                   scene.ui.point_marker_colour_mixratio_slider,
                   scene.ui.point_marker_colour_strength_spin,
                   scene.ui.point_marker_colour_strength_slider)

    connect_dash(scene, ['line' 'dash'], scene.ui.point_line_stroke, scene.ui.point_custom_dash)

    connect_colour(scene, ['line', 'colour'],
                   scene.ui.point_border_colour_name,
                   scene.ui.point_border_colour_mix_name,
                   scene.ui.point_border_colour_mixratio_spin,
                   scene.ui.point_border_colour_mixratio_slider,
                   scene.ui.point_border_colour_strength_spin,
                   scene.ui.point_border_colour_strength_slider)

    scene.ui.point_def_str.editingFinished.connect(
        lambda: connect_def_str_lineedit_abstract(scene, scene.ui.point_def_str))
