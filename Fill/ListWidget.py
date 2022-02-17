def fill_listWidget_with_data(project_data, listWidget, tab_index):
    types = ['point', 'segment', 'circle', 'polygon', 'linestring', 'function', 'colour', 'number']
    listWidget.clear()
    for item in project_data.items.values():
        if item.item["type"] == types[tab_index]:
            listWidget.addItem(item.get_id())
