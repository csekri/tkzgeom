import Constant as c
from ConnectSignal.Lambda import (
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_lineedit_abstract,
    connect_dash_lineedit_abstract,
    connect_spinbox_value_changed_abstract,
    connect_spinbox_editing_finished_abstract
)


def connect_o_arrow(
        scene, ui_tip, ui_side, ui_reversed,
        ui_length_spin, ui_length_slider,
        ui_width_spin, ui_width_slider):
    """Connect origin arrow."""

    ui_tip.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['o_arrow'], 'tip', c.attribute_values(c.ArrowTip)))

    ui_side.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['o_arrow'], 'side', c.attribute_values(c.ArrowSide)))

    ui_length_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['o_arrow'], 'length', lambda y: y/10.0, ui_length_spin))
    ui_length_slider.sliderReleased.connect(
        lambda : connect_slider_released_abstract(scene))
    ui_length_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['o_arrow'], 'length', ui_length_spin))
    ui_length_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['o_arrow'], 'width', lambda y: y/10.0, ui_width_spin))
    ui_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['o_arrow'], 'width', ui_width_spin))
    ui_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_reversed.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['o_arrow'], 'reversed'))


def connect_d_arrow(
        scene, ui_tip, ui_side, ui_reversed,
        ui_length_spin, ui_length_slider,
        ui_width_spin, ui_width_slider):
    """Connect destination arrow."""

    ui_tip.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['d_arrow'], 'tip', c.attribute_values(c.ArrowTip)))

    ui_side.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['d_arrow'], 'side', c.attribute_values(c.ArrowSide)))

    ui_length_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['d_arrow'], 'length', lambda y: y/10.0, ui_length_spin))
    ui_length_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_length_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['d_arrow'], 'length', ui_length_spin))
    ui_length_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_width_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, ['d_arrow'], 'width', lambda y: y/10.0, ui_width_spin))
    ui_width_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_width_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, ['d_arrow'], 'width', ui_width_spin))
    ui_width_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_reversed.stateChanged.connect(
        lambda x: connect_checkbox_abstract(x, scene, ['d_arrow'], 'reversed'))


def connect_colour(
        scene, attributes, ui_name, ui_mix_with,
        ui_mix_spin, ui_mix_slider,
        ui_strength_spin, ui_strength_slider):
    """Connect colour."""
    ui_name.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'name', c.attribute_values(c.Colour), True))
    ui_mix_with.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'mix_with', c.attribute_values(c.Colour), True))

    ui_mix_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'mix_percent', lambda y: y, ui_mix_spin))
    ui_mix_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_mix_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'mix_percent', ui_mix_spin))
    ui_mix_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_strength_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'strength', lambda y: y, ui_strength_spin))
    ui_strength_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_strength_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'strength', ui_strength_spin))
    ui_strength_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))


def connect_fill_pattern(
        scene, attributes, ui_type,
        ui_distance_spin, ui_distance_slider,
        ui_size_spin, ui_size_slider,
        ui_rotation_spin, ui_rotation_slider,
        ui_xshift_spin, ui_xshift_slider,
        ui_yshift_spin, ui_yshift_slider):
    """Connect fill pattern."""
    ui_type.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'type', c.attribute_values(c.PatternType), True))

    ui_distance_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'distance', lambda y: y/10.0, ui_distance_spin))
    ui_distance_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_distance_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'distance', ui_distance_spin))
    ui_distance_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_size_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'size', lambda y: y/20.0, ui_size_spin))
    ui_size_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_size_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'size', ui_size_spin))
    ui_size_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_rotation_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'rotation', lambda y: y*1.8, ui_rotation_spin))
    ui_rotation_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_rotation_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'rotation', ui_rotation_spin))
    ui_rotation_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_xshift_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'xshift', lambda y: y/20.0, ui_xshift_spin))
    ui_xshift_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_xshift_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'xshift', ui_xshift_spin))
    ui_xshift_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_yshift_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'yshift', lambda y: y/20.0, ui_yshift_spin))
    ui_yshift_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_yshift_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'yshift', ui_yshift_spin))
    ui_yshift_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))


def connect_decoration(
        scene, attributes, ui_type,
        ui_amplitude_spin, ui_amplitude_slider,
        ui_wavelength_spin, ui_wavelength_slider,
        ui_text):
    """Connect decoration pattern."""
    ui_type.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'type', c.attribute_values(c.DecorationType), True))

    ui_amplitude_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'amplitude', lambda y: y/10.0, ui_amplitude_spin))
    ui_amplitude_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_amplitude_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'amplitude', ui_amplitude_spin))
    ui_amplitude_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_wavelength_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'wavelength', lambda y: y/10.0, ui_wavelength_spin))
    ui_wavelength_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_wavelength_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'wavelength', ui_wavelength_spin))
    ui_wavelength_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_text.editingFinished.connect(
        lambda: connect_lineedit_abstract(scene, attributes, 'text', ui_text))


def connect_dash(scene, attributes, ui_dash, ui_custom_stroke):  # TODO change ['line', 'dash'] to attributes
    """Connect dash pattern."""

    ui_custom_stroke.editingFinished.connect(
        lambda: connect_dash_lineedit_abstract(scene, ['line', 'dash'], 'custom_pattern', ui_custom_stroke))

    ui_dash.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, ['line', 'dash'], 'stroke', c.attribute_values(c.LineStroke)))


def connect_strategy(
        scene, attributes, ui_tabWidget, ui_connect_link,
        ui_rounded_corners_spin, ui_rounded_corners_slider,
        ui_out_angle_spin, ui_out_angle_slider,
        ui_in_angle_spin, ui_in_angle_slider,
        ui_bend_direction,
        ui_bend_angle_spin, ui_bend_angle_slider,
        ui_smooth_tension_spin, ui_smooth_tension_slider):
    """Connect curve strategy."""

    def tabWidget_func(index, scene):
        """Connect strategy tabWidget."""
        if not scene.skip_combobox_changes:
            ids = scene.list_focus_ids
            if not ids:
                return
            for id in ids:
                final_property = scene.project_data.items[id].item
                for prop in attributes:
                    final_property = final_property[prop]
                if index == 0:
                    final_property["type"] = c.attribute_values(c.StrategyType)[ui_connect_link.currentIndex()]
                elif index == 1:
                    final_property["type"] = c.StrategyType.IO_ANGLE
                elif index == 2:
                    final_property["type"] = c.StrategyType.BENDED_LEFT
                else:
                    final_property["type"] = c.StrategyType.SMOOTH
            scene.edit.add_undo_item(scene)

    def connect_bend_direction_func(index, scene):
        """Connect bend direction."""
        if not scene.skip_combobox_changes:
            ids = scene.list_focus_ids
            if not ids:
                return
            for id in ids:
                final_property = scene.project_data.items[id].item
                for prop in attributes:
                    final_property = final_property[prop]
                final_property["type"] = c.attribute_values(c.StrategyType)[index+4]
            scene.edit.add_undo_item(scene)

    ui_tabWidget.currentChanged.connect(lambda x: tabWidget_func(x, scene))

    ui_connect_link.currentIndexChanged.connect(
        lambda x: connect_combobox_abstract(x, scene, attributes, 'type', c.attribute_values(c.StrategyType), True))

    ui_bend_direction.currentIndexChanged.connect(
        lambda x: connect_bend_direction_func(x, scene))

    ui_in_angle_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'in_angle', lambda y: y*3.6, ui_in_angle_spin))
    ui_in_angle_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_in_angle_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'in_angle', ui_in_angle_spin))
    ui_in_angle_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_out_angle_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'out_angle', lambda y: y*3.6, ui_out_angle_spin))
    ui_out_angle_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_out_angle_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'out_angle', ui_out_angle_spin))
    ui_out_angle_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_rounded_corners_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'rounded_corners', lambda y: y/4.0, ui_rounded_corners_spin))
    ui_rounded_corners_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_rounded_corners_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'rounded_corners', ui_rounded_corners_spin))
    ui_rounded_corners_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_bend_angle_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'bend_angle', lambda y: y*3.6, ui_bend_angle_spin))
    ui_bend_angle_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_bend_angle_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'bend_angle', ui_bend_angle_spin))
    ui_bend_angle_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))

    ui_smooth_tension_slider.sliderMoved.connect(
        lambda x: connect_slider_moved_abstract(x, scene, attributes, 'smooth_tension', lambda y: y/50.0+0.2, ui_smooth_tension_spin))
    ui_smooth_tension_slider.sliderReleased.connect(
        lambda: connect_slider_released_abstract(scene))
    ui_smooth_tension_spin.valueChanged.connect(
        lambda x: connect_spinbox_value_changed_abstract(x, scene, attributes, 'smooth_tension', ui_smooth_tension_spin))
    ui_smooth_tension_spin.editingFinished.connect(
        lambda: connect_spinbox_editing_finished_abstract(scene))
