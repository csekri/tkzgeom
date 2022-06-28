from Point import Point
import Constant as c
from GeometryMath import circumcentre, incentre


class CircleCentre(Point):
    def __init__(self, item):
        """Construct CircleCentre."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.CIRCLE_CENTRE

    def depends_on(self):
        return self.item["definition"]

    def tikzify(self, items=None):
        circle_id = self.item["definition"][0]
        circle_type = items[circle_id].item["sub_type"]
        circle_definition = items[circle_id].item["definition"]
        if circle_type == c.Circle.Definition.CIRCUM or circle_type == c.Circle.Definition.ARC:
            return '\\tkzDefCircle[circum](%s,%s,%s)\\tkzGetPoint{%s}\n' \
                   % (circle_definition["A"],
                      circle_definition["B"],
                      circle_definition["C"],
                      self.get_id())
        if circle_type == c.Circle.Definition.WITH_CENTRE:
            return '\\tkzDefPointWith[colinear=at %s](%s,%s)\\tkzGetPoint{%s}\n' % (
                circle_definition["P"],
                circle_definition["O"],
                circle_definition["O"],
                self.get_id())
        if circle_type == c.Circle.Definition.INSCRIBED:
            return '\\tkzDefCircle[in](%s,%s,%s)\\tkzGetPoint{%s}\n' \
                   % (circle_definition["A"],
                      circle_definition["B"],
                      circle_definition["C"],
                      self.get_id())
        return ""

    def recompute_canvas(self, items, window, width, height):
        circle_id = self.item["definition"][0]
        circle_type = items[circle_id].item["sub_type"]
        circle_definition = items[circle_id].item["definition"]
        if circle_type == c.Circle.Definition.CIRCUM or circle_type == c.Circle.Definition.ARC:
            A = items[circle_definition["A"]].get_canvas_coordinates()
            B = items[circle_definition["B"]].get_canvas_coordinates()
            C = items[circle_definition["C"]].get_canvas_coordinates()
            self.set_canvas_coordinates(*circumcentre(A, B, C))
        if circle_type == c.Circle.Definition.INSCRIBED:
            A = items[circle_definition["A"]].get_canvas_coordinates()
            B = items[circle_definition["B"]].get_canvas_coordinates()
            C = items[circle_definition["C"]].get_canvas_coordinates()
            self.set_canvas_coordinates(*incentre(A, B, C))
        if circle_type == c.Circle.Definition.WITH_CENTRE:
            O = items[circle_definition["O"]].get_canvas_coordinates()
            self.set_canvas_coordinates(*O)

    def __str__(self):
        return "todo later"

    def definition_builder(self, data, items=None):
        return data

    def parse_into_definition(self, arguments, items):
        # arguments length condition
        if len(arguments) != 1:
            return None
        # all arguments are members of the regular expression for argument name
        if not all(map(lambda x: self.name_pattern(x), arguments)):
            return None
        # all arguments are items that already exist
        if not all(map(lambda x: x in items, arguments)):
            return None
        # the type of all arguments is of a certain type
        if not all(map(lambda x: items[x].item["type"] == 'circle', arguments)):
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
        return ["c"]

    def patterns(self):
        return ["c"]
