import Constant as c

def fill_o_arrow(
        scene, item, ui_tip, ui_side, ui_reversed,
        ui_length_spin, ui_length_slider,
        ui_width_spin, ui_width_slider):
    scene.skip_combobox_changes = True
    ui_tip.setCurrentIndex(c.attribute_values(c.ArrowTip).index(item["o_arrow"]["tip"]))
    ui_side.setCurrentIndex(c.attribute_values(c.ArrowSide).index(item["o_arrow"]["side"]))
    scene.skip_combobox_changes = False

    ui_length_slider.setValue(10.0 * item["o_arrow"]["length"])
    ui_length_spin.setValue(item["o_arrow"]["length"])

    ui_width_slider.setValue(10.0 * item["o_arrow"]["width"])
    ui_width_spin.setValue(item["o_arrow"]["width"])

    scene.skip_checkbox_changes = True
    scene.ui.segment_o_reversed.setChecked(item["o_arrow"]["reversed"])
    scene.skip_checkbox_changes = False

def fill_d_arrow(
        scene, item, ui_tip, ui_side, ui_reversed,
        ui_length_spin, ui_length_slider,
        ui_width_spin, ui_width_slider):
    scene.skip_combobox_changes = True
    ui_tip.setCurrentIndex(c.attribute_values(c.ArrowTip).index(item["d_arrow"]["tip"]))
    ui_side.setCurrentIndex(c.attribute_values(c.ArrowSide).index(item["d_arrow"]["side"]))
    scene.skip_combobox_changes = False

    ui_length_slider.setValue(10.0 * item["d_arrow"]["length"])
    ui_length_spin.setValue(item["d_arrow"]["length"])

    ui_width_slider.setValue(10.0 * item["d_arrow"]["width"])
    ui_width_spin.setValue(item["d_arrow"]["width"])

    scene.skip_checkbox_changes = True
    scene.ui.segment_o_reversed.setChecked(item["d_arrow"]["reversed"])
    scene.skip_checkbox_changes = False

def fill_colour(
        scene, item, colours, ui_name, ui_mix_with,
        ui_mix_spin, ui_mix_slider,
        ui_strength_spin, ui_strength_slider):
    scene.skip_combobox_changes = True
    ui_name.clear()
    ui_name.addItems(colours)
    ui_name.setCurrentIndex(colours.index(item["name"]))
    ui_mix_with.clear()
    ui_mix_with.addItems(colours)
    ui_mix_with.setCurrentIndex(colours.index(item["mix_with"]))
    scene.skip_combobox_changes = False

    ui_mix_slider.setValue(item["mix_percent"])
    ui_mix_spin.setValue(item["mix_percent"])

    ui_strength_slider.setValue(item["strength"])
    ui_strength_spin.setValue(item["strength"])

def fill_fill_pattern(
        scene, item, ui_type,
        ui_distance_spin, ui_distance_slider,
        ui_size_spin, ui_size_slider,
        ui_rotation_spin, ui_rotation_slider,
        ui_xshift_spin, ui_xshift_slider,
        ui_yshift_spin, ui_yshift_slider):
    scene.skip_combobox_changes = True
    ui_type.setCurrentIndex(c.attribute_values(c.PatternType).index(item["type"]))
    scene.skip_combobox_changes = False

    ui_distance_slider.setValue(10.0*item["distance"])
    ui_distance_spin.setValue(item["distance"])

    ui_size_slider.setValue(20.0*item["size"])
    ui_size_spin.setValue(item["size"])

    ui_rotation_slider.setValue(1.0/1.8*item["rotation"])
    ui_rotation_spin.setValue(item["rotation"])

    ui_xshift_slider.setValue(20.0*item["xshift"])
    ui_xshift_spin.setValue(item["xshift"])

    ui_yshift_slider.setValue(20.0*item["yshift"])
    ui_yshift_spin.setValue(item["yshift"])

def fill_decoration(
        scene, item, ui_type,
        ui_amplitude_spin, ui_amplitude_slider,
        ui_wavelength_spin, ui_wavelength_slider,
        ui_text):
    scene.skip_combobox_changes = True
    ui_type.setCurrentIndex(c.attribute_values(c.DecorationType).index(item["type"]))
    scene.skip_combobox_changes = False

    ui_amplitude_slider.setValue(10.0*item["amplitude"])
    ui_amplitude_spin.setValue(item["amplitude"])

    ui_wavelength_slider.setValue(10.0*item["wavelength"])
    ui_wavelength_spin.setValue(item["wavelength"])

    ui_text.setText(item["text"])


def fill_dash(scene, item, ui_dash, ui_custom):
    scene.skip_combobox_changes = True
    ui_dash.setCurrentIndex(c.attribute_values(c.LineStroke).index(item["stroke"]))
    scene.skip_combobox_changes = False
    ui_custom.setText(' '.join(map(str, item["custom_pattern"])))


def fill_strategy(
        scene, item, ui_tabWidget, ui_connect_link,
        ui_rounded_corners_spin, ui_rounded_corners_slider,
        ui_out_angle_spin, ui_out_angle_slider,
        ui_in_angle_spin, ui_in_angle_slider,
        ui_bend_direction,
        ui_bend_angle_spin, ui_bend_angle_slider,
        ui_smooth_tension_spin, ui_smooth_tension_slider):
    index = c.attribute_values(c.StrategyType).index(item["line"]["strategy"]["type"])

    scene.skip_combobox_changes = True
    if index < 3:
        ui_tabWidget.setCurrentIndex(0)
        ui_connect_link.setCurrentIndex(index)
    elif index == 3:
        ui_tabWidget.setCurrentIndex(1)
    elif index in [4, 5]:
        ui_tabWidget.setCurrentIndex(2)
    else:
        ui_tabWidget.setCurrentIndex(3)
    ui_bend_direction.setCurrentIndex(item["line"]["strategy"]["type"] != c.StrategyType.BENDED_LEFT)
    scene.skip_combobox_changes = False

    ui_out_angle_slider.setValue(1.0/3.6*item["line"]["strategy"]["out_angle"])
    ui_out_angle_spin.setValue(item["line"]["strategy"]["out_angle"])

    ui_in_angle_slider.setValue(1.0/3.6*item["line"]["strategy"]["in_angle"])
    ui_in_angle_spin.setValue(item["line"]["strategy"]["in_angle"])

    ui_rounded_corners_slider.setValue(4.0*item["line"]["strategy"]["rounded_corners"])
    ui_rounded_corners_spin.setValue(item["line"]["strategy"]["rounded_corners"])

    ui_bend_angle_slider.setValue(1.0/3.6*item["line"]["strategy"]["bend_angle"])
    ui_bend_angle_spin.setValue(item["line"]["strategy"]["bend_angle"])

    ui_smooth_tension_slider.setValue(-10+50.0*item["line"]["strategy"]["smooth_tension"])
    ui_smooth_tension_spin.setValue(item["line"]["strategy"]["smooth_tension"])

