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
from Circle import Circle
from Polygon import Polygon
from Linestring import Linestring
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
    def draw_aspect_ratio(scene):
        """
        SUMMARY
            draws two lines onto the canvas where the given aspect ratio crops the canvas
        PARAMETERS
            scene: GraphicsScene
            colour: colour of the two lines
        RETURNS
            None
        """
        colour = QtGui.QColor(0, 0, 0, 150)
        aspect_ratio = 16/9 # eval(scene.aspect_ratio)
        width, height = scene.width(), scene.height()
        # window_aspect = width / height
        # aspect_ratio < 1 means we draw vertical lines
        if aspect_ratio < width / height:
            x_from, y_from, x_to, y_to = (
            (width - height * aspect_ratio) / 2, 0, (width - height * aspect_ratio) / 2, height)
            graphics_line_1 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
            x_from, y_from, x_to, y_to = (
            width - (width - height * aspect_ratio) / 2, 0, width - (width - height * aspect_ratio) / 2, height)
            graphics_line_2 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
        # aspect_ratio > 1 means we draw horizontal lines
        else:
            x_from, y_from, x_to, y_to = (
            0, (height - width / aspect_ratio) / 2, width, (height - width / aspect_ratio) / 2)
            graphics_line_1 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
            x_from, y_from, x_to, y_to = (
            0, height - (height - width / aspect_ratio) / 2, width, height - (height - width / aspect_ratio) / 2)
            graphics_line_2 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
        # if aspect ratio is 1 we don't draw at all
        if aspect_ratio != width / height:
            graphics_line_1.setPen(QtGui.QPen(QtGui.QBrush(colour), 2))
            graphics_line_2.setPen(QtGui.QPen(QtGui.QBrush(colour), 2))
            scene.addItem(graphics_line_1)
            scene.addItem(graphics_line_2)

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

    def add_circles(scene):
        for item in scene.project_data.items.values():
            if item.item["type"] in ['circle']:
                item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM)

    def add_linestrings(scene):
        for item in scene.project_data.items.values():
            if item.item["type"] in ['linestring']:
                item.draw_on_canvas(scene.project_data.items, scene, ColorMapping.OTHER_ITEM)

    def add_half_ready_segment(scene):
        if scene.select_mode.get_type() == c.Tool.SEGMENT_THROUGH\
        and len(scene.select_history.type_history) == 1:
            Segment.draw_on_canvas_static(
                *scene.project_data.items[scene.select_history.id_history[0]].get_canvas_coordinates(),
                *scene.mouse.get_xy(),
                scene,
                ColorMapping.OTHER_ITEM)

    def add_half_ready_circle(scene):
        if scene.select_mode.get_type() in [c.Tool.CIRCUM_CIRCLE, c.Tool.CIRCLE_WITH_CENTRE]\
        and len(scene.select_history.type_history) + 1 == c.CIRCLE_PATTERN_LENGTH[scene.select_mode.get_type()]:
            centre, radius = scene.item_to_be.recompute_canvas_with_mouse(scene, *scene.mouse.get_xy())
            Circle.draw_on_canvas_static(
                centre, radius, scene,
                ColorMapping.OTHER_ITEM)

    def add_half_ready_linestring(scene):
        if scene.select_mode.get_type() == c.Tool.LINESTRING\
        and scene.select_history.type_history:
            Linestring.draw_on_canvas_static(
                *scene.mouse.get_xy(),
                scene.select_history.id_history,
                scene,
                ColorMapping.OTHER_ITEM_FILL)

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
    if scene.is_aspect_ratio:
        draw_aspect_ratio(scene)
    if scene.show_canvas_items or scene.key_bank.move_point.state == KeyState.DOWN or scene.key_bank.move_canvas.state == KeyState.DOWN:
        add_polygons(scene)
        add_segments(scene)
        add_circles(scene)
        add_linestrings(scene)
    add_half_ready_segment(scene)
    add_half_ready_circle(scene)
    add_half_ready_linestring(scene)
    add_half_ready_polygon(scene)
    if scene.show_canvas_items or scene.key_bank.move_point.state == KeyState.DOWN or scene.key_bank.move_canvas.state == KeyState.DOWN:
        add_points(scene)
    add_item_in_focus(scene)
