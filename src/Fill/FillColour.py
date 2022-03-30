import Constant as c


def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def fill_colour_fields(scene):
    """Fill all widgets in the colour tab."""
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'colour':
        return

    scene.ui.colour_name.setText(scene.project_data.items[ids[0]].get_id())
    hex = scene.project_data.items[ids[0]].item["definition"]
    scene.ui.colour_visualise_pushbutton.setStyleSheet(
        '''QTextBrowser {
            background-color: %s;
        }''' % hex
    )
    scene.ui.colour_hex_lineedit.setText(hex)
    r, g, b = hex_to_rgb(hex)
    scene.ui.colour_red_label.setText(str(r))
    scene.ui.colour_green_label.setText(str(g))
    scene.ui.colour_blue_label.setText(str(b))
