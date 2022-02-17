# standard and pip imports
import sys, os, json
import numpy as np
import json
from PyQt5 import QtCore, QtWidgets, QtGui
from copy import deepcopy

from Mouse import Mouse
from Factory import Factory
from Items import Items
from Save import EditManagement
from PointClasses.FreePoint import FreePoint
import Constant as c
from SelectPattern import SelectMode, ItemAccumulator
from HighlightItem import item_in_focus
import CanvasRendering as cr
from KeyBank import KeyBank, KeyState
from Fill.ListWidget import fill_listWidget_with_data
from SyntaxHighlight import syntax_highlight
from Tikzifyables.Labelable import Labelable


# class for the graphics scene (canvas)
class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__ (self):
        """Construct the graphicsScene class."""
        super(GraphicsScene, self).__init__ ()

        self.mouse = Mouse()
        self.project_data = Items()
        self.edit = EditManagement()
        self.key_bank = KeyBank()
        self.select_mode = SelectMode(0, 0)
        self.select_history = ItemAccumulator()
        self.mock_item = None
        self.focus_id = ''
        self.current_tab_idx = 0

    def mousePressEvent(self, event):
        self.mouse.set_xy(int(event.scenePos().x()), int(event.scenePos().y()))
        self.mouse.set_pressed_xy(int(event.scenePos().x()), int(event.scenePos().y()))

        if self.select_mode.get_type() == c.Tool.FREE:
            item = Factory.create_empty_item("point", c.Point.Definition.FREE)
            definition = item.definition_builder(
                FreePoint.phi_inverse(self.project_data.window, *self.mouse.get_xy(), 641, 641), None)
            item.item["id"] = Factory.next_id(item, definition, self.project_data.items)
            item.item["definition"] = definition
            item.item["label"]["text"] = f'${item.item["id"]}$'
            if isinstance(item, Labelable):
                item.id = item.item["id"]
            self.project_data.add(item)
            fill_listWidget_with_data(self.project_data, self.widgets["list_widget"], self.current_tab_idx)
            browser_text = syntax_highlight(self.project_data.tikzify())
            self.widgets["text_browser"].setText(browser_text)
        else:
            focus = item_in_focus(self.project_data, self.mouse)
            if not bool(focus):
                self.select_history.reset_history()
                return None
            self.select_history.add_to_history(focus, self.project_data.items[focus].item["type"])
            if self.select_mode.get_type() == c.Tool.SEGMENT_THROUGH:
                item = Factory.create_empty_item("segment", c.Point.Definition.FREE)
            if self.select_mode.get_type() == c.Tool.MIDPOINT_SEGMENT:
                item = Factory.create_empty_item("point", c.Point.Definition.SEGMENT_MIDPOINT)
            if self.select_mode.get_type() == c.Tool.POLYGON:
                item = Factory.create_empty_item("polygon", c.Point.Definition.SEGMENT_MIDPOINT)



            if ids := self.select_history.match_pattern(item.patterns()):
                definition = item.definition_builder(ids, self.project_data.items)
                id = Factory.next_id(item, definition, self.project_data.items)
                item.item["definition"] = definition
                item.item["id"] = id
                self.project_data.add(item)
                fill_listWidget_with_data(self.project_data, self.widgets["list_widget"], self.current_tab_idx)
                browser_text = syntax_highlight(self.project_data.tikzify())
                self.widgets["text_browser"].setText(browser_text)
        self.project_data.recompute_canvas(641, 641)
        cr.clear(self)
        cr.add_all_items(self)


    def mouseMoveEvent(self, event):
        old_x, old_y = self.mouse.get_xy()
        self.mouse.set_xy(int(event.scenePos().x()), int(event.scenePos().y()))
        if self.key_bank.move_point.state == KeyState.DOWN and self.focus_id:
            definition = self.project_data.items[self.focus_id].definition_builder(
                FreePoint.phi_inverse(self.project_data.window, *self.mouse.get_xy(), 641, 641), None)
            self.project_data.items[self.focus_id].item["definition"] = definition

        if self.key_bank.move_canvas.state == KeyState.DOWN:
            old_tikz_dx, old_tikz_dy = FreePoint.phi_inverse(self.project_data.window, old_x, old_y, 641, 641)
            tikz_dx, tikz_dy = FreePoint.phi_inverse(self.project_data.window, *self.mouse.get_xy(), 641, 641)
            self.project_data.set_window_translate(tikz_dx-old_tikz_dx, tikz_dy-old_tikz_dy)

        self.project_data.recompute_canvas(641, 641)
        cr.clear(self)
        cr.add_all_items(self)


    def mouseReleaseEvent(self, event):
        self.mouse.set_xy(int(event.scenePos().x()), int(event.scenePos().y()))
        browser_text = syntax_highlight(self.project_data.tikzify())
        self.widgets["text_browser"].setText(browser_text)


    def get_main_window_references(self, widgets):
        self.widgets = widgets
