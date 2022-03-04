from PyQt5 import QtCore, QtWidgets, QtGui
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon

from Item import Item
from Tikzifyables.Arrowable import Arrowable
from Tikzifyables.DashPatternable import DashPatternable
from Tikzifyables.Colourable.LineColourable import LineColourable
from Tikzifyables.Fillable import Fillable
from Tikzifyables.Decorationable import Decorationable
import Constant as c

class Polygon(Item, DashPatternable, LineColourable, Fillable, Decorationable):
    def __init__(self, item):
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "")
        DashPatternable.__init__(self, self.item)
        LineColourable.__init__(self, self.item)
        Fillable.__init__(self, self.item)
        Decorationable.__init__(self, self.item)

    def tikzify(self):
        options = [
            self.tikzify_dash(),
            'draw=' + self.tikzify_line_colour(),
            self.tikzify_fill_pattern(),
            self.tikzify_decoration()
        ]
        options = filter(bool, options)
        return "\\fill[%s](%s.center)--cycle;" % ( ', '.join(options) , '.center)--('.join(self.item["definition"]))

    def __str__(self):
        return "Segment from (%s) to (%s)" % (self.item["definition"]["A"], self.item["definition"]["B"])

    def draw_on_canvas(self, items, scene, colour=QtCore.Qt.darkMagenta):
        qpolygon = QtGui.QPolygonF([QtCore.QPointF(*items[i].get_canvas_coordinates()) for i in self.item["definition"]])
        polygon_item = QtWidgets.QGraphicsPolygonItem(qpolygon)
        polygon_item.setBrush(QtGui.QBrush(colour))
        pen = QtGui.QPen()
        pen.setStyle(QtCore.Qt.NoPen)
        polygon_item.setPen(pen)
        scene.addItem(polygon_item)

    def definition_string(self):
        def_str = [('{0:.6g}'.format(i) if isinstance(i, float) else i) for i in self.item["definition"]]
        return '%s(%s)' % (type(self).__name__, ', '.join(def_str))

    @staticmethod
    def draw_on_canvas_static(x, y, id_history, scene, colour=QtCore.Qt.darkMagenta):
        coordinates = [QtCore.QPointF(*scene.project_data.items[x].get_canvas_coordinates()) for x in id_history]
        qpolygon = QtGui.QPolygonF(coordinates + [QtCore.QPointF(x, y)])
        polygon_item = QtWidgets.QGraphicsPolygonItem(qpolygon)
        polygon_item.setBrush(QtGui.QBrush(colour))
        pen = QtGui.QPen()
        pen.setStyle(QtCore.Qt.NoPen)
        polygon_item.setPen(pen)
        scene.addItem(polygon_item)



    def is_inside(self, x, y, items):
        polygon_coordinates = []
        for item_id in self.depends_on():
            polygon_coordinates.append(items[item_id].get_canvas_coordinates())
        shapely_polygon = ShapelyPolygon(polygon_coordinates)
        return shapely_polygon.contains(ShapelyPoint(x, y))

    def depends_on(self):
        return self.item["definition"]

    @staticmethod
    def static_patterns():
        return [i*'p' for i in range(3,40)]

    def patterns(self):
        return [i*'p' for i in range(3,40)]

    def next_id_func(self, definition, iter_counter):
        return 'Polygon_' + chr(ord('A') + iter_counter % 26) + (iter_counter // 26) * '\''

    def definition_builder(self, data, items=None):
        return data[:-1]

    def parse_into_definition(self, arguments, items):
        if len(arguments) <= 2:
            return None
        condition = not all(map(lambda x: self.name_pattern(x), arguments))
        if condition:
            return None
        return self.definition_builder(arguments + ["mock_item"])

    def dictionary_builder(self, definition, id, sub_type=None):
        dictionary = {}
        dictionary["id"] = id
        dictionary["type"] = 'polygon'
        dictionary["sub_type"] = None
        dictionary["show"] = True
        dictionary["definition"] = definition
        dictionary["line"] = {}
        dictionary["line"]["line_width"] = c.Polygon.Default.LINE_WIDTH
        dictionary["line"]["colour"] = {}
        dictionary["line"]["colour"]["name"] = c.Polygon.Default.Line_Colour.NAME
        dictionary["line"]["colour"]["mix_with"] = c.Polygon.Default.Line_Colour.MIX_WITH
        dictionary["line"]["colour"]["mix_percent"] = c.Polygon.Default.Line_Colour.MIX_RATIO
        dictionary["line"]["colour"]["strength"] = c.Polygon.Default.Line_Colour.STRENGTH
        dictionary["line"]["dash"] = {}
        dictionary["line"]["dash"]["stroke"] = c.Polygon.Default.LINE_DASH_STROKE
        dictionary["line"]["dash"]["custom_pattern"] = c.Polygon.Default.LINE_DASH_CUSTOM
        dictionary["line"]["decoration"] = {}
        dictionary["line"]["decoration"]["type"] = c.Polygon.Default.Decoration.TYPE
        dictionary["line"]["decoration"]["amplitude"] = c.Polygon.Default.Decoration.AMPLITUDE
        dictionary["line"]["decoration"]["wavelength"] = c.Polygon.Default.Decoration.WAVELENGTH
        dictionary["line"]["decoration"]["text"] = c.Polygon.Default.Decoration.TEXT
        dictionary["fill"] = {}
        dictionary["fill"]["colour"] = {}
        dictionary["fill"]["colour"]["name"] = c.Polygon.Default.Fill_Colour.NAME
        dictionary["fill"]["colour"]["mix_with"] = c.Polygon.Default.Fill_Colour.MIX_WITH
        dictionary["fill"]["colour"]["mix_percent"] = c.Polygon.Default.Fill_Colour.MIX_RATIO
        dictionary["fill"]["colour"]["strength"] = c.Polygon.Default.Fill_Colour.STRENGTH
        dictionary["fill"]["pattern"] = {}
        dictionary["fill"]["pattern"]["type"] = c.Polygon.Default.Fill_Pattern.TYPE
        dictionary["fill"]["pattern"]["distance"] = c.Polygon.Default.Fill_Pattern.DISTANCE
        dictionary["fill"]["pattern"]["size"] = c.Polygon.Default.Fill_Pattern.SIZE
        dictionary["fill"]["pattern"]["rotation"] = c.Polygon.Default.Fill_Pattern.ROTATION
        dictionary["fill"]["pattern"]["xshift"] = c.Polygon.Default.Fill_Pattern.XSHIFT
        dictionary["fill"]["pattern"]["yshift"] = c.Polygon.Default.Fill_Pattern.YSHIFT

        self.item = dictionary
