from Circle import Circle
from Item import Item
import Constant as c
import GeometryMath as gmath


class CircumCircle(Circle):
    def __init__(self, item):
        Circle.__init__(self, item)
        self.item["sub_type"] = c.Circle.Definition.CIRCUM

    def tikzify(self):
        return '\\tkzDefCircle[circum](%s,%s,%s)\\tkzDrawCircle(tkzPointResult,%s)'\
        % (self.item["definition"]["A"], self.item["definition"]["B"], self.item["definition"]["C"], self.item["definition"]["C"])

    def recompute_canvas(self, items, window, width, height):
        A = items[self.depends_on()[0]].get_canvas_coordinates()
        B = items[self.depends_on()[1]].get_canvas_coordinates()
        C = items[self.depends_on()[2]].get_canvas_coordinates()
        centre = gmath.circumcentre(A, B, C)
        radius = gmath.circumradius(A, centre)
        self.set_canvas_centre_xy(*centre)
        self.set_canvas_radius(radius)

    def __str__(self):
        return "Circumscribed circle (%s) of %s" % (self.item["id"], self.item["definition"]["A"]+self.item["definition"]["B"]+self.item["definition"]["C"])

    def definition_builder(self, data, items=None):
        return dict(zip(["A", "B", "C"], data))

    @staticmethod
    def static_patterns():
        return ["ppp"]

    def patterns(self):
        return ["ppp"]
