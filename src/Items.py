from __future__ import annotations

from PointClasses.FreePoint import FreePoint
from Point import Point
from Segment import Segment
from Circle import Circle
from Polygon import Polygon
from Linestring import Linestring
from Colour import Colour
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
    def __init__(
                self: Items,
                window=c.WindowDefault,
                packages=c.PackagesDefault,
                bg_colour=c.BackGroundColourDefault,  # TODO this should change
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
        self.window = Window(self.window.left - dx, self.window.top - dy, self.window.scale)

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
        num_points = len(list(filter(lambda x: isinstance(x, Point) or isinstance(x, Circle), self.items.values())))
        recomputed_ids = set()
        for item in self.items.values():
            if isinstance(item, FreePoint):
                item.recompute_canvas(self.items, self.window, width, height)
                recomputed_ids.add(item.get_id())

        while len(recomputed_ids) < num_points:
            for item in self.items.values():
                if (isinstance(item, Point) or isinstance(item, Circle)) and item.get_id() not in recomputed_ids:
                    if set(item.depends_on()).issubset(recomputed_ids):
                        item.recompute_canvas(self.items, self.window, width, height)
                        recomputed_ids.add(item.get_id())

    @staticmethod
    def filter_sort_map(class_of, item_filter, tikzify_function, sort_key):
        if sort_key is None and item_filter is None:
            return lambda items: map(tikzify_function,
                                     filter(lambda x: isinstance(x, class_of), items))
        if item_filter is None:
            return lambda items: map(tikzify_function,
                                     sorted(filter(lambda x: isinstance(x, class_of), items), key=sort_key))
        if sort_key is None:
            return lambda items: map(tikzify_function,
                                     filter(lambda x: isinstance(x, class_of) and item_filter(x), items))
        return lambda items: map(tikzify_function,
                                 sorted(filter(lambda x: isinstance(x, class_of) and item_filter(x), items),
                                        key=sort_key))

    def tikzify(self, current_width, current_height, init_width, init_height):
        xmin, xmax = self.window.left, self.window.left + 10 * self.window.scale * current_width / init_height
        ymin, ymax = self.window.top - 10 * self.window.scale * current_height / init_height, self.window.top
        xstep, ystep = 2 * [self.window.scale]

        init_crop = '\\tkzInit[xmin=%.5f, ymin=%.5f, xmax=%.5f,\nymax=%.5f,xstep=%.5f, ystep=%.5f]\n' % \
                    (xmin, ymin, xmax, ymax, xstep, ystep)
        init_crop += '\\tkzClip'

        tikzified_colours = '\n'.join(
            Items.filter_sort_map(Colour, None, lambda x: x.tikzify(), None)(self.items.values()))
        if tikzified_colours:
            tikzified_colours = '% COLOURS\n' + tikzified_colours

        tikzified_points_def = '\n'.join(
            Items.filter_sort_map(Point, None, lambda x: x.tikzify() + '\n' + x.tikzify_node(), None)(
                self.items.values()))
        if tikzified_points_def:
            tikzified_points_def = '% POINT DEFINTIONS\n' + tikzified_points_def

        tikzified_polygons = '\n'.join(
            Items.filter_sort_map(Polygon, lambda x: x.item["show"], lambda x: x.tikzify(), lambda y: y.get_id())(
                self.items.values()))
        if tikzified_polygons:
            tikzified_polygons = '% POLYGONS\n' + tikzified_polygons

        tikzified_nodes_repeat = '\n'.join(
            Items.filter_sort_map(Point, lambda x: x.item["show"], lambda x: x.tikzify_node(), lambda y: y.get_id())(
                self.items.values()))

        tikzified_points_label = '\n'.join(
            Items.filter_sort_map(Point, lambda x: x.item["label"]["show"], lambda x: x.tikzify_label(),
                                  lambda y: y.get_id())(self.items.values()))
        if tikzified_points_label:
            tikzified_points_label = '% POINT LABELS\n' + tikzified_points_label

        tikzified_segments_draw = '\n'.join(
            Items.filter_sort_map(Segment, lambda x: x.item["show"], lambda x: x.tikzify(), lambda y: y.get_id())(
                self.items.values()))
        if tikzified_segments_draw:
            tikzified_segments_draw = '% DRAW SEGMENTS\n' + tikzified_segments_draw

        tikzified_segment_markers_draw = '\n'.join(
            Items.filter_sort_map(Segment, lambda x: x.item["show"], lambda x: x.tikzify_segment_marker(), lambda y: y.get_id())(
                self.items.values()))
        if tikzified_segment_markers_draw:
            tikzified_segment_markers_draw = '% DRAW SEGMENT MARKERS\n' + tikzified_segment_markers_draw

        tikzified_circles_draw = '\n'.join(
            Items.filter_sort_map(Circle, lambda x: x.item["show"], lambda x: x.tikzify(), lambda y: y.get_id())(
                self.items.values()))
        if tikzified_circles_draw:
            tikzified_circles_draw = '% DRAW CIRCLES\n' + tikzified_circles_draw

        tikzified_linestrings_draw = '\n'.join(
            Items.filter_sort_map(Linestring, lambda x: x.item["show"], lambda x: x.tikzify(), lambda y: y.get_id())(
                self.items.values()))
        if tikzified_linestrings_draw:
            tikzified_linestrings_draw = '% DRAW LINESTRINGS\n' + tikzified_linestrings_draw

        object_blocks = [
            self.code_before,
            tikzified_colours,
            init_crop,
            tikzified_points_def,
            tikzified_polygons,
            tikzified_segments_draw,
            tikzified_segment_markers_draw,
            tikzified_circles_draw,
            tikzified_linestrings_draw,
            tikzified_nodes_repeat,
            tikzified_points_label,
            self.code_after
        ]
        string = '\n\n'.join(filter(bool, object_blocks))

        return '\\begin{tikzpicture}\n%s\n\\end{tikzpicture}' % string

    def doc_surround_tikzify(self, current_width, current_height, init_width, init_height):
        string = '\documentclass{standalone}\n'
        string += '\n'.join(self.packages) + '\n'
        string += '\n' + '\\begin{document}' + '\n'
        string += self.tikzify(current_width, current_height, init_width, init_height)
        string += '\n' + '\\end{document}' + '\n'
        return string

    def change_id(self, from_id, to_id):
        print(from_id, to_id)
        self.items[to_id] = self.items.pop(from_id)
        if isinstance(self.items[to_id], Point) and self.items[to_id].item["label"]["text"] == f'${from_id}$':
            self.items[to_id].item["label"]["text"] = f'${to_id}$'
        for item in self.items.values():
            item.change_id(from_id, to_id)

    def state_dict(self):
        dictionary = {'items': []}
        for item in self.items.values():
            dictionary["items"].append(item.item)
        dictionary["window"] = {'left': self.window.left, 'top': self.window.top, 'scale': self.window.scale}
        dictionary["bg_colour"] = self.bg_colour
        dictionary["code_before"] = self.code_before
        dictionary["code_after"] = self.code_after
        dictionary["packages"] = self.packages
        return dictionary
