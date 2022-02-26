from Fill.FillAll import fill_all_fields
from Fill.ListWidget import fill_listWidget_with_data, listWidget_set_current_row
from Colour import Colour
from Factory import Factory

def connect_add_colour_pushbutton(scene):
    item = Colour({ 'id': '', 'type': 'colour', 'definition': '#000000'})
    item.item["id"] = Factory.next_id(item, None, scene.project_data.items)
    scene.project_data.add(item) #.append({ 'id': new_id, 'definition': '#ffffff'})
    fill_listWidget_with_data(scene.project_data, scene.ui.listWidget, scene.current_tab_idx)
    fill_all_fields(scene)
    listWidget_set_current_row(scene.ui.listWidget, item.get_id())
    scene.edit.add_undo_item(scene)


def connect_colour(scene):
    scene.ui.colour_add_new_pushbutton.pressed.connect(
        lambda : connect_add_colour_pushbutton(scene))
