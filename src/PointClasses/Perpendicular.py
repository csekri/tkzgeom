from Point import Point
import Constant as c
import GeometryMath as gmath
from math import cos, sin, radians


class Perpendicular(Point):
    def __init__(self, item):
        """Construct a perpendicular point."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.PERPENDICULAR

    def tikzify(self, items=None):
        return "\\tkzDefLine[orthogonal=through %s](%s,%s)\\tkzGetPoint{%s}" % (self.item["definition"]["P"], self.item["definition"]["A"], self.item["definition"]["B"], self.item["id"])

    def recompute_canvas(self, items, window, width, height):
        A = items[self.depends_on()[0]].get_canvas_coordinates()
        B = items[self.depends_on()[1]].get_canvas_coordinates()
        P = items[self.depends_on()[2]].get_canvas_coordinates()
        angle = 90.0
        cosa = cos(radians(angle))
        sina = sin(radians(angle))
        diff = gmath.sub(A, B)
        C = diff[0] * cosa - diff[1] * sina, diff[0] * sina + diff[1] * cosa
        self.set_canvas_coordinates(*gmath.add(P, C))

    def __str__(self):  # TODO finish str
        return "Perpendicular (%s) of %s and %s" % (self.item["id"], self.item["definition"]["A"], self.item["definition"]["B"])

    def definition_builder(self, data, items=None):
        return dict(zip(["A", "B", "P"], data))

    def parse_into_definition(self, arguments, items):
        # arguments length condition
        if len(arguments) != 3:
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
        # condition for cross reference
        for id in arguments:
            deep_depends = items[id].deep_depends_on(items)
            if self.get_id() in deep_depends:
                return None
        return self.definition_builder(arguments)

    @staticmethod
    def static_patterns():
        return ["ppp"]

    def patterns(self):
        return ["ppp"]
