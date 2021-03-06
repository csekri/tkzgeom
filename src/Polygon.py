from PyQt5 import QtCore, QtWidgets, QtGui
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon

from Item import Item
from Tikzifyables.DashPatternable import DashPatternable
from Tikzifyables.Colourable.LineColourable import LineColourable
from Tikzifyables.Fillable import Fillable
from Tikzifyables.Decorationable import Decorationable
from Tikzifyables.CurveStrategyable import CurveStrategyable
import Constant as c


class Polygon(Item, DashPatternable, LineColourable, Fillable, Decorationable, CurveStrategyable):
    def __init__(self, item):
        """Construct Polygon."""
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "")
        DashPatternable.__init__(self, self.item)
        LineColourable.__init__(self, self.item)
        Fillable.__init__(self, self.item)
        Decorationable.__init__(self, self.item)
        CurveStrategyable.__init__(self, self.item)

    def tikzify(self, items=None):
        strategy_options, strategy_coordinates = self.tikzify_strategy(False)
        options = [
            self.tikzify_dash(),
            'draw=' + self.tikzify_line_colour(),
            '' if self.item["line"]["line_width"] == c.Point.Default.LINE_WIDTH else f'line width={self.item["line"]["line_width"]}',
            self.tikzify_fill_pattern(),
            self.tikzify_decoration(),
            strategy_options
        ]
        options = filter(bool, options)
        return "\\draw[%s] %s;" % (', '.join(options), strategy_coordinates)

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
        # arguments length condition
        if len(arguments) <= 2:
            return None
        # all arguments are members of the regular expression for argument name
        if not all(map(lambda x: self.name_pattern(x), arguments)):
            return None
        # all arguments are items that already exist
        if not all(map(lambda x: x in items, arguments)):
            return None
        # the type of all arguments is of a certain type
        if not all(map(lambda x: items[x].item["type"] == 'point', arguments)):
            return None
        # self-reference condition (self-reference is not permitted)
        if self.get_id() in arguments:
            return None
        return self.definition_builder(arguments+['mock item'])

    def dictionary_builder(self, definition, id_, sub_type=None):
        dictionary = {}
        dictionary["id"] = id_
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
        dictionary["line"]["strategy"] = {}
        dictionary["line"]["strategy"]["type"] = c.Polygon.Default.Strategy.TYPE
        dictionary["line"]["strategy"]["rounded_corners"] = c.Polygon.Default.Strategy.ROUNDED_CORNERS
        dictionary["line"]["strategy"]["bend_angle"] = c.Polygon.Default.Strategy.BEND_ANGLE
        dictionary["line"]["strategy"]["in_angle"] = c.Polygon.Default.Strategy.IN_ANGLE
        dictionary["line"]["strategy"]["out_angle"] = c.Polygon.Default.Strategy.OUT_ANGLE
        dictionary["line"]["strategy"]["smooth_tension"] = c.Polygon.Default.Strategy.SMOOTH_TENSION
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
