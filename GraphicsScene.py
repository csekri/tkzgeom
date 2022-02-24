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
from Tikzifyables.Labelable import Labelable
import Constant as c
from SelectPattern import SelectMode, ItemAccumulator
from HighlightItem import item_in_focus
import CanvasRendering as cr
from KeyBank import KeyBank, KeyState
from Fill.ListWidget import fill_listWidget_with_data, listWidget_set_current_row
from SyntaxHighlight import syntax_highlight
from Tikzifyables.Labelable import Labelable
from Segment import Segment
from GeometryMath import dist, ortho_proj


# class for the graphics scene (canvas)
class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__ (self, widgets, title):
        """Construct the graphicsScene class."""
        super(GraphicsScene, self).__init__ ()

        self.mouse = Mouse()
        self.project_data = Items()
        self.select_mode = SelectMode(0, 0)
        self.widgets = widgets
        self.title = title # function from main window to set window title
        self.auto_compile = False
        self.show_pdf = False
        self.show_canvas_labels = True
        self.show_canvas_items = True
        self.select_history = ItemAccumulator()
        self.edit = EditManagement()
        self.edit.add_undo_item(self)
        self.key_bank = KeyBank()
        self.mock_item = None
        self.focus_id = ''
        self.current_tab_idx = 0
        self.list_focus_ids = [0]

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
            self.project_data.recompute_canvas(641, 641)
            self.edit.add_undo_item(self)
            fill_listWidget_with_data(self.project_data, self.widgets["list_widget"], self.current_tab_idx)
            self.widgets["tab_widget"].setCurrentIndex(c.TYPES.index('point'))
            listWidget_set_current_row(self.widgets["list_widget"], item.get_id())
            browser_text = syntax_highlight(self.project_data.tikzify())
            self.widgets["text_browser"].setText(browser_text)
        else:
            focus = item_in_focus(self.project_data, self.mouse)
            print('focus', focus)
            if not bool(focus):
                self.select_history.reset_history()
                return None
            self.select_history.add_to_history(focus, self.project_data.items[focus].item["type"])
            type, sub_type = c.Tool.TYPE_MAP[self.select_mode.get_type()]
            item = Factory.create_empty_item(type, sub_type)

            if ids := self.select_history.match_pattern(item.patterns()):
                if self.select_mode.get_type() == c.Tool.POLYGON:
                    if ids[0] != ids[-1]:
                        self.select_history.id_history = ids
                        self.select_history.type_history = ''.join(map(lambda x: self.select_history.type_map[self.project_data.items[x].item["type"]], ids))
                        return None
                if self.select_mode.get_type() == c.Tool.POINT_ON_LINE:
                    A, B = self.project_data.items[ids[0]].item["definition"].values()
                    A_coords = self.project_data.items[A].get_canvas_coordinates()
                    B_coords = self.project_data.items[B].get_canvas_coordinates()
                    AP = dist(A_coords, self.mouse.get_xy())
                    PB = dist(B_coords, self.mouse.get_xy())
                    ratio = AP / (AP + PB)
                    ids = [A, B, ratio]
                definition = item.definition_builder(ids, self.project_data.items)
                id = Factory.next_id(item, definition, self.project_data.items)
                item.item["definition"] = definition
                item.item["id"] = id
                if isinstance(item, Labelable):
                    item.item["label"]["text"] = f'${item.item["id"]}$'
                if isinstance(item, Segment):
                    item.item["o_arrow"]["tip"] = 'Stealth'
                self.project_data.add(item)
                self.project_data.recompute_canvas(641, 641)
                self.edit.add_undo_item(self)
                fill_listWidget_with_data(self.project_data, self.widgets["list_widget"], self.current_tab_idx)
                self.widgets["tab_widget"].setCurrentIndex(c.TYPES.index(type))
                listWidget_set_current_row(self.widgets["list_widget"], item.get_id())
                browser_text = syntax_highlight(self.project_data.tikzify())
                self.widgets["text_browser"].setText(browser_text)
        cr.clear(self)
        cr.add_all_items(self)


    def mouseMoveEvent(self, event):
        old_x, old_y = self.mouse.get_xy()
        self.mouse.set_xy(int(event.scenePos().x()), int(event.scenePos().y()))

        focus = item_in_focus(self.project_data, self.mouse)
        if focus and self.project_data.items[focus].item["type"] == 'point'\
        and self.select_history.type_history:
            self.mouse.set_xy(*self.project_data.items[focus].get_canvas_coordinates())

        if self.key_bank.move_point.state == KeyState.DOWN and self.focus_id:
            focus_subtype = self.project_data.items[self.focus_id].item["sub_type"]
            if focus_subtype == c.Point.Definition.FREE:
                definition = self.project_data.items[self.focus_id].definition_builder(
                    FreePoint.phi_inverse(self.project_data.window, *self.mouse.get_xy(), 641, 641), None)
                self.project_data.items[self.focus_id].item["definition"] = definition
            elif focus_subtype == c.Point.Definition.ON_LINE:
                A, B = self.project_data.items[self.focus_id].depends_on()
                A_coords = self.project_data.items[A].get_canvas_coordinates()
                B_coords = self.project_data.items[B].get_canvas_coordinates()
                ortho_point = ortho_proj(A_coords, B_coords, self.mouse.get_xy())
                AP = dist(A_coords, ortho_point)
                PB = dist(B_coords, ortho_point)
                AB = dist(A_coords, B_coords)
                if (AP + AB - PB) ** 2 < 1e-9:
                    ratio = -AP / AB
                else:
                    ratio = AP / AB
                definition = self.project_data.items[self.focus_id].definition_builder(
                    [A, B, ratio], None)
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
