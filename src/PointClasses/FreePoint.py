from Point import Point
from Item import Item
import Constant as c

class FreePoint(Point):
    def __init__(self, item):
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.FREE

    @staticmethod
    def phi(window, x, y, width, height):
        window_initial_height = height
        return (x - window.left) * window_initial_height / (window.scale * 10.0),\
            (window.top - y) * window_initial_height / (window.scale * 10.0)


    @staticmethod
    def phi_inverse(window, x, y, width, height):
        return window.left + x / width * window.scale*10.0,\
            window.top - y / height * window.scale*10.0

    def tikzify(self):
        return "\\tkzDefPoint(%s, %s){%s}" % (self.item["definition"]["x"], self.item["definition"]["y"], self.item["id"])

    def depends_on(self):
        return []

    def recompute_canvas(self, items, window, width, height):
        self.set_canvas_coordinates(*FreePoint.phi(window, self.item["definition"]["x"], self.item["definition"]["y"], width, height))

    def definition_builder(self, data, items):
        return { "x": data[0], "y": data[1] }


    def __str__(self):
        return "FreePoint (%s) at (%s, %s)" % (self.item["id"], self.item["definition"]["x"], self.item["definition"]["y"])

    @staticmethod
    def static_patterns():
        return []

    def patterns(self):
        return []
