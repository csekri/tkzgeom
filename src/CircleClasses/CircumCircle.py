from Circle import Circle
from Item import Item
import Constant as c
import GeometryMath as gmath


class CircumCircle(Circle):
    def __init__(self, item):
        """Construct CircumCircle."""
        Circle.__init__(self, item)
        self.item["sub_type"] = c.Circle.Definition.CIRCUM

    def tikzify(self):
        return '\\tkzDefCircle[circum](%s,%s,%s)\\tkzDrawCircle[%s](tkzPointResult,%s)'\
        % (self.item["definition"]["A"], self.item["definition"]["B"], self.item["definition"]["C"], self.tikzify_options(), self.item["definition"]["C"])

    def recompute_canvas(self, items, window, width, height):
        A = items[self.depends_on()[0]].get_canvas_coordinates()
        B = items[self.depends_on()[1]].get_canvas_coordinates()
        C = items[self.depends_on()[2]].get_canvas_coordinates()
        centre = gmath.circumcentre(A, B, C)
        if centre is None:
            self.set_canvas_centre_xy(*B)
            self.set_canvas_radius(0)
        radius = gmath.circumradius(A, centre)
        self.set_canvas_centre_xy(*centre)
        self.set_canvas_radius(radius)

    def recompute_canvas_with_mouse(self, scene, x, y):
        A = scene.project_data.items[scene.select_history.id_history[0]].get_canvas_coordinates()
        B = scene.project_data.items[scene.select_history.id_history[1]].get_canvas_coordinates()
        C = x, y
        centre = gmath.circumcentre(A, B, C)
        if centre is None:
            return B, 0
        radius = gmath.circumradius(A, centre)
        return centre, radius

    def __str__(self):
        return "Circumscribed circle (%s) of %s" % (self.item["id"], self.item["definition"]["A"]+self.item["definition"]["B"]+self.item["definition"]["C"])

    def definition_builder(self, data, items=None):
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
