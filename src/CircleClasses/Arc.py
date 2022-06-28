from Circle import Circle
from PyQt5 import QtWidgets, QtGui, QtCore
from Item import Item
import Constant as c
import GeometryMath as gmath
from math import atan2, degrees


class Arc(Circle):
    def __init__(self, item):
        """Construct Arc."""
        Circle.__init__(self, item)
        self.item["sub_type"] = c.Circle.Definition.ARC
        self.start_angle = 0
        self.end_angle = 0

    def tikzify(self, items=None):
        return """\\makeatletter
\\tkzDefCircle[circum](%s,%s,%s)
\\tkzFindSlopeAngle(tkzPointResult,%s)\\tkzGetAngle{A@angle}
\\tkzFindSlopeAngle(tkzPointResult,%s)\\tkzGetAngle{B@angle}
\\tkzFindSlopeAngle(tkzPointResult,%s)\\tkzGetAngle{C@angle}
\\ifboolexpr{(test {\\ifdimless{\\C@angle cm}{\\A@angle cm}} and (test {\\ifdimless{\\A@angle cm}{\\B@angle cm}} or test {\\ifdimless{\\B@angle cm}{\\C@angle cm}})) or (test {\\ifdimless{\\A@angle cm}{\\C@angle cm}} and test {\\ifdimless{\\A@angle cm}{\\B@angle cm}} and test {\\ifdimless{\\B@angle cm}{\\C@angle cm}})}
{\\tkzDrawArc[%s](tkzPointResult,%s)(%s)}
{\\tkzDrawArc[%s](tkzPointResult,%s)(%s)}
\\makeatother""" % (
                   self.item["definition"]["A"],
                   self.item["definition"]["B"],
                   self.item["definition"]["C"],

                   self.item["definition"]["A"],
                   self.item["definition"]["B"],
                   self.item["definition"]["C"],

                   self.tikzify_options(),
                   self.item["definition"]["A"],
                   self.item["definition"]["C"],
                   self.tikzify_options(),
                   self.item["definition"]["C"],
                   self.item["definition"]["A"],
        )
        # return '\\tkzDefCircle[circum](%s,%s,%s)\\tkzDrawArc[towards, %s](tkzPointResult,%s)(%s)' % (
        #     self.item["definition"]["A"],
        #     self.item["definition"]["B"],
        #     self.item["definition"]["C"],
        #     self.tikzify_options(),
        #     self.item["definition"]["C"],
        #     self.item["definition"]["A"]
        # )

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

        A_angle = int(degrees(atan2(*gmath.sub(A, centre))))
        B_angle = int(degrees(atan2(*gmath.sub(B, centre))))
        C_angle = int(degrees(atan2(*gmath.sub(C, centre))))
        end_angle = A_angle-90
        start_angle = C_angle-90
        if (A_angle > C_angle and not (A_angle > B_angle > C_angle))\
        or (C_angle > A_angle and (C_angle > B_angle > A_angle)):
            end_angle, start_angle = start_angle, end_angle

        self.start_angle = start_angle
        self.end_angle = end_angle

    def recompute_canvas_with_mouse(self, scene, x, y):
        A = scene.project_data.items[scene.select_history.id_history[0]].get_canvas_coordinates()
        B = scene.project_data.items[scene.select_history.id_history[1]].get_canvas_coordinates()
        C = x, y
        centre = gmath.circumcentre(A, B, C)
        if centre is None:
            return B, 0, 0, 0
        radius = gmath.circumradius(A, centre)
        A_angle = int(degrees(atan2(*gmath.sub(A, centre))))
        B_angle = int(degrees(atan2(*gmath.sub(B, centre))))
        C_angle = int(degrees(atan2(*gmath.sub(C, centre))))
        end_angle = A_angle-90
        start_angle = C_angle-90
        if (A_angle > C_angle and not (A_angle > B_angle > C_angle))\
        or (C_angle > A_angle and (C_angle > B_angle > A_angle)):
            end_angle, start_angle = start_angle, end_angle
        return centre, radius, start_angle, end_angle

    def __str__(self): # TODO finish str
        return "Arc circle (%s) through %s" % (self.item["id"], self.item["definition"]["A"]+self.item["definition"]["B"]+self.item["definition"]["C"])

    def definition_builder(self, data, items=None):
        return dict(zip(["A", "B", "C"], data))

    @staticmethod
    def draw_on_canvas_static_arc_version(centre, radius, start_angle, end_angle, scene, colour=QtCore.Qt.darkMagenta):
        thickness = 4
        graphics_arc = QtWidgets.QGraphicsEllipseItem(*gmath.sub(centre, [radius, radius]), 2*radius, 2*radius)
        graphics_arc.setStartAngle(start_angle*16)
        graphics_arc.setSpanAngle(((end_angle - start_angle) % 360)*16)
        pen = QtGui.QPen()
        pen.setWidth(thickness)
        pen.setColor(colour)
        graphics_arc.setPen(pen)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.NoBrush)
        graphics_arc.setBrush(brush)
        scene.addItem(graphics_arc)

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
