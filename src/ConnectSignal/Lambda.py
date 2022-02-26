from Fill.ListWidget import fill_listWidget_with_data
from Fill.FillAll import fill_all_fields
from Colour import Colour
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
        if old_id in main_window.scene.project_data.items:
            main_window.scene.project_data.items[old_id].item["id"] = item.text()
            main_window.scene.project_data.items[item.text()] = main_window.scene.project_data.items.pop(old_id)
        else:
            pass
        main_window.listWidget_edit_row = None
        cr.clear(main_window.scene)
        cr.add_all_items(main_window.scene)

def listWidget_current_row_changed_func(main_window):
    # TODO fill widget fields with relevant data
    main_window.scene.list_focus_ids = [item.text() for item in main_window.listWidget.selectedItems()]
    print(main_window.scene.list_focus_ids)
    fill_all_fields(main_window.scene)

def connect_plain_text_edit_abstract(scene, properties_list, dict_key, plain_text_edit_widget):
    ids = scene.list_focus_ids
    if scene.skip_plaintextedit_changes:
        return
    if not ids:
        return
    for id in ids:
        final_property = scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        final_property[dict_key] = plain_text_edit_widget.toPlainText()

def connect_text_edit_pushbutton_apply_abstract(scene):
    scene.edit.add_undo_item(scene)

def connect_combobox_abstract(value, scene, properties_list, dict_key, value_list, is_colour=False):
    if is_colour:
        value_list = value_list + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    if scene.skip_combobox_changes:
        return
    ids = scene.list_focus_ids
    if not ids:
        return
    for id in ids:
        final_property = scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        new_value = value_list[value]
        final_property[dict_key] = new_value
    scene.edit.add_undo_item(scene)

def connect_checkbox_abstract(state, scene, properties_list, dict_key):
    if scene.skip_checkox_changes:
        return
    ids = scene.list_focus_ids
    if not ids:
        return
    for id in ids:
        final_property = scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        final_property[dict_key] = bool(state)
    scene.edit.add_undo_item(scene)

def connect_slider_moved_abstract(value, scene, properties_list, dict_key, linear_map, spinbox):
    ids = scene.list_focus_ids
    if not ids:
        return
    for id in ids:
        final_property = scene.project_data.items[id].item
        for prop in properties_list:
            final_property = final_property[prop]
        new_value = linear_map(value)
        final_property[dict_key] = new_value
    spinbox.setValue(new_value)

def connect_slider_released_abstract(scene):
    scene.edit.add_undo_item(scene)

def connect_dash_lineedit_abstract(scene, properties_list, dict_key, lineedit):
    ids = scene.list_focus_ids
    if not lineedit.hasFocus():
        do_edit = True
        for id in ids:
            final_property = scene.project_data.items[id].item
            for prop in properties_list:
                final_property = final_property[prop]
            try:
                lengths = list(map(int, lineedit.text().split(' ')))
                if len(lengths) % 2 != 0:
                    throw_error = 1/0
                final_property[dict_key] = lengths
                do_edit = True
            except:
                lengths_str = ''
                for num in final_property[dict_key]:
                    lengths_str += "%s " % str(num)
                lengths_str = lengths_str[:-1]
                lineedit.setText(lengths_str)
                do_edit = False
        if do_edit:
            scene.edit.add_undo_item(scene)
    else:
        scene.ui.listWidget.setFocus(True)

def connect_lineedit_abstract(scene, properties_list, dict_key, lineedit):
    ids = scene.list_focus_ids
    if not lineedit.hasFocus():
        for id in ids:
            final_property = scene.project_data.items[id].item
            for prop in properties_list:
                final_property = final_property[prop]
            final_property[dict_key] = lineedit.text()
        scene.edit.add_undo_item(scene)
    else:
        scene.ui.listWidget.setFocus(True)






#
