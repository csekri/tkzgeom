import Constant as c
from ConnectSignal.Lambda import (
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
)

def connect_o_arrow(scene, ui_tip, ui_side, ui_reversed,
        ui_length_spin, ui_length_slider,
        ui_width_spin, ui_width_slider):

    ui_tip.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['o_arrow'], 'tip', c.attribute_values(c.ArrowTip)))

    ui_side.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['o_arrow'], 'side', c.attribute_values(c.ArrowSide)))

    ui_length_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['o_arrow'], 'length', lambda x: x/10.0, ui_length_spin))
    ui_length_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['o_arrow'], 'width', lambda x: x/10.0, ui_width_spin))
    ui_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_reversed.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['o_arrow'], 'reversed'))


def connect_d_arrow(scene, ui_tip, ui_side, ui_reversed,
        ui_length_spin, ui_length_slider,
        ui_width_spin, ui_width_slider):

    ui_tip.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['d_arrow'], 'tip', c.attribute_values(c.ArrowTip)))

    ui_side.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['d_arrow'], 'side', c.attribute_values(c.ArrowSide)))

    ui_length_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['d_arrow'], 'length', lambda x: x/10.0, ui_length_spin))
    ui_length_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['d_arrow'], 'width', lambda x: x/10.0, ui_width_spin))
    ui_width_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_reversed.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['d_arrow'], 'reversed'))

def connect_colour(scene, attributes, ui_name, ui_mix_with,
        ui_mix_spin, ui_mix_slider,
        ui_strength_spin, ui_strength_slider):
    ui_name.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'name', c.attribute_values(c.Colour), True))
    ui_mix_with.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'mix_with', c.attribute_values(c.Colour), True))

    ui_mix_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'mix_percent', lambda x: x, ui_mix_spin))
    ui_mix_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_strength_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'strength', lambda x: x, ui_strength_spin))
    ui_strength_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

def connect_fill_pattern(scene, attributes, ui_type,
        ui_distance_spin, ui_distance_slider,
        ui_size_spin, ui_size_slider,
        ui_rotation_spin, ui_rotation_slider,
        ui_xshift_spin, ui_xshift_slider,
        ui_yshift_spin, ui_yshift_slider):

    ui_type.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'type', c.attribute_values(c.PatternType), True))

    ui_distance_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'distance', lambda x: x/10.0, ui_distance_spin))
    ui_distance_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'size', lambda x: x/20.0, ui_size_spin))
    ui_size_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_rotation_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'rotation', lambda x: x*1.8, ui_rotation_spin))
    ui_rotation_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_xshift_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'xshift', lambda x: x/20.0, ui_xshift_spin))
    ui_xshift_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))

    ui_yshift_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'yshift', lambda x: x/20.0, ui_yshift_spin))
    ui_yshift_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))





#
