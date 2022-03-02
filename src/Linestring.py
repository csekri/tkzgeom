from PyQt5 import QtCore, QtWidgets, QtGui

from Item import Item
from Tikzifyables.Arrowable import Arrowable
from Tikzifyables.DashPatternable import DashPatternable
from Tikzifyables.Colourable.LineColourable import LineColourable
from Tikzifyables.Fillable import Fillable
from Tikzifyables.Decorationable import Decorationable
import Constant as c
from GeometryMath import point_segment_dist_sqr


class Linestring(Item, DashPatternable, LineColourable, Decorationable):
    def __init__(self, item):
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "")
        DashPatternable.__init__(self, self.item)
        LineColourable.__init__(self, self.item)
        Decorationable.__init__(self, self.item)

    def tikzify(self):
        options = [
            self.tikzify_dash(),
            'draw=' + self.tikzify_line_colour(),
            self.tikzify_decoration()
        ]
        options = filter(bool, options)
        return "\\draw[%s](%s.center)--cycle;" % (', '.join(options), ')--('.join(self.item["definition"]))

    def __str__(self): # TODO modify this too, this is now an error
        return "Segment from (%s) to (%s)" % (self.item["definition"]["A"], self.item["definition"]["B"])

    def draw_on_canvas(self, items, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        coord_list = [items[i].get_canvas_coordinates() for i in self.item["definition"]]
        for i in range(len(coord_list) - 1):
            graphics_line = QtWidgets.QGraphicsLineItem(*coord_list[i], *coord_list[i + 1])
            pen = QtGui.QPen()
            pen.setWidth(thickness)
            pen.setDashPattern([4, 4])
            pen.setColor(colour)
            graphics_line.setPen(pen)
            scene.addItem(graphics_line)

    @staticmethod
    def draw_on_canvas_static(x, y, id_history, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        coord_list = [scene.project_data.items[i].get_canvas_coordinates() for i in id_history] + [[x, y]]
        for i in range(len(coord_list) - 1):
            graphics_line = QtWidgets.QGraphicsLineItem(*coord_list[i], *coord_list[i + 1])
            pen = QtGui.QPen()
            pen.setWidth(thickness)
            pen.setColor(colour)
            pen.setDashPattern([4, 4])
            graphics_line.setPen(pen)
            scene.addItem(graphics_line)

    def distance_sqr(self, x, y, items):
        min_dist = 1e6
        coord_list = [items[i].get_canvas_coordinates() for i in self.depends_on()]
        for i in range(len(coord_list) - 1):
            if (distance := point_segment_dist_sqr(coord_list[i], coord_list[i + 1], [x, y])) < min_dist:
                min_dist = distance
        return min_dist

    def depends_on(self):
        return self.item["definition"]

    def definition_builder(self, data):
        return data

    @staticmethod
    def static_patterns():
        return [i * 'p' for i in range(3, 40)]

    def patterns(self):
        return [i * 'p' for i in range(3, 40)]

    def next_id_func(self, definition, iter_counter):
        return 'Linestring_' + chr(ord('A') + iter_counter % 26) + (iter_counter // 26) * '\''

    def definition_builder(self, data, items=None):
        return data[:-1]

    def dictionary_builder(self, definition, id, sub_type=None): # TODO create Linestring class in Constant.py and modify entries here
        dictionary = {}
        dictionary["id"] = id
        dictionary["type"] = 'linestring'
        dictionary["show"] = True
        dictionary["definition"] = definition
        dictionary["line"] = {}
        dictionary["line"]["line_width"] = c.Linestring.Default.LINE_WIDTH
        dictionary["line"]["colour"] = {}
        dictionary["line"]["colour"]["name"] = c.Linestring.Default.Line_Colour.NAME
        dictionary["line"]["colour"]["mix_with"] = c.Linestring.Default.Line_Colour.MIX_WITH
        dictionary["line"]["colour"]["mix_percent"] = c.Linestring.Default.Line_Colour.MIX_RATIO
        dictionary["line"]["colour"]["strength"] = c.Linestring.Default.Line_Colour.STRENGTH
        dictionary["line"]["dash"] = {}
        dictionary["line"]["dash"]["stroke"] = c.Linestring.Default.LINE_DASH_STROKE
        dictionary["line"]["dash"]["custom_pattern"] = c.Linestring.Default.LINE_DASH_CUSTOM
        dictionary["line"]["double"] = {}
        dictionary["line"]["double"]["distance"] = c.Linestring.Default.Double_Line.DISTANCE
        dictionary["line"]["double"]["colour"] = {}
        dictionary["line"]["double"]["colour"]["name"] = c.Linestring.Default.Double_Line.Colour.NAME
        dictionary["line"]["double"]["colour"]["mix_with"] = c.Linestring.Default.Double_Line.Colour.MIX_WITH
        dictionary["line"]["double"]["colour"]["mix_percent"] = c.Linestring.Default.Double_Line.Colour.MIX_RATIO
        dictionary["line"]["double"]["colour"]["strength"] = c.Linestring.Default.Double_Line.Colour.STRENGTH
        dictionary["line"]["decoration"] = {}
        dictionary["line"]["decoration"]["type"] = c.Linestring.Default.Decoration.TYPE
        dictionary["line"]["decoration"]["amplitude"] = c.Linestring.Default.Decoration.AMPLITUDE
        dictionary["line"]["decoration"]["wavelength"] = c.Linestring.Default.Decoration.WAVELENGTH
        dictionary["line"]["decoration"]["text"] = c.Linestring.Default.Decoration.TEXT
        # dictionary["line"]["o_extension"] = 0.0
        # dictionary["line"]["d_extension"] = 1.0
        dictionary["line"]["o_connect_to"] = c.Linestring.Default.LINE_CONNECT_TO
        dictionary["line"]["d_connect_to"] = c.Linestring.Default.LINE_CONNECT_TO
        dictionary["o_arrow"] = {}
        dictionary["o_arrow"]["width"] = c.Linestring.Default.O_Arrow.WIDTH
        dictionary["o_arrow"]["length"] = c.Linestring.Default.O_Arrow.LENGTH
        dictionary["o_arrow"]["tip"] = c.Linestring.Default.O_Arrow.TIP
        dictionary["o_arrow"]["bending"] = c.Linestring.Default.O_Arrow.BENDING
        dictionary["o_arrow"]["side"] = c.Linestring.Default.O_Arrow.SIDE
        dictionary["o_arrow"]["reversed"] = c.Linestring.Default.O_Arrow.REVERSED
        dictionary["d_arrow"] = {}
        dictionary["d_arrow"]["width"] = c.Linestring.Default.D_Arrow.WIDTH
        dictionary["d_arrow"]["length"] = c.Linestring.Default.D_Arrow.LENGTH
        dictionary["d_arrow"]["tip"] = c.Linestring.Default.D_Arrow.TIP
        dictionary["d_arrow"]["bending"] = c.Linestring.Default.D_Arrow.BENDING
        dictionary["d_arrow"]["side"] = c.Linestring.Default.D_Arrow.SIDE
        dictionary["d_arrow"]["reversed"] = c.Linestring.Default.D_Arrow.REVERSED

        self.item = dictionary
