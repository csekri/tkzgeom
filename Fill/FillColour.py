import Constant as c

def fill_colour_fields(main_window):
    ids = main_window.scene.list_focus_ids
    if not ids:
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
