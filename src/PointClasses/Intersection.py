from Point import Point
import Constant as c
from GeometryMath import ll_intersection


class Intersection(Point):
    def __init__(self, item):
        """Construct Intersection."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.INTERSECTION

    def tikzify(self):
        return "\\tkzInterLL(%s,%s)(%s,%s)\\tkzGetPoint{%s}" % (self.depends_on()[0],
                                                                self.depends_on()[1],
                                                                self.depends_on()[2],
                                                                self.depends_on()[3],
                                                                self.get_id())

    def recompute_canvas(self, items, window, width, height):
        A = items[self.item["definition"]["A"]].get_canvas_coordinates()
        B = items[self.item["definition"]["B"]].get_canvas_coordinates()
        C = items[self.item["definition"]["C"]].get_canvas_coordinates()
        D = items[self.item["definition"]["D"]].get_canvas_coordinates()
        P = ll_intersection(A, B, C, D)
        self.set_canvas_coordinates(*P)

    def __str__(self):
        return "OnLine (%s) of %s and %s with ratio %s" % (self.get_id(), self.item["definition"]["A"], self.item["definition"]["B"], self.item["definition"]["ratio"])

    def definition_builder(self, data, items=None):
        if len(data) == 2: # ss
            A, B = items[data[0]].depends_on()
            C, D = items[data[1]].depends_on()
            return dict(zip(["A", "B", "C", "D"], [A, B, C, D]))
        if len(data) == 3: # ss
            if items[data[0]].item["type"] == 'segment':
                data = list(reversed(data))
            C, D = items[data[2]].depends_on()
            return dict(zip(["A", "B", "C", "D"], [data[0], data[1], C, D]))
        return dict(zip(["A", "B", "C", "D"], data))

    def parse_into_definition(self, arguments, items):
        # arguments length condition
        if len(arguments) != 4:
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
        return ["ss", "pppp", "spp", "pps"]

    def patterns(self):
        return ["ss", "pppp", "spp", "pps"]
