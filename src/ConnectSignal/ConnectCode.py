from PyQt5 import QtCore, QtWidgets


def __package_list_updated(scene):
    """Rename package."""
    for i in range(scene.ui.packages_listWidget.count()):
        scene.project_data.packages[i] = scene.ui.packages_listWidget.item(i).text()


def __add_new_package(scene):
    """Add new package."""
    selector = scene.ui.packages_listWidget  # alias for the listWidget
    if selector.item(selector.count() - 1).text() != '':
        item = QtWidgets.QListWidgetItem('% \\usepackage{new-package}')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        selector.addItem(item)
        selector.editItem(item)
        selector.verticalScrollBar().setValue(selector.verticalScrollBar().maximum())
        if selector.count() > len(scene.project_data.packages):
            scene.project_data.packages.append('')


def __delete_package(scene):
    """Delete package."""
    current_row = scene.ui.packages_listWidget.currentRow()
    if current_row > 6:
        scene.ui.packages_listWidget.takeItem(current_row)
        del scene.project_data.packages[current_row]


def __connect_code_plain_text_edit(scene, plain_text_edit_widget, is_before):
    """Connect code before/after plainTextEdit."""
    if is_before:
        scene.project_data.code_before = plain_text_edit_widget.toPlainText()
    else:
        scene.project_data.code_after = plain_text_edit_widget.toPlainText()


def __connect_code_text_edit_pushbutton_apply(scene):
    """Connect apply changes pushbutton."""
    scene.edit.add_undo_item(scene)


def connect_code(scene):
    """Connect signals in the code tab."""
    scene.ui.packages_listWidget.itemChanged.connect(lambda: __package_list_updated(scene))
    scene.ui.packages_add_new.clicked.connect(lambda: __add_new_package(scene))
    scene.ui.packages_delete.clicked.connect(lambda: __delete_package(scene))

    scene.ui.code_before_text.textChanged.connect(
        lambda: __connect_code_plain_text_edit(scene, scene.ui.code_before_text, True))
    scene.ui.code_before_apply.clicked.connect(
        lambda: __connect_code_text_edit_pushbutton_apply(scene))

    scene.ui.code_after_text.textChanged.connect(
        lambda: __connect_code_plain_text_edit(scene, scene.ui.code_after_text, False))
    scene.ui.code_after_apply.clicked.connect(
        lambda: __connect_code_text_edit_pushbutton_apply(scene))
