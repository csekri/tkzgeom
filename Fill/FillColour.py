import Constant as c

def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)

def fill_colour_fields(main_window):
    ids = main_window.scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[main_window.scene.current_tab_idx] != 'colour':
        return

    hex = ''
    for colour in main_window.scene.project_data.colours:
        if colour["id"] == ids[0]:
            hex = colour["definition"]
    main_window.colour_visualise_pushbutton.setStyleSheet(
        '''QTextBrowser {
            background-color: %s;
        }''' % hex
    )
    main_window.colour_hex_label.setText(hex)
    r, g, b = hex_to_rgb(hex)
    main_window.colour_red_label.setText(str(r))
    main_window.colour_green_label.setText(str(g))
    main_window.colour_blue_label.setText(str(b))
