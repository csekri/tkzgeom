from Point import Point
import Constant as c
from GeometryMath import ortho_proj


class Projection(Point):
    def __init__(self, item):
        """Construct Projection."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.PROJECTION

    def tikzify(self):
        return '\\tkzDefPointBy[projection=onto %s--%s](%s)\\tkzGetPoint{%s}\n' % (
            self.item["definition"]["A"],
            self.item["definition"]["B"],
            self.item["definition"]["P"],
            self.get_id())

    def recompute_canvas(self, items, window, width, height):
        A = items[self.depends_on()[0]].get_canvas_coordinates()
        B = items[self.depends_on()[1]].get_canvas_coordinates()
        P = items[self.depends_on()[2]].get_canvas_coordinates()
        self.set_canvas_coordinates(*ortho_proj(A, B, P))

    def __str__(self):
        return "Orthogonal projection (%s) of point %s onto line %s"\
            % (self.item["id"], self.item["definition"]["P"], self.item["definition"]["A"]+self.item["definition"]["B"])

    def definition_builder(self, data, items=None):
        if len(data) == 3:
            return dict(zip(["A", "B", "P"], data))
        if items[data[0]].item["type"] == 'point':
            data = list(reversed(data))
        A, B = items[data[0]].depends_on()
        return dict(zip(["A", "B", "P"], [A, B, data[1]]))

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
        return ["ppp", "sp", "ps"]

    def patterns(self):
        return ["ppp", "sp", "ps"]
