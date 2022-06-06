from PyQt5 import QtCore, QtWidgets, QtGui

from Item import Item
import Constant as c
from Tikzifyables.Labelable import Labelable
from Tikzifyables.DashPatternable import DashPatternable
from Tikzifyables.Colourable.LineColourable import LineColourable
from Tikzifyables.Colourable.FillColourable import FillColourable


class Point(Item, Labelable, DashPatternable, LineColourable, FillColourable):
    def __init__(self, item):
        """Construct Point."""
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "", "")
        Labelable.__init__(self, self.item)
        DashPatternable.__init__(self, self.item)
        LineColourable.__init__(self, self.item)
        FillColourable.__init__(self, self.item)
        self.__canvas_x = 0
        self.__canvas_y = 0

    def get_canvas_coordinates(self):
        return self.__canvas_x, self.__canvas_y

    def set_canvas_coordinates(self, x, y):
        self.__canvas_x = x
        self.__canvas_y = y

    def __tikzify_marker(self):
        extra = ''
        if self.item["marker"]["shape"] == 'regular polygon':
            extra = 'regular polygon sides=' + str(self.item["marker"]["shape_number"])
        elif self.item["marker"]["shape"] == 'star':
            extra = f'star points={self.item["marker"]["shape_number"]}, star point ratio={self.item["marker"]["ratio"]}'

        options = [
            self.item["marker"]["shape"],
            'minimum size=' + str(self.item["marker"]["size"]),
            'inner sep=' + str(self.item["marker"]["inner_sep"]),
            '' if self.item["marker"]["shape"] == 'circle' or self.item["marker"]["rounded_corners"] == c.Point.Default.Marker.ROUNDED_CORNERS else f'rounded corners={self.item["marker"]["rounded_corners"]}pt',
            '' if self.item["marker"]["text_width"] == c.Point.Default.Marker.TEXT_WIDTH else 'text width=' + str(self.item["marker"]["text_width"]),
        ]
        if extra:
            options.append(extra)
        options = filter(bool, options)

        return ', '.join(options)

    def tikzify_node(self):
        options = [
            f'draw={c.Point.Default.Line_Colour.NAME}' if not bool(self.tikzify_line_colour()) else f'draw={self.tikzify_line_colour()}',
            f'fill={c.Point.Default.FillColor.NAME}' if not bool(self.tikzify_fill_colour()) else f'fill={self.tikzify_fill_colour()}',
            '' if self.item["line"]["line_width"] == c.Point.Default.LINE_WIDTH else f'line width={self.item["line"]["line_width"]}',
            self.__tikzify_marker(),
            self.tikzify_dash()
        ]
        options = filter(bool, options)
        return '\\node[%s] (%s) at (%s) {%s};' % (', '.join(options), self.get_id(), self.get_id(), self.item["marker"]["text"])

    def tikzify(self, items=None):
        raise NotImplementedError

    def draw_on_canvas(self, items, scene, colour=QtCore.Qt.darkMagenta):
        radius = 6
        graphics_point = QtWidgets.QGraphicsEllipseItem(self.__canvas_x-radius,self.__canvas_y-radius, 2*radius, 2*radius)
        graphics_point.setBrush(QtGui.QBrush(colour))
        scene.addItem(graphics_point)
        if scene.show_canvas_labels:
            text = QtWidgets.QGraphicsTextItem(self.item["id"])
            text.setPos(self.__canvas_x,self.__canvas_y)
            text.setDefaultTextColor (colour)
            font = text.font()
            font.setPointSize(12)
            font.setWeight(600)
            text.setFont(font)
            # text.setTextWidth(400)
            scene.addItem(text)

    def distance_sqr(self, x, y, items):
        return (self.__canvas_x-x) ** 2 + (self.__canvas_y-y) ** 2

    def next_id_func(self, definition, iter_counter):
        return chr(ord('A') + iter_counter % 26) + (iter_counter // 26) * '\''

    def dictionary_builder(self, definition, id_, sub_type=None):
        dictionary = {}
        dictionary["id"] = id_
        dictionary["type"] = 'point'
        dictionary["sub_type"] = sub_type
        dictionary["show"] = True
        dictionary["definition"] = definition
        dictionary["marker"] = {}
        dictionary["marker"]["size"] = c.Point.Default.Marker.SIZE
        dictionary["marker"]["shape"] = c.Point.Default.Marker.SHAPE
        dictionary["marker"]["shape_number"] = c.Point.Default.Marker.SHAPE_NUMBER
        dictionary["marker"]["ratio"] = c.Point.Default.Marker.RATIO
        dictionary["marker"]["inner_sep"] = c.Point.Default.Marker.INNER_SEP
        dictionary["marker"]["rounded_corners"] = c.Point.Default.Marker.ROUNDED_CORNERS
        dictionary["marker"]["text"] = c.Point.Default.Marker.TEXT
        dictionary["marker"]["text_width"] = c.Point.Default.Marker.TEXT_WIDTH
        dictionary["line"] = {}
        dictionary["line"]["line_width"] = c.Point.Default.LINE_WIDTH
        dictionary["line"]["colour"] = {}
        dictionary["line"]["colour"]["name"] = c.Point.Default.Line_Colour.NAME
        dictionary["line"]["colour"]["mix_with"] = c.Point.Default.Line_Colour.MIX_WITH
        dictionary["line"]["colour"]["mix_percent"] = c.Point.Default.Line_Colour.MIX_RATIO
        dictionary["line"]["colour"]["strength"] = c.Point.Default.Line_Colour.STRENGTH
        dictionary["line"]["dash"] = {}
        dictionary["line"]["dash"]["stroke"] = c.Point.Default.LINE_DASH_STROKE
        dictionary["line"]["dash"]["custom_pattern"] = c.Point.Default.LINE_DASH_CUSTOM
        dictionary["fill"] = {}
        dictionary["fill"]["colour"] = {}
        dictionary["fill"]["colour"]["name"] = c.Point.Default.Fill_Colour.NAME
        dictionary["fill"]["colour"]["mix_with"] = c.Point.Default.Fill_Colour.MIX_WITH
        dictionary["fill"]["colour"]["mix_percent"] = c.Point.Default.Fill_Colour.MIX_RATIO
        dictionary["fill"]["colour"]["strength"] = c.Point.Default.Fill_Colour.STRENGTH
        dictionary["label"] = {}
        dictionary["label"]["show"] = c.Point.Default.Label.SHOW
        dictionary["label"]["text"] = f'${id_}$'
        dictionary["label"]["text"] = c.Point.Default.Label.TEXT
        dictionary["label"]["anchor"] = c.Point.Default.Label.ANCHOR
        dictionary["label"]["offset"] = c.Point.Default.Label.OFFSET

        self.item = dictionary




#
