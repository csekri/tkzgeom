import Constant as c

def fill_o_arrow(scene, item, ui_tip, ui_side, ui_reversed,
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

    scene.skip_checkox_changes = True
    scene.ui.segment_o_reversed.setChecked(item["o_arrow"]["reversed"])
    scene.skip_checkox_changes = False

def fill_d_arrow(scene, item, ui_tip, ui_side, ui_reversed,
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

    scene.skip_checkox_changes = True
    scene.ui.segment_o_reversed.setChecked(item["d_arrow"]["reversed"])
    scene.skip_checkox_changes = False

def fill_colour(scene, item, colours, ui_name, ui_mix_with,
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

def fill_fill_pattern(scene, item, ui_type,
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
