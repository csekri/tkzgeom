from Circle import Circle
from Item import Item
import Constant as c
from GeometryMath import sub, norm


class CircleWithCentre(Circle):
    def __init__(self, item):
        Circle.__init__(self, item)
        self.item["sub_type"] = c.Circle.Definition.WITH_CENTRE

    def tikzify(self):
        return '\\tkzDrawCircle[%s](%s,%s)' % (self.tikzify_options(), self.item["definition"]["O"], self.item["definition"]["P"])

    def recompute_canvas(self, items, window, width, height):
        O = items[self.depends_on()[0]].get_canvas_coordinates()
        P = items[self.depends_on()[1]].get_canvas_coordinates()
        self.set_canvas_centre_xy(*O)
        self.set_canvas_radius(norm(sub(O, P)))

    def recompute_canvas_with_mouse(self, scene, x, y):
        O = scene.project_data.items[scene.select_history.id_history[0]].get_canvas_coordinates()
        P = x, y
        return O, norm(sub(O, P))

    def __str__(self):
        return "Circle (%s) with centre %s and perimetric point %s" % (self.item["id"], self.item["definition"]["O"], self.item["definition"]["P"])

    def definition_builder(self, data, items=None):
        return dict(zip(["O", "P"], data))

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
        return ["pp"]

    def patterns(self):
        return ["pp"]
