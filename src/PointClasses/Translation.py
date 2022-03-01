from Point import Point
from Item import Item
import Constant as c
from GeometryMath import translation


class Translation(Point):
    def __init__(self, item):
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.TRANSLATION

    def tikzify(self):
        return '\\tkzDefPointWith[colinear=at %s](%s,%s)\\tkzGetPoint{%s}\n' % (
            self.item["definition"]["P"],
            self.item["definition"]["A"],
            self.item["definition"]["B"],
            self.get_id())

    def recompute_canvas(self, items, window, width, height):
        A = items[self.depends_on()[0]].get_canvas_coordinates()
        B = items[self.depends_on()[1]].get_canvas_coordinates()
        P = items[self.depends_on()[2]].get_canvas_coordinates()
        self.set_canvas_coordinates(*translation(A, B, P))

    def __str__(self):
        return "Translate (%s) from point %s with vector %s"\
            % (self.item["id"], self.item["definition"]["P"], self.item["definition"]["A"]+self.item["definition"]["B"])

    def definition_builder(self, data, items):
        return dict(zip(["A", "B", "P"], data))

    @staticmethod
    def static_patterns():
        return ["ppp"]

    def patterns(self):
        return ["ppp"]
