from Fill.FillAll import fill_all_fields
from Fill.ListWidget import fill_listWidget_with_data, listWidget_set_current_row
from ConnectSignal.Lambda import connect_lineedit_abstract
from Colour import Colour
from Factory import Factory


def connect_add_colour_pushbutton(scene):
    """Connect add colour pushButton."""
    item = Colour({ 'id': '', 'type': 'colour', 'definition': '#000000'})
    item.item["id"] = Factory.next_id(item, None, scene.project_data.items)
    scene.project_data.add(item)
    fill_listWidget_with_data(scene.project_data, scene.ui.listWidget, scene.current_tab_idx)
    fill_all_fields(scene)
    listWidget_set_current_row(scene.ui.listWidget, item.get_id())  # TODO explore if needed (from listWidget)
    scene.edit.add_undo_item(scene)


def connect_colour(scene):
    """Connect signals in the colour tab."""
    scene.ui.colour_add_new_pushbutton.pressed.connect(
        lambda : connect_add_colour_pushbutton(scene))
    scene.ui.colour_hex_lineedit.editingFinished.connect(
        lambda : connect_lineedit_abstract(scene, [], 'definition', scene.ui.colour_hex_lineedit))
