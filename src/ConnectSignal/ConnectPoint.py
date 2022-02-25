import Constant as c
from ConnectSignal.Lambda import (
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract,
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_dash_lineedit_abstract
)

def connect_point(scene):
    colours = c.attribute_values(c.Colour)\
        + [i["id"] for i in scene.project_data.colours]
    scene.ui.plainTextEdit.textChanged.connect(
        lambda : connect_plain_text_edit_abstract(scene, ['marker'], 'text', scene.ui.plainTextEdit))
    scene.ui.point_apply_text_change.clicked.connect(
        lambda : connect_text_edit_pushbutton_apply_abstract(scene))

    scene.ui.point_marker_colour_name.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['fill', 'colour'], 'name', colours))
    scene.ui.point_marker_colour_mix_name.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['fill', 'colour'], 'mix_with', colours))

    scene.ui.point_marker_shape.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['marker'], 'shape', c.attribute_values(c.Marker_Shape)))

    scene.ui.point_show_label.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['label'], 'show'))

    scene.ui.point_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'size', lambda x: x, scene.ui.point_size_spin))
    scene.ui.point_size_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.point_shape_number_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'shape_number', lambda x: x, scene.ui.point_shape_number_spin))
    scene.ui.point_shape_number_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.point_inner_sep_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'inner_sep', lambda x: x, scene.ui.point_inner_sep_spin))
    scene.ui.point_inner_sep_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.point_ratio_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['marker'], 'ratio', lambda x: 0.5+x/20, scene.ui.point_ratio_spin))
    scene.ui.point_ratio_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.point_marker_colour_mixratio_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['fill', 'colour'], 'mix_percent', lambda x: x, scene.ui.point_marker_colour_mixratio_spin))
    scene.ui.point_marker_colour_mixratio_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.point_marker_colour_strength_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['fill', 'colour'], 'strength', lambda x: x, scene.ui.point_marker_colour_strength_spin))
    scene.ui.point_marker_colour_strength_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    scene.ui.point_custom_dash.editingFinished.connect(
        lambda : connect_dash_lineedit_abstract(scene, ['line', 'dash'], 'custom_pattern', scene.ui.point_custom_dash))

    scene.ui.point_line_stroke.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line', 'dash'], 'stroke', c.attribute_values(c.Line_Stroke)))
