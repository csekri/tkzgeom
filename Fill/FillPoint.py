import Constant as c

def fill_point_fields(main_window):
    ids = main_window.scene.list_focus_ids
    colours = c.attribute_values(c.Colour)\
        + [i["id"] for i in main_window.scene.project_data.colours]
    if not ids:
        return
    if c.TYPES[main_window.scene.current_tab_idx] != 'point':
        return
    point = main_window.scene.project_data.items[ids[0]].item
    main_window.skip_plaintextedit_changes = True
    main_window.plainTextEdit.setPlainText(point["marker"]["text"])
    main_window.skip_plaintextedit_changes = False
    main_window.skip_combobox_changes = True
    main_window.point_marker_colour_name.clear()
    main_window.point_marker_colour_name.addItems(colours)
    main_window.point_marker_colour_name.setCurrentIndex(colours.index(point["fill"]["colour"]["name"]))
    main_window.point_marker_colour_mix_name.clear()
    main_window.point_marker_colour_mix_name.addItems(colours)
    main_window.point_marker_colour_mix_name.setCurrentIndex(colours.index(point["fill"]["colour"]["mix_with"]))
    main_window.point_marker_shape.setCurrentIndex(c.attribute_values(c.Marker_Shape).index(point["marker"]["shape"]))
    main_window.skip_combobox_changes = False
    main_window.point_show_label.setEnabled(point["label"]["show"])
