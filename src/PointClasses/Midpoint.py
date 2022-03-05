from Point import Point
from Item import Item
import Constant as c


class Midpoint(Point):
    def __init__(self, item):
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.SEGMENT_MIDPOINT


    def tikzify(self):
        return "\\tkzDefMidPoint(%s,%s)\\tkzGetPoint{%s}" % (self.item["definition"]["A"], self.item["definition"]["B"], self.item["id"])

    def recompute_canvas(self, items, window, width, height):
        x1, y1 = items[self.depends_on()[0]].get_canvas_coordinates()
        x2, y2 = items[self.depends_on()[1]].get_canvas_coordinates()
        self.set_canvas_coordinates(x1/2 + x2/2, y1/2 + y2/2)

    def __str__(self):
        return "Midpoint (%s) of %s and %s" % (self.item["id"], self.item["definition"]["A"], self.item["definition"]["B"])

    def definition_builder(self, data, items=None):
        if len(data) == 2:
            return dict(zip(["A", "B"], data))
        return dict(zip(["A", "B"], items[data[0]].item["definition"].values()))

    def parse_into_definition(self, arguments, items):
        # arguments length condition
        if len(arguments) != 2:
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
        return ["pp", "s"]

    def patterns(self):
        return ["pp", "s"]
