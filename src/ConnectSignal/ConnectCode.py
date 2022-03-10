from PyQt5 import QtCore, QtWidgets

from Fill.FillAll import fill_all_fields
from Fill.ListWidget import fill_listWidget_with_data, listWidget_set_current_row
from ConnectSignal.Lambda import (
    connect_lineedit_abstract,
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract
)
from Colour import Colour
from Factory import Factory


def package_list_updated(scene):
    for i in range(scene.ui.packages_listWidget.count()):
        scene.project_data.packages[i] = scene.ui.packages_listWidget.item(i).text()


def add_new_package(scene):
    selector = scene.ui.packages_listWidget # alias for the listWidget
    if selector.item(selector.count() - 1).text() != '':
        item = QtWidgets.QListWidgetItem('')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        selector.addItem(item)
        selector.editItem(item)
        selector.verticalScrollBar().setValue(selector.verticalScrollBar().maximum())
        if selector.count() > len(scene.project_data.packages):
            scene.project_data.packages.append('')


def delete_package(scene):
    current_row = scene.ui.packages_listWidget.currentRow()
    if current_row > 6:
        scene.ui.packages_listWidget.takeItem(current_row)
        del scene.project_data.packages[current_row]


def connect_code_plain_text_edit(scene, plain_text_edit_widget, is_before):
    if is_before:
        scene.project_data.code_before = plain_text_edit_widget.toPlainText()
    else:
        scene.project_data.code_after = plain_text_edit_widget.toPlainText()


def connect_code_text_edit_pushbutton_apply(scene):
    scene.edit.add_undo_item(scene)


def connect_code(scene):
    scene.ui.packages_listWidget.itemChanged.connect(lambda : package_list_updated(scene))
    scene.ui.packages_add_new.clicked.connect(lambda : add_new_package(scene))
    scene.ui.packages_delete.clicked.connect(lambda : delete_package(scene))

    scene.ui.code_before_text.textChanged.connect(
        lambda : connect_code_plain_text_edit(scene, scene.ui.code_before_text, True))
    scene.ui.code_before_apply.clicked.connect(
        lambda : connect_code_text_edit_pushbutton_apply(scene))

    scene.ui.code_after_text.textChanged.connect(
        lambda : connect_code_plain_text_edit(scene, scene.ui.code_after_text, False))
    scene.ui.code_after_apply.clicked.connect(
        lambda : connect_code_text_edit_pushbutton_apply(scene))
