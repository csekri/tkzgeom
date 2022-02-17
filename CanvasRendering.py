"""
This file contains the functions that handle the Qt items
drawn on the screens. All of these functions are defined on
the graphicsScene class.

"""

from PyQt5 import QtGui

from HighlightItem import item_in_focus
import Constant as c

class ColorMapping:
    FREE_POINT = QtGui.QColor(213, 4, 2, 150)
    FREE_POINT_FOCUS = FREE_POINT.darker(130)
    FREE_POINT_FOCUS.setAlpha(130)

    OTHER_ITEM = QtGui.QColor(4, 127, 204, 150)
    OTHER_ITEM_FOCUS = OTHER_ITEM.darker(130)
    OTHER_ITEM_FOCUS.setAlpha(150)

    SELECT_ITEM = QtGui.QColor(252, 186, 3, 150)
    SELECT_ITEM_FOCUS = OTHER_ITEM.darker(130)
    SELECT_ITEM_FOCUS.setAlpha(150)

def clear(scene):
    scene.clear()

def add_all_items(scene):
    for item in scene.project_data.items.values():
        if item.item["type"] != 'point':
            item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM)

    for item in scene.project_data.items.values():
        if item.item["type"] == 'point':
            if item.item["sub_type"] == c.Point.Definition.FREE:
                item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.FREE_POINT)
            else:
                item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM)

    focus = item_in_focus(scene.project_data, scene.mouse)
    if focus:
        if scene.project_data.items[focus].item["type"] == "point" and\
        scene.project_data.items[focus].item["sub_type"] == c.Point.Definition.FREE:
            scene.project_data.items[focus].draw_on_canvas(scene.project_data.items, scene, ColorMapping.FREE_POINT_FOCUS)
        else:
            scene.project_data.items[focus].draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM_FOCUS)

    for item_id in scene.select_history.id_history:
        scene.project_data.items[item_id].draw_on_canvas(scene.project_data.items, scene, ColorMapping.SELECT_ITEM)
