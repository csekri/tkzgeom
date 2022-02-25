import Constant as c

def fill_point_fields(scene):
    ids = scene.list_focus_ids
    colours = c.attribute_values(c.Colour)\
        + [i["id"] for i in scene.project_data.colours]
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'point':
        return
    point = scene.project_data.items[ids[0]].item
    scene.skip_plaintextedit_changes = True
    scene.ui.plainTextEdit.setPlainText(point["marker"]["text"])
    scene.skip_plaintextedit_changes = False
    scene.skip_combobox_changes = True
    scene.ui.point_marker_colour_name.clear()
    scene.ui.point_marker_colour_name.addItems(colours)
    scene.ui.point_marker_colour_name.setCurrentIndex(colours.index(point["fill"]["colour"]["name"]))
    scene.ui.point_marker_colour_mix_name.clear()
    scene.ui.point_marker_colour_mix_name.addItems(colours)
    scene.ui.point_marker_colour_mix_name.setCurrentIndex(colours.index(point["fill"]["colour"]["mix_with"]))
    scene.ui.point_marker_shape.setCurrentIndex(c.attribute_values(c.Marker_Shape).index(point["marker"]["shape"]))
    scene.skip_combobox_changes = False
    scene.ui.point_show_label.setChecked(point["label"]["show"])

    scene.ui.point_size_slider.setValue(point["marker"]["size"])
    scene.ui.point_size_spin.setValue(point["marker"]["size"])

    scene.ui.point_shape_number_slider.setValue(point["marker"]["shape_number"])
    scene.ui.point_shape_number_spin.setValue(point["marker"]["shape_number"])

    scene.ui.point_inner_sep_slider.setValue(point["marker"]["inner_sep"])
    scene.ui.point_inner_sep_spin.setValue(point["marker"]["inner_sep"])

    scene.ui.point_ratio_slider.setValue(-10+20*point["marker"]["ratio"])
    scene.ui.point_ratio_spin.setValue(point["marker"]["ratio"])

    scene.ui.point_marker_colour_mixratio_slider.setValue(point["fill"]["colour"]["mix_percent"])
    scene.ui.point_marker_colour_mixratio_spin.setValue(point["fill"]["colour"]["mix_percent"])

    scene.ui.point_marker_colour_strength_slider.setValue(point["fill"]["colour"]["strength"])
    scene.ui.point_marker_colour_strength_spin.setValue(point["fill"]["colour"]["strength"])
