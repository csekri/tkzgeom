from Constant import TYPES
from PyQt5 import QtCore, QtWidgets


def fill_listWidget_with_data(project_data, listWidget, tab_index):
    """Remove and add all items to listWidget"""
    listWidget.clear()
    for item in project_data.items.values():
        if item.item["type"] == TYPES[tab_index]:
            item = QtWidgets.QListWidgetItem(item.get_id())
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            listWidget.addItem(item)


# TODO explore if needed
def listWidget_set_current_row(listWidget, id):
    """Find id in listWidget and set current row to that."""
    items = listWidget.findItems(id, QtCore.Qt.MatchExactly)
    listWidget.setCurrentRow(listWidget.row(items[0]))


def set_selected_id_in_listWidget(scene, index):
    """Set index in listWidget selected."""
    length = scene.ui.listWidget.count()
    if length == 0:
        scene.list_focus_ids = []
        scene.ui.listWidget.setCurrentRow(-1)
    elif 0 <= index < length:
        scene.list_focus_ids = [index]
        scene.ui.listWidget.setCurrentRow(index)
        scene.ui.listWidget.item(index).setSelected(True)
    else:
        scene.list_focus_ids = [length - 1]
        scene.ui.listWidget.setCurrentRow(length - 1)
        scene.ui.listWidget.item(length-1).setSelected(True)
