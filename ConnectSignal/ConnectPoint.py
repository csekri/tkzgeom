from ConnectSignal.Lambda import (
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract
)

def connect_point(main_window):

    main_window.plainTextEdit.textChanged.connect(
        lambda : connect_plain_text_edit_abstract(main_window, ['marker'], 'text', main_window.plainTextEdit))
    main_window.point_apply_text_change.clicked.connect(
        lambda : connect_text_edit_pushbutton_apply_abstract(main_window.scene))
