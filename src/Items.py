from PointClasses.FreePoint import FreePoint
from PointClasses.Midpoint import Midpoint
from PointClasses.OnLine import OnLine
from Point import Point
from Segment import Segment
from Polygon import Polygon
from Colour import Colour
from HighlightItem import item_in_focus
from PyQt5 import QtCore
import Constant as c

from collections import namedtuple, OrderedDict

Window = namedtuple('Window', ['left', 'top', 'scale'])

'''
colours=[
    {
        "id": "horseWhite",
        "definition": "#ededf0"
    },
    {
        "id": "loveRed",
        "definition": "#d50402"
    }
]
'''

class Items:
    def __init__(self,
            window=c.WindowDefault,
            packages=c.PackagesDefault,
            bg_colour=c.BackGroundColourDefault,
            code_before='',
            code_after=''):
        self.items = OrderedDict()
        self.window = Window(left=window["left"], top=window["top"], scale=window["scale"])
        self.packages = packages
        self.bg_colour = bg_colour
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
        if sort_key is None:
            return lambda items: map(tikzify_function, filter(lambda x: isinstance(x, class_of), items))
        return lambda items: map(tikzify_function, sorted(filter(lambda x: isinstance(x, class_of), items), key=sort_key))


    def tikzify(self):
        init_crop = '\\edef\\xmin{%f}\\edef\\xmax{%f}\n'  % (self.window.left, self.window.left + 10 * self.window.scale)
        init_crop += '\\edef\\ymin{%f}\\edef\\ymax{%f}\n'  % (self.window.top - 10 * self.window.scale, self.window.top)
        init_crop += "\\edef\\xstep{%f}"  % self.window.scale
        init_crop += "\\edef\\ystep{%f}\n"  % self.window.scale
        init_crop += "\\tkzInit[xmin=\\xmin, ymin=\\ymin, xmax=\\xmax, ymax=\\ymax, xstep=\\xstep, ystep=\\ystep]\n"
        init_crop += "\\tkzClip\n"

        # tikzified_colours = \
        #     '\n'.join([('\\definecolor{%s}{HTML}{%s}' % (i["id"], i["definition"][1:])) for i in self.colours])
        tikzified_colours = '\n'.join(Items.filter_sort_map(Colour, lambda x: x.tikzify(), None)(self.items.values()))
        if tikzified_colours:
            tikzified_colours = '% COLOURS\n' + tikzified_colours


        tikzified_points_def = '\n'.join(Items.filter_sort_map(Point, lambda x: x.tikzify()+'\n'+x.tikzify_node(), None)(self.items.values()))
        if tikzified_points_def:
            tikzified_points_def = '% POINT DEFINTIONS\n' + tikzified_points_def


        tikzified_polygons = '\n'.join(Items.filter_sort_map(Polygon, lambda x: x.tikzify(), lambda y: y.get_id())(self.items.values()))
        if tikzified_polygons:
            tikzified_polygons = '% POLYGONS\n' + tikzified_polygons

        tikzified_nodes_repeat = \
        '\n'.join(Items.filter_sort_map(Point, lambda x: x.tikzify_node(), lambda y: y.get_id())(self.items.values()))\
        if tikzified_polygons else ''


        tikzified_points_label = '\n'.join(Items.filter_sort_map(Point, lambda x: x.tikzify_label(), lambda y: y.get_id())(self.items.values()))
        if tikzified_points_label:
            tikzified_points_label = '% POINT LABELS\n' + tikzified_points_label


        tikzified_segments_draw = '\n'.join(Items.filter_sort_map(Segment, lambda x: x.tikzify(), lambda y: y.get_id())(self.items.values()))
        if tikzified_segments_draw:
            tikzified_segments_draw = '% DRAW SEGMENTS\n' + tikzified_segments_draw

        object_blocks = [
            tikzified_colours,
            init_crop,
            tikzified_points_def,
            tikzified_polygons,
            tikzified_points_label,
            tikzified_segments_draw,
            tikzified_nodes_repeat,
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


    def state_dict(self):
        dictionary = { 'items' : []}
        for item in self.items.values():
            dictionary["items"].append(item.item)
        dictionary["window"] = { 'left': self.window.left, 'top': self.window.top, 'scale': self.window.scale}
        dictionary["bg_colour"] = self.bg_colour
        dictionary["code_before"] = self.code_before
        dictionary["code_after"] = self.code_after
        dictionary["packages"] = self.packages
        return dictionary
