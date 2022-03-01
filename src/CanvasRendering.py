"""
This file contains the functions that handle the Qt items
drawn on the screens. All of these functions are defined on
the graphicsScene class.

"""

from PyQt5 import QtGui, QtWidgets
import numpy as np

from HighlightItem import item_in_focus
import Constant as c
from Segment import Segment
from Polygon import Polygon
from KeyBank import KeyState

class ColorMapping:
    FREE_POINT = QtGui.QColor(213, 4, 2, 150)
    FREE_POINT_FOCUS = FREE_POINT.darker(130)
    FREE_POINT_FOCUS.setAlpha(130)

    OTHER_ITEM = QtGui.QColor(4, 127, 204, 150)
    OTHER_ITEM_FILL = OTHER_ITEM.lighter(150)
    OTHER_ITEM_FILL.setAlpha(60)
    OTHER_ITEM_FOCUS = OTHER_ITEM.darker(130)
    OTHER_ITEM_FOCUS.setAlpha(150)
    OTHER_ITEM_FOCUS_FILL = OTHER_ITEM_FOCUS.lighter(150)
    OTHER_ITEM_FOCUS_FILL.setAlpha(60)

    SELECT_ITEM = QtGui.QColor(252, 186, 3, 150)
    SELECT_ITEM_FILL = SELECT_ITEM.lighter(150)
    SELECT_ITEM_FILL.setAlpha(150)
    SELECT_ITEM_FOCUS = OTHER_ITEM.darker(130)
    SELECT_ITEM_FOCUS.setAlpha(150)
    SELECT_ITEM_FOCUS_FILL = SELECT_ITEM_FOCUS.lighter(150)
    SELECT_ITEM_FOCUS_FILL.setAlpha(60)

def clear(scene):
    scene.clear()

def add_all_items(scene):
    def add_pdf(scene):
        pixmap = QtGui.QPixmap("try-1.png")
        if not scene.show_pdf:
            pixmap.fill()
        tkz_img = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(tkz_img)

    def add_polygons(scene):
        for item in scene.project_data.items.values():
            if item.item["type"] == 'polygon':
                item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM_FILL)

    def add_segments(scene):
        for item in scene.project_data.items.values():
            if item.item["type"] in ['segment']:
                item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM)

    def add_half_ready_segment(scene):
        if scene.select_mode.get_type() == c.Tool.SEGMENT_THROUGH\
        and len(scene.select_history.type_history) == 1:
            Segment.draw_on_canvas_static(
                *scene.project_data.items[scene.select_history.id_history[0]].get_canvas_coordinates(),
                *scene.mouse.get_xy(),
                scene,
                ColorMapping.OTHER_ITEM)

    def add_half_ready_polygon(scene):
        if scene.select_mode.get_type() == c.Tool.POLYGON\
        and scene.select_history.type_history:
            Polygon.draw_on_canvas_static(
                *scene.mouse.get_xy(),
                scene.select_history.id_history,
                scene,
                ColorMapping.OTHER_ITEM_FILL)

    def add_points(scene):
        for item in scene.project_data.items.values():
            if item.item["type"] == 'point':
                if item.item["sub_type"] in [c.Point.Definition.FREE, c.Point.Definition.ON_LINE]:
                    item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.FREE_POINT)
                else:
                    item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM)

    def add_item_in_focus(scene):
        focus = item_in_focus(scene.project_data, scene.mouse)
        if focus:
            if scene.project_data.items[focus].item["type"] == 'point' and\
            scene.project_data.items[focus].item["sub_type"] in [c.Point.Definition.FREE, c.Point.Definition.ON_LINE]:
                scene.project_data.items[focus].draw_on_canvas(scene.project_data.items, scene, ColorMapping.FREE_POINT_FOCUS)
            elif scene.project_data.items[focus].item["type"] == 'polygon':
                scene.project_data.items[focus].draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM_FOCUS_FILL)
            else:
                scene.project_data.items[focus].draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM_FOCUS)
        for item_id in scene.select_history.id_history:
            scene.project_data.items[item_id].draw_on_canvas(scene.project_data.items, scene, ColorMapping.SELECT_ITEM)

    if scene.show_pdf:
        add_pdf(scene)
    if scene.show_canvas_items or scene.key_bank.move_point.state == KeyState.DOWN or scene.key_bank.move_canvas.state == KeyState.DOWN:
        add_polygons(scene)
        add_segments(scene)
    add_half_ready_segment(scene)
    add_half_ready_polygon(scene)
    if scene.show_canvas_items or scene.key_bank.move_point.state == KeyState.DOWN or scene.key_bank.move_canvas.state == KeyState.DOWN:
        add_points(scene)
    add_item_in_focus(scene)
