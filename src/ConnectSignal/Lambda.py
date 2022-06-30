import json
from copy import deepcopy

from Fill.ListWidget import fill_listWidget_with_data, set_selected_id_in_listWidget
from Fill.FillAll import fill_all_fields
from Colour import Colour
from Items import Items
from Item import Item
from Factory import Factory
import CanvasRendering as cr
import Constant as c
from DefinitionParser import parse_def


def tabWidget_func(value, main_window):
    """Connect main tabWidget."""
    main_window.scene.current_tab_idx = value
    fill_listWidget_with_data(main_window.scene.project_data, main_window.listWidget, value)
    set_selected_id_in_listWidget(main_window.scene, 0)


def listWidget_double_func(scene):
    """Connect listWidget double click."""
    scene.listWidget_edit_row = scene.ui.listWidget.currentItem().text()


def listWidget_text_changed_func(item, scene):
    """Connect listWidget item text changed."""
    scene.ui.listWidget.setFocus()
    if scene.skip_item_changes:
        return
    if not Item.name_pattern_static(item.text()) or item.text() in scene.project_data.items:
        scene.skip_item_changes = True
        item.setText(scene.listWidget_edit_row)
        scene.skip_item_changes = False
        return
    if scene.listWidget_edit_row:
        old_id = scene.listWidget_edit_row
        scene.listWidget_edit_row = None

        scene.project_data.change_id(old_id, item.text())

        # that is if the colour name is changed we replace all
        # occurances of the colour
        if c.TYPES[scene.current_tab_idx] == 'colour':
            print(type)
            state_dict = scene.project_data.state_dict()
            string = json.dumps(state_dict)
            string = string.replace(f': \"{old_id}\"', f': \"{item.text()}\"')
            data = json.loads(string)
            print(data)
            scene.project_data\
                = Items(data["window"], data["packages"], data["bg_colour"], data["code_before"], data["code_after"])
            for ditem in (data["items"]):
                scene.project_data.add(Factory.create_item(ditem))
            scene.list_focus_ids = [item.text()]
        fill_listWidget_with_data(scene.project_data,
                                  scene.ui.listWidget,
                                  scene.current_tab_idx)
        set_selected_id_in_listWidget(scene, scene.ui.listWidget.currentRow())
        scene.edit.add_undo_item(scene)
        cr.clear(scene)
        cr.add_all_items(scene)


def connect_name_change_abstract(ui_name, scene):
    """Connect listWidget item text changed."""
    scene.ui.listWidget.setFocus()
    old_id = scene.ui.listWidget.currentItem().text()
    if scene.skip_item_changes:
        return
    if not Item.name_pattern_static(ui_name.text()) or ui_name.text() in scene.project_data.items:
        scene.skip_item_changes = True
        ui_name.setText(old_id)
        scene.skip_item_changes = False
        return

    scene.project_data.change_id(old_id, ui_name.text())

    # that is if the colour name is changed we replace all
    # occurances of the colour
    if c.TYPES[scene.current_tab_idx] == 'colour':
        print(type)
        state_dict = scene.project_data.state_dict()
        string = json.dumps(state_dict)
        string = string.replace(f': \"{old_id}\"', f': \"{ui_name.text()}\"')
        data = json.loads(string)
        print(data)
        scene.project_data\
            = Items(data["window"], data["packages"], data["bg_colour"], data["code_before"], data["code_after"])
        for ditem in (data["items"]):
            scene.project_data.add(Factory.create_item(ditem))
        scene.list_focus_ids = [ui_name.text()]
    fill_listWidget_with_data(scene.project_data,
                              scene.ui.listWidget,
                              scene.current_tab_idx)
    set_selected_id_in_listWidget(scene, scene.ui.listWidget.currentRow())
    scene.edit.add_undo_item(scene)
    cr.clear(scene)
    cr.add_all_items(scene)


def listWidget_current_row_changed_func(main_window):
    """Connect listWidget current row changed."""
    main_window.scene.list_focus_ids = [item.text() for item in main_window.listWidget.selectedItems()]
    fill_all_fields(main_window.scene)


def connect_plain_text_edit_abstract(scene, properties_list, dict_key, plain_text_edit_widget):
    """Be an abstract plainTextEdit callback function."""
    ids = scene.list_focus_ids
    if scene.skip_plaintextedit_changes:
        return
    if not ids:
        return
    for id_ in ids:
        final_property = scene.project_data.items[id_].item
        for prop in properties_list:
            final_property = final_property[prop]
        final_property[dict_key] = plain_text_edit_widget.toPlainText()


def connect_text_edit_pushbutton_apply_abstract(scene):
    """Be an abstract pushButton callback function for applying text edit."""
    scene.edit.add_undo_item(scene)


def connect_combobox_abstract(value, scene, properties_list, dict_key, value_list, is_colour=False):
    """Be an abstract comboBox callback function."""
    if is_colour:
        value_list = value_list + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    if scene.skip_combobox_changes:
        return
    ids = scene.list_focus_ids
    if not ids:
        return
    for id_ in ids:
        final_property = scene.project_data.items[id_].item
        for prop in properties_list:
            final_property = final_property[prop]
        new_value = value_list[value]
        final_property[dict_key] = new_value
    scene.edit.add_undo_item(scene)


def connect_checkbox_abstract(state, scene, properties_list, dict_key):
    """Be an abstract checkBox callback function."""
    if scene.skip_checkbox_changes:
        return
    ids = scene.list_focus_ids
    if not ids:
        return
    for id_ in ids:
        final_property = scene.project_data.items[id_].item
        for prop in properties_list:
            final_property = final_property[prop]
        final_property[dict_key] = bool(state)
    scene.edit.add_undo_item(scene)


def connect_slider_moved_abstract(value, scene, properties_list, dict_key, linear_map, spinbox):
    """Be an abstract slider moved callback function."""
    ids = scene.list_focus_ids
    if not ids:
        return
    new_value = 0.0
    for id_ in ids:
        final_property = scene.project_data.items[id_].item
        for prop in properties_list:
            final_property = final_property[prop]
        new_value = linear_map(value)
        final_property[dict_key] = new_value
    spinbox.setValue(new_value)


def connect_slider_released_abstract(scene):
    """Be an abstract slider released callback function."""
    scene.edit.add_undo_item(scene)


def connect_dash_lineedit_abstract(scene, properties_list, dict_key, lineedit):
    """Be an abstract lineEdit callback function for dash pattern."""
    ids = scene.list_focus_ids
    if not lineedit.hasFocus():
        do_edit = True
        for id_ in ids:
            final_property = scene.project_data.items[id_].item
            for prop in properties_list:
                final_property = final_property[prop]
            try:
                lengths = list(map(int, lineedit.text().split(' ')))
                if len(lengths) % 2 != 0:
                    throw_error = 1 / 0
                final_property[dict_key] = lengths
                do_edit = True
            except ZeroDivisionError:
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
    """Be an abstract lineEdit callback function."""
    ids = scene.list_focus_ids
    if not lineedit.hasFocus():
        for id_ in ids:
            final_property = scene.project_data.items[id_].item
            for prop in properties_list:
                final_property = final_property[prop]
            final_property[dict_key] = lineedit.text()
        scene.edit.add_undo_item(scene)
    else:
        scene.ui.listWidget.setFocus(True)


def connect_def_str_lineedit_abstract(scene, lineedit):
    """Be an abstract lineEdit callback function for definition."""
    # TODO extra code needed to prevent cross dependency of two objects
    # e.g. A -> B and B -> A should not happen simultaneously
    ids = scene.list_focus_ids
    if not ids:
        return None
    id_ = ids[0]
    if not lineedit.hasFocus():
        try:
            parse_step1 = parse_def(lineedit.text(), c.PARSE_TO_TYPE_MAP)
            if not parse_step1:
                print(1 / 0)
            type, sub_type = c.PARSE_TO_TYPE_MAP[parse_step1[0]]
            if type != scene.project_data.items[id_].item["type"]:
                print(1 / 0)
            item = Factory.create_empty_item(type, sub_type)
            item.item["id"] = id_
            parse_step2 = item.parse_into_definition(parse_step1[1], scene.project_data.items)
            if not parse_step2:
                print(1 / 0)
            item_dict = deepcopy(scene.project_data.items[id_].item)
            item_dict["definition"] = parse_step2
            item_dict["type"] = type
            item_dict["sub_type"] = sub_type

            scene.project_data.items[id_] = Factory.create_item(item_dict)
            lineedit.setText(lineedit.text().replace(' ', ''))
            do_edit = True
        except ZeroDivisionError:
            lineedit.setText(scene.project_data.items[id_].definition_string())
            do_edit = False
        if do_edit:
            scene.project_data.recompute_canvas(*scene.init_canvas_dims)
            scene.edit.add_undo_item(scene)
    else:
        scene.ui.listWidget.setFocus(True)


def connect_spinbox_value_changed_abstract(value, scene, properties_list, dict_key, spinbox):
    """Be an abstract spinbox value changed callback function."""
    ids = scene.list_focus_ids
    if not ids:
        return
    new_value = 0.0
    for id_ in ids:
        final_property = scene.project_data.items[id_].item
        for prop in properties_list:
            final_property = final_property[prop]
        new_value = value
        final_property[dict_key] = new_value


def connect_spinbox_editing_finished_abstract(scene):
    """Be an abstract spinbox editing finished callback function."""
    scene.edit.add_undo_item(scene)
    scene.ui.listWidget.setFocus(True)