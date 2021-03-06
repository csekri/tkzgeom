from PyQt5 import QtCore, QtWidgets, QtGui

from Item import Item
from Tikzifyables.Arrowable import Arrowable
from Tikzifyables.DashPatternable import DashPatternable
from Tikzifyables.Doubleable import Doubleable
from Tikzifyables.Colourable.LineColourable import LineColourable
import Constant as c
from GeometryMath import point_segment_dist_sqr


class Segment(Item, Arrowable, DashPatternable, Doubleable, LineColourable):
    def __init__(self, item):
        """Construct Segment."""
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "")
        Arrowable.__init__(self, self.item)
        DashPatternable.__init__(self, self.item)
        Doubleable.__init__(self, self.item)
        LineColourable.__init__(self, self.item)

    def tikzify(self, items=None):
        options = [
            '' if self.item["line"]["line_width"] == c.Segment.Default.LINE_WIDTH else f'line width={self.item["line"]["line_width"]}',
            self.tikzify_arrows(),
            self.tikzify_dash(),
            'draw=' + self.tikzify_line_colour(),
            self.tikzify_double()
        ]
        options = filter(bool, options)
        origin = self.item["definition"]["A"]\
            if self.item["line"]["o_extension"] == 0.0\
            else f'$({self.item["definition"]["A"]})!{self.item["line"]["o_extension"]}!({self.item["definition"]["B"]})$'
        if self.item["line"]["o_connect_to"] == c.LineConnectTo.NODE_CENTRE:
            origin = self.item["definition"]["A"] + '.center'
        destination = self.item["definition"]["B"]\
            if self.item["line"]["d_extension"] == 1.0\
            else f'$({self.item["definition"]["A"]})!{self.item["line"]["d_extension"]}!({self.item["definition"]["B"]})$'
        if self.item["line"]["d_connect_to"] == c.LineConnectTo.NODE_CENTRE:
            destination = self.item["definition"]["B"] + '.center'
        return '\\draw[%s](%s) -- (%s);' % ( ', '.join(options) , origin, destination)

    def tikzify_segment_marker(self):
        if self.item["marker"]["symbol"] == c.SegmentMarkerType.NONE:
            return ''
        options = [
            f'mark={self.item["marker"]["symbol"]}',
            '' if self.item["marker"]["size"] == 4.0 else f'size={self.item["marker"]["size"]}',
            '' if self.item["marker"]["position"] == 0.5 else f'pos={self.item["marker"]["position"]}'
        ]
        options = filter(bool, options)
        tkzMarkSegment = '\\tkzMarkSegment[%s](%s,%s)' % (', '.join(options), self.item["definition"]["A"], self.item["definition"]["B"])
        if self.item["marker"]["width"] != 0.4:
            return '\\begin{scope}[%s]\n%s\n\\end{scope}' % (f'line width={self.item["marker"]["width"]}', tkzMarkSegment)
        return tkzMarkSegment

    def __str__(self):
        return "Segment from (%s) to (%s)" % (self.item["definition"]["A"], self.item["definition"]["B"])

    def draw_on_canvas(self, items, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        graphics_line = QtWidgets.QGraphicsLineItem(
            *items[self.item["definition"]["A"]].get_canvas_coordinates(),
            *items[self.item["definition"]["B"]].get_canvas_coordinates()
        )
        graphics_line.setPen(QtGui.QPen(QtGui.QBrush(colour), thickness))
        scene.addItem(graphics_line)

    @staticmethod
    def draw_on_canvas_static(x1, y1, x2, y2, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        graphics_line = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
        graphics_line.setPen(QtGui.QPen(QtGui.QBrush(colour), thickness))
        scene.addItem(graphics_line)

    def distance_sqr(self, x, y, items):
        A = items[self.item["definition"]["A"]].get_canvas_coordinates()
        B = items[self.item["definition"]["B"]].get_canvas_coordinates()
        P = x, y
        return point_segment_dist_sqr(A, B, P)

    @staticmethod
    def static_patterns():
        return ["pp"]

    def patterns(self):
        return ["pp"]

    def next_id_func(self, definition, iter_counter):
        current = definition["A"] + '_' + definition["B"]
        if iter_counter != 0:
            current += '_' + iter_counter * '\''
        return current

    def definition_builder(self, data, items=None):
        return dict(zip(["A", "B"], data))

    def parse_into_definition(self, arguments, items):
        if len(arguments) != 2:
            return None
        condition1 = not all(map(lambda x: self.name_pattern(x), arguments))
        if condition1:
            return None
        condition2 = not all(map(lambda x: x in items, arguments))
        if condition2:
            return None
        condition3 = not all(map(lambda x: items[x].item["type"] == 'point', arguments))
        if condition3:
            return None
        return self.definition_builder(arguments)

    def dictionary_builder(self, definition, id_, sub_type=None):
        dictionary = {}
        dictionary["id"] = id_
        dictionary["type"] = 'segment'
        dictionary["sub_type"] = None
        dictionary["show"] = True
        dictionary["definition"] = definition
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
        dictionary["marker"] = {}
        dictionary["marker"]["symbol"] = c.Segment.Default.Segment_Marker.SYMBOL
        dictionary["marker"]["width"] = c.Segment.Default.Segment_Marker.WIDTH
        dictionary["marker"]["size"] = c.Segment.Default.Segment_Marker.SIZE
        dictionary["marker"]["position"] = c.Segment.Default.Segment_Marker.POSITION

        self.item = dictionary
