from Point import Point
import Constant as c
from GeometryMath import bisector_point


class Bisector(Point):
    def __init__(self, item):
        """Construct Bisector."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.BISECTOR

    def tikzify(self, items=None):
        return '\\tkzDefLine[bisector](%s,%s,%s)\\tkzGetPoint{%s}' % (self.item["definition"]["A"],
                                                                      self.item["definition"]["B"],
                                                                      self.item["definition"]["C"],
                                                                      self.get_id())

    def recompute_canvas(self, items, window, width, height):
        A = items[self.depends_on()[0]].get_canvas_coordinates()
        B = items[self.depends_on()[1]].get_canvas_coordinates()
        C = items[self.depends_on()[2]].get_canvas_coordinates()
        self.set_canvas_coordinates(*bisector_point(A, B, C))

    def __str__(self):
        return "Bisector point (%s) of angle %s"\
            % (self.item["id"], self.item["definition"]["A"]+self.item["definition"]["B"]+self.item["definition"]["C"])

    def definition_builder(self, data, items=None):
        if len(data) == 3:
            return dict(zip(["A", "B", "C"], data))

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
