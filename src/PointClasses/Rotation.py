from Point import Point
import Constant as c
import GeometryMath as gmath
from math import cos, sin, radians


class Rotation(Point):
    def __init__(self, item):
        """Construct Rotation."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.ROTATION

    def tikzify(self):
        return "\\tkzDefPointBy[rotation=center %s angle %s](%s)\\tkzGetPoint{%s}" % (self.item["definition"]["B"], self.item["definition"]["angle"], self.item["definition"]["A"], self.get_id())

    def recompute_canvas(self, items, window, width, height):
        A = items[self.item["definition"]["A"]].get_canvas_coordinates()
        B = items[self.item["definition"]["B"]].get_canvas_coordinates()
        angle = self.item["definition"]["angle"]
        cosa = cos(radians(-angle))
        sina = sin(radians(-angle))
        diff = gmath.sub(A, B)
        C = diff[0] * cosa - diff[1] * sina, diff[0] * sina + diff[1] * cosa
        self.set_canvas_coordinates(*gmath.add(B, C))

    def depends_on(self):
        return [self.item["definition"]["A"], self.item["definition"]["B"]]

    def __str__(self):
        return "Rotation (%s) of %s and %s with angle %s" % (self.get_id(), self.item["definition"]["A"], self.item["definition"]["B"], self.item["definition"]["angle"])

    def definition_builder(self, data, items=None):
        return dict(zip(["A", "B", "angle"], data + [45.0]))

    def parse_into_definition(self, arguments, items):
        # arguments length condition
        if len(arguments) != 3:
            return None
        # first two arguments are members of the regular expression for argument name
        if not all(map(lambda x: self.name_pattern(x), arguments[:2])):
            return None
        # third argument is a float
        try:
            float(arguments[2])
        except ValueError:
            return None
        # all arguments are items that already exist
        if not all(map(lambda x: x in items, arguments[:2])):
            return None
        # the type of all arguments is of a certain type
        if not all(map(lambda x: items[x].item["type"] == 'point', arguments[:2])):
            return None
        # self-reference condition (self-reference is not permitted)
        if self.get_id() in arguments[:2]:
            return None
        # condition for cross reference
        for id in arguments[:2]:
            deep_depends = items[id].deep_depends_on(items)
            if self.get_id() in deep_depends:
                return None

        return self.definition_builder(arguments[:2] + [float(arguments[2])])

    @staticmethod
    def static_patterns():
        return ["s", "pp"]

    def patterns(self):
        return ["s", "pp"]
