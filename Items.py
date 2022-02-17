from PointClasses.FreePoint import FreePoint
from Point import Point
from PointClasses.Midpoint import Midpoint
from Segment import Segment
from HighlightItem import item_in_focus
from PyQt5 import QtCore
import Constant as c

from collections import namedtuple

Window = namedtuple('Window', ['left', 'top', 'scale'])


class Items:
    def __init__(self,
            window=c.WindowDefault,
            packages=c.PackagesDefault,
            bg_colour=c.BackGroundColourDefault,
            colours=[],
            code_before='',
            code_after=''):
        self.items = {}
        self.window = Window(left=window["left"], top=window["top"], scale=window["scale"])
        self.packages = packages
        self.bg_colour = bg_colour
        self.colours = colours
        self.code_before = code_before
        self.code_after = code_after

    def set_window(self, left, top, scale):
        self.window = Window(left=left, top=top, scale=scale)

    def set_window_translate(self, dx, dy):
        self.window = Window(self.window.left-dx, self.window.top-dy, self.window.scale)

    def add(self, item):
        self.items[item.get_id()] = item

    def __str__(self):
        if not self.items:
            return '[]'
        string = '[\n'
        for item in self.items.values():
            string += '    ' + str(item) + '\n'
        string += ']'
        return string

    def recompute_canvas(self, width, height):
        num_points = len(list(filter(lambda x: isinstance(x, Point), self.items.values())))
        recomputed_ids = set()
        for item in self.items.values():
            if isinstance(item, FreePoint):
                item.recompute_canvas(self.items, self.window, width, height)
                recomputed_ids.add(item.get_id())

        while len(recomputed_ids) < num_points:
            for item in self.items.values():
                if isinstance(item, Point) and item.get_id() not in recomputed_ids:
                    if set(item.depends_on()).issubset(recomputed_ids):
                        item.recompute_canvas(self.items, self.window, width, height)
                        recomputed_ids.add(item.get_id())






    @staticmethod
    def filter_sort_map(class_of, tikzify_function, sort_key):
        return lambda items: map(tikzify_function, sorted(filter(lambda x: isinstance(x, class_of), items), key=sort_key))


    def tikzify(self):

        tikzified_points_def = '\n'.join(filter(bool, [
            '\n'.join(Items.filter_sort_map(FreePoint, lambda x: x.tikzify()+'\n'+x.tikzify_node(), lambda y: y.get_id())(self.items.values())),
            '\n'.join(Items.filter_sort_map(Midpoint, lambda x: x.tikzify()+'\n'+x.tikzify_node(), lambda y: y.get_id())(self.items.values())),
        ]))
        if tikzified_points_def:
            tikzified_points_def = '% POINT DEFINTIONS\n' + tikzified_points_def

        tikzified_points_label = '\n'.join(Items.filter_sort_map(Point, lambda x: x.tikzify_label(), lambda y: y.get_id())(self.items.values()))
        if tikzified_points_label:
            tikzified_points_label = '% POINT LABELS\n' + tikzified_points_label


        tikzified_segments_draw = '\n'.join(Items.filter_sort_map(Segment, lambda x: x.tikzify(), lambda y: y.get_id())(self.items.values()))
        if tikzified_segments_draw:
            tikzified_segments_draw = '% DRAW SEGMENTS\n' + tikzified_segments_draw

        object_blocks = [
            tikzified_points_def,
            tikzified_points_label,
            tikzified_segments_draw,
        ]
        string = '\n\n'.join(filter(bool, object_blocks))

        return '\\begin{tikzpicture}\n%s\n\\end{tikzpicture}' % string

    def doc_surround_tikzify(self):
        string = '\documentclass[tikz]{standalone}\n'
        string += '\n'.join(self.packages)
        string += '\n' + '\\begin{document}' + '\n'
        string += self.tikzify()
        string += '\n' + '\\end{document}' + '\n'
        return string

    def change_id(self, from_id, to_id):
        for item in self.items:
            item.change_id(from_id, to_id)


    def save_into_file(self):
        dictionary = { 'items': 0}
        for item in self.items.values():
            dictionary
