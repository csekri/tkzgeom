import Constant as c
from ConnectSignal.Lambda import (
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract,
    connect_combobox_colour_abstract
)

def connect_point(main_window):
    colours = c.attribute_values(c.Colour)\
        + [i["id"] for i in main_window.scene.project_data.colours]
    main_window.plainTextEdit.textChanged.connect(
        lambda : connect_plain_text_edit_abstract(main_window, ['marker'], 'text', main_window.plainTextEdit))
    main_window.point_apply_text_change.clicked.connect(
        lambda : connect_text_edit_pushbutton_apply_abstract(main_window.scene))

    main_window.point_marker_colour_name.currentIndexChanged.connect(
        lambda x: connect_combobox_colour_abstract(x, main_window, ['fill', 'colour'], 'name', colours))
    main_window.point_marker_colour_mix_name.currentIndexChanged.connect(
        lambda x: connect_combobox_colour_abstract(x, main_window, ['fill', 'colour'], 'mix_with', colours))
