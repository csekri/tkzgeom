from PyQt5 import QtCore, QtWidgets, QtGui

from Item import Item
from Point import Point
from Tikzifyables.Arrowable import Arrowable
from Tikzifyables.DashPatternable import DashPatternable
from Tikzifyables.Doubleable import Doubleable
from Tikzifyables.Colourable.LineColourable import LineColourable
import Constant as c
import GeometryMath as gmath
from math import sin, cos, pi, radians


class Circle(Item, Arrowable, DashPatternable, Doubleable, LineColourable):
    def __init__(self, item):
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "", "")
        Arrowable.__init__(self, self.item)
        DashPatternable.__init__(self, self.item)
        Doubleable.__init__(self, self.item)
        LineColourable.__init__(self, self.item)
        self.__canvas_centre_x = 0
        self.__canvas_centre_y = 0
        self.__canvas_radius = 0

    def tikzify(self):
        return NotImplementedError

    def set_canvas_radius(self, radius):
        self.__canvas_radius = radius

    def get_canvas_radius(self):
        return self.__canvas_radius

    def get_canvas_centre_xy(self):
        return self.__canvas_centre_x, self.__canvas_centre_y

    def set_canvas_centre_xy(self, x, y):
        self.__canvas_centre_x, self.__canvas_centre_y = x, y

    def __str__(self):
        return NotImplementedError

    def draw_on_canvas(self, items, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        centre = self.get_canvas_centre_xy()
        radius = self.get_canvas_radius()
        graphics_point = QtWidgets.QGraphicsEllipseItem(*gmath.sub(centre, [radius, radius]), 2*radius, 2*radius)
        pen = QtGui.QPen()
        pen.setWidth(thickness)
        pen.setColor(colour)
        graphics_point.setPen(pen)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.NoBrush)
        graphics_point.setBrush(brush)
        scene.addItem(graphics_point)

    @staticmethod
    def draw_on_canvas_static(centre, radius, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        graphics_point = QtWidgets.QGraphicsEllipseItem(*gmath.sub(centre, [radius, radius]), 2*radius, 2*radius)
        pen = QtGui.QPen()
        pen.setWidth(thickness)
        pen.setColor(colour)
        graphics_point.setPen(pen)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.NoBrush)
        graphics_point.setBrush(brush)
        scene.addItem(graphics_point)

    def recompute_canvas_with_mouse(self, scene, x, y):
        return NotImplementedError

    def distance_sqr(self, x, y, items):
        O = self.get_canvas_centre_xy()
        r = self.get_canvas_radius()
        P = x, y
        return gmath.pt_circle_dist_sqr(O, r, P)

    def definition_builder(self, data, items=None):
        return NotImplementedError

    def patterns(self):
        return NotImplementedError

    def next_id_func(self, definition, iter_counter):
        return 'Circle_' + chr(ord('A') + iter_counter % 26) + (iter_counter // 26) * '\''

    def dictionary_builder(self, definition, id, sub_type=None):  # TODO to be updated
        dictionary = {}
        dictionary["id"] = id
        dictionary["type"] = 'circle'
        dictionary["sub_type"] = sub_type
        dictionary["show"] = True
        dictionary["definition"] = definition
        dictionary["label"] = {}
        dictionary["label"]["show"] = c.Segment.Default.Label.SHOW
        dictionary["label"]["text"] = c.Segment.Default.Label.TEXT
        dictionary["label"]["anchor"] = c.Segment.Default.Label.ANCHOR
        dictionary["label"]["offset"] = c.Segment.Default.Label.OFFSET
        dictionary["line"] = {}
        dictionary["line"]["line_width"] = c.Segment.Default.LINE_WIDTH
        dictionary["line"]["colour"] = {}
        dictionary["line"]["colour"]["name"] = c.Segment.Default.Line_Colour.NAME
        dictionary["line"]["colour"]["mix_with"] = c.Segment.Default.Line_Colour.MIX_WITH
        dictionary["line"]["colour"]["mix_percent"] = c.Segment.Default.Line_Colour.MIX_RATIO
        dictionary["line"]["colour"]["strength"] = c.Segment.Default.Line_Colour.STRENGTH
        dictionary["line"]["dash"] = {}
        dictionary["line"]["dash"]["stroke"] = c.Segment.Default.LINE_DASH_STROKE
        dictionary["line"]["dash"]["custom_pattern"] = c.Segment.Default.LINE_DASH_CUSTOM
        dictionary["line"]["double"] = {}
        dictionary["line"]["double"]["distance"] = c.Segment.Default.Double_Line.DISTANCE
        dictionary["line"]["double"]["colour"] = {}
        dictionary["line"]["double"]["colour"]["name"] = c.Segment.Default.Double_Line.Colour.NAME
        dictionary["line"]["double"]["colour"]["mix_with"] = c.Segment.Default.Double_Line.Colour.MIX_WITH
        dictionary["line"]["double"]["colour"]["mix_percent"] = c.Segment.Default.Double_Line.Colour.MIX_RATIO
        dictionary["line"]["double"]["colour"]["strength"] = c.Segment.Default.Double_Line.Colour.STRENGTH
        dictionary["line"]["o_extension"] = 0.0
        dictionary["line"]["d_extension"] = 1.0
        dictionary["line"]["o_connect_to"] = c.Segment.Default.LINE_CONNECT_TO
        dictionary["line"]["d_connect_to"] = c.Segment.Default.LINE_CONNECT_TO
        dictionary["o_arrow"] = {}
        dictionary["o_arrow"]["width"] = c.Segment.Default.O_Arrow.WIDTH
        dictionary["o_arrow"]["length"] = c.Segment.Default.O_Arrow.LENGTH
        dictionary["o_arrow"]["tip"] = c.Segment.Default.O_Arrow.TIP
        dictionary["o_arrow"]["bending"] = c.Segment.Default.O_Arrow.BENDING
        dictionary["o_arrow"]["side"] = c.Segment.Default.O_Arrow.SIDE
        dictionary["o_arrow"]["reversed"] = c.Segment.Default.O_Arrow.REVERSED
        dictionary["d_arrow"] = {}
        dictionary["d_arrow"]["width"] = c.Segment.Default.D_Arrow.WIDTH
        dictionary["d_arrow"]["length"] = c.Segment.Default.D_Arrow.LENGTH
        dictionary["d_arrow"]["tip"] = c.Segment.Default.D_Arrow.TIP
        dictionary["d_arrow"]["bending"] = c.Segment.Default.D_Arrow.BENDING
        dictionary["d_arrow"]["side"] = c.Segment.Default.D_Arrow.SIDE
        dictionary["d_arrow"]["reversed"] = c.Segment.Default.D_Arrow.REVERSED
        dictionary["fill"] = {}
        # dictionary["fill"]["colour"] = {}
        # dictionary["fill"]["colour"]["name"] = c.Point.Default.Fill_Colour.NAME
        # dictionary["fill"]["colour"]["mix_with"] = c.Point.Default.Fill_Colour.MIX_WITH
        # dictionary["fill"]["colour"]["mix_percent"] = c.Point.Default.Fill_Colour.MIX_RATIO
        # dictionary["fill"]["colour"]["strength"] = c.Point.Default.Fill_Colour.STRENGTH

        self.item = dictionary

