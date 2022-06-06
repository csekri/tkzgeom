from Point import Point
import Constant as c


class FreePoint(Point):
    def __init__(self, item):
        """Construct FreePoint."""
        Point.__init__(self, item)
        self.item["sub_type"] = c.Point.Definition.FREE

    @staticmethod
    def phi(window, x, y, width, height):
        """Transform tikz coordinates to canvas coordinates."""
        return (x - window.left) * height / (window.scale * 10.0),\
            (window.top - y) * height / (window.scale * 10.0)

    @staticmethod
    def phi_inverse(window, x, y, width, height):
        """Transform canvas coordinates to tikz coordinates."""
        return window.left + x / height * window.scale*10.0,\
            window.top - y / height * window.scale*10.0

    def tikzify(self, items=None):
        return "\\tkzDefPoint(%.6f, %.6f){%s}" % (self.item["definition"]["x"],
                                                  self.item["definition"]["y"],
                                                  self.item["id"])

    def depends_on(self):
        return []

    def recompute_canvas(self, items, window, width, height):
        self.set_canvas_coordinates(*FreePoint.phi(window,
                                                   self.item["definition"]["x"],
                                                   self.item["definition"]["y"],
                                                   width,
                                                   height))

    def definition_builder(self, data, items=None):
        return { "x": data[0], "y": data[1] }

    def parse_into_definition(self, arguments, items):
        if len(arguments) != 2:
            return None
        try:
            arg_conv = list(map(float, arguments))
        except ValueError:
            return None
        return self.definition_builder(arg_conv)

    def __str__(self):
        return "FreePoint (%s) at (%s, %s)" % (self.item["id"],
                                               self.item["definition"]["x"],
                                               self.item["definition"]["y"])

    @staticmethod
    def static_patterns():
        return []

    def patterns(self):
        return []
