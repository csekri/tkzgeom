from Point import Point
import Constant as c


class OnLine(Point):
    def __init__(self, item):
        """Construct OnLine."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.ON_LINE

    def tikzify(self, items=None):
        return "\\tkzDefPointBy[homothety=center %s ratio %s](%s) \\tkzGetPoint{%s}" % (self.item["definition"]["A"], self.item["definition"]["ratio"], self.item["definition"]["B"], self.get_id())

    def recompute_canvas(self, items, window, width, height):
        A = items[self.item["definition"]["A"]].get_canvas_coordinates()
        B = items[self.item["definition"]["B"]].get_canvas_coordinates()
        r = self.item["definition"]["ratio"]
        x, y = A[0]+r*(B[0]-A[0]), A[1]+r*(B[1]-A[1])
        self.set_canvas_coordinates(x, y)

    def depends_on(self):
        return [self.item["definition"]["A"], self.item["definition"]["B"]]

    def __str__(self):
        return "OnLine (%s) of %s and %s with ratio %s" % (self.get_id(), self.item["definition"]["A"], self.item["definition"]["B"], self.item["definition"]["ratio"])

    def definition_builder(self, data, items=None):
        return dict(zip(["A", "B", "ratio"], data))

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
        return ["s"]

    def patterns(self):
        return ["s"]
