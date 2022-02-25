from Fill.ListWidget import fill_listWidget_with_data
from Fill.FillPoint import fill_point_fields
from Fill.FillColour import fill_colour_fields

import CanvasRendering as cr

def tabWidget_func(value, main_window):
    main_window.scene.current_tab_idx = value
    fill_listWidget_with_data(main_window.scene.project_data, main_window.listWidget, value)

def listWidget_double_func(item, main_window):
    main_window.listWidget_edit_row = main_window.listWidget.currentItem().text()

def listWidget_text_changed_func(item, main_window):
    # TODO check validity of new id
    if main_window.listWidget_edit_row:
        old_id = main_window.listWidget_edit_row
        # main_window.listWidget.currentItem().setText(main_window.listWidget_edit_row)
        # old_id = main_window.listWidget.currentItem().text()
        main_window.scene.project_data.items[old_id].item["id"] = item.text()
        main_window.scene.project_data.items[item.text()] = main_window.scene.project_data.items.pop(old_id)
        main_window.listWidget_edit_row = None
        cr.clear(main_window.scene)
        cr.add_all_items(main_window.scene)

def listWidget_current_row_changed_func(main_window):
    # TODO fill widget fields with relevant data
    main_window.scene.list_focus_ids = [item.text() for item in main_window.listWidget.selectedItems()]
    print(main_window.scene.list_focus_ids)
    fill_point_fields(main_window)
    fill_colour_fields(main_window)

def connect_plain_text_edit_abstract(main_window, properties_list, dict_key, plain_text_edit_widget):
    ids = main_window.scene.list_focus_ids
    if main_window.skip_plaintextedit_changes:
        return
    for id in ids:
        final_property = main_window.scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        final_property[dict_key] = plain_text_edit_widget.toPlainText()

def connect_text_edit_pushbutton_apply_abstract(scene):
    scene.edit.add_undo_item(scene)

def connect_combobox_abstract(value, main_window, properties_list, dict_key, value_list):
    if main_window.skip_combobox_changes:
        return
    ids = main_window.scene.list_focus_ids
    for id in ids:
        final_property = main_window.scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        new_value = value_list[value]
        final_property[dict_key] = new_value
        print(main_window.scene.project_data.items[id].item)
    main_window.scene.edit.add_undo_item(main_window.scene)

def connect_checkbox_abstract(state, main_window, properties_list, dict_key):
    ids = main_window.scene.list_focus_ids
    for id in ids:
        final_property = main_window.scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        final_property[dict_key] = bool(state)
    main_window.scene.edit.add_undo_item(main_window.scene)
