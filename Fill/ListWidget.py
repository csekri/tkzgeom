from Constant import TYPES
from PyQt5 import QtCore, QtWidgets

def fill_listWidget_with_data(project_data, listWidget, tab_index):
    listWidget.clear()
    for item in project_data.items.values():
        if item.item["type"] == TYPES[tab_index]:
            item = QtWidgets.QListWidgetItem(item.get_id())
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            listWidget.addItem(item)
    if TYPES[tab_index] == 'colour':
        for colour in project_data.colours:
                item = QtWidgets.QListWidgetItem(colour["id"])
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                listWidget.addItem(item)

def listWidget_set_current_row(listWidget, id):
    items = listWidget.findItems(id, QtCore.Qt.MatchExactly)
    listWidget.setCurrentRow(listWidget.row(items[0]))
