import json

from Fill.ListWidget import fill_listWidget_with_data, set_selected_id_in_listWidget
from Fill.FillAll import fill_all_fields
from Colour import Colour
from Items import Items
from Factory import Factory
import CanvasRendering as cr
import Constant as c
from DefinitionParser import parse_def
from copy import deepcopy


def tabWidget_func(value, main_window):
    main_window.scene.current_tab_idx = value
    fill_listWidget_with_data(main_window.scene.project_data, main_window.listWidget, value)
    set_selected_id_in_listWidget(main_window.scene, 0)


def listWidget_double_func(item, main_window):
    main_window.listWidget_edit_row = main_window.listWidget.currentItem().text()


def listWidget_text_changed_func(item, main_window):
    # TODO check validity of new id
    if main_window.listWidget_edit_row:
        old_id = main_window.listWidget_edit_row
        # type = main_window.scene.project_data.items[old_id].item["type"]
        # if old_id in main_window.scene.project_data.items:
        #     main_window.scene.project_data.items[old_id].item["id"] = item.text()
        #     main_window.scene.project_data.items[item.text()] = main_window.scene.project_data.items.pop(old_id)
        main_window.listWidget_edit_row = None

        main_window.scene.project_data.change_id(old_id, item.text())

        # that is if the colour name is changed we replace all
        # occurances of the colour
        if type == 'colour':
            state_dict = main_window.scene.project_data.state_dict()
            string = json.dumps(state_dict)
            string = string.replace(f': \"{old_id}\"', f': \"{item.text()}\"')
            data = json.loads(string)
            print(data)
            main_window.scene.project_data\
                = Items(data["window"], data["packages"], data["bg_colour"], data["code_before"], data["code_after"])
            for ditem in (data["items"]):
                main_window.scene.project_data.add(Factory.create_item(ditem))
            main_window.scene.list_focus_ids = [item.text()]
        fill_listWidget_with_data(main_window.scene.project_data, main_window.scene.ui.listWidget, main_window.scene.current_tab_idx)
        set_selected_id_in_listWidget(main_window.scene, main_window.ui.scene.ui.listWidget.currentRow())
        main_window.scene.edit.add_undo_item(main_window.scene)
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


def connect_def_str_lineedit_abstract(scene, lineedit):
    # TODO extra code needed to prevent cross dependency of two objects
    # e.g. A -> B and B -> A should not happen simultaneously
    ids = scene.list_focus_ids
    if not ids:
        return None
    id = ids[0]
    if not lineedit.hasFocus():
        do_edit = True
        try:
            parse_step1 = parse_def(lineedit.text(), c.PARSE_TO_TYPE_MAP)
            if not parse_step1:
                throw_error = 1/0
            type, sub_type = c.PARSE_TO_TYPE_MAP[parse_step1[0]]
            item = Factory.create_empty_item(type, sub_type)
            item.item["id"] = id
            parse_step2 = item.parse_into_definition(parse_step1[1], scene.project_data.items)
            if not parse_step2:
                throw_error = 1/0
            item_dict = deepcopy(scene.project_data.items[id].item)
            item_dict["definition"] = parse_step2
            item_dict["type"] = type
            item_dict["sub_type"] = sub_type
            scene.project_data.items[id] = Factory.create_item(item_dict)
            lineedit.setText(lineedit.text().replace(' ', ''))
            do_edit = True
        except ZeroDivisionError:
            lineedit.setText(scene.project_data.items[id].definition_string())
            do_edit = False
        if do_edit:
            scene.project_data.recompute_canvas(*scene.init_canvas_dims)
            scene.edit.add_undo_item(scene)
    else:
        scene.ui.listWidget.setFocus(True)





#
