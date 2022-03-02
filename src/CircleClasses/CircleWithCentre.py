from Circle import Circle
from Item import Item
import Constant as c
from GeometryMath import sub, norm


class CircleWithCentre(Circle):
    def __init__(self, item):
        Circle.__init__(self, item)
        self.item["sub_type"] = c.Circle.Definition.WITH_CENTRE

    def tikzify(self):
        return '\\tkzDrawCircle(%s,%s)' % (self.item["definition"]["O"], self.item["definition"]["P"])
        # return "\\tkzDefMidPoint(%s,%s)\\tkzGetPoint{%s}" % (self.item["definition"]["A"], self.item["definition"]["B"], self.item["id"])

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

    @staticmethod
    def static_patterns():
        return ["pp"]

    def patterns(self):
        return ["pp"]
