"""
contains drawing routines for primitives
"""


from PyQt5 import QtCore, QtWidgets, QtGui, uic
import son_of_j as soj
import eucl_math as em
import numpy as np
from cv2 import imwrite


CANVAS_POINT_RADIUS = 7
CANVAS_LINE_THICKNESS = 3
CANVAS_CIRCLE_THICKNESS = 3


# clears all objects on the canvas and adds an the last compiled pdf image
def clear_canvas(scene):
    scene.clear()
    pixmap = QtGui.QPixmap("tmp/temp-1.jpg")
    if not scene.show_pdf:
        pixmap.fill()
    tkz_jpg = QtWidgets.QGraphicsPixmapItem(pixmap)
    scene.addItem(tkz_jpg)
    if scene.aspect_ratio_indicator:
        draw_aspect_ratio(scene, QtCore.Qt.black)


def draw_aspect_ratio(scene, colour):
    aspect_ratio = eval(scene.aspect_ratio)
    pixels = scene.settings["pixels"]
    if aspect_ratio < 1:
        x_from, y_from, x_to, y_to = (pixels*(1-aspect_ratio)/2,0,pixels*(1-aspect_ratio)/2,pixels)
        graphics_line_1 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
        x_from, y_from, x_to, y_to = (pixels - pixels*(1-aspect_ratio)/2,0,pixels - pixels*(1-aspect_ratio)/2,pixels)
        graphics_line_2 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
    else:
        x_from, y_from, x_to, y_to = (0,pixels*(1-1/aspect_ratio)/2,pixels,pixels*(1-1/aspect_ratio)/2)
        graphics_line_1 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
        x_from, y_from, x_to, y_to = (0,pixels - pixels*(1-1/aspect_ratio)/2,pixels,pixels - pixels*(1-1/aspect_ratio)/2)
        graphics_line_2 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
    if aspect_ratio != 1:
        graphics_line_1.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
        graphics_line_2.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
        scene.addItem(graphics_line_1)
        scene.addItem(graphics_line_2)



def empty_jpg(width, height):
    empty_image = 255 * np.ones((width, height)) # blank white bw-matrix
    imwrite('tmp/temp-1.jpg', empty_image)

def always_on_drawing_plan(scene):
    if scene.canvas_always_on:
        clear_canvas(scene)
        add_all_items_to_scene(scene, QtCore.Qt.darkCyan)
        add_selected_items_to_scene(scene, QtCore.Qt.blue)
        add_specific_item_to_scene(scene, scene.focused_point_id, QtCore.Qt.darkMagenta)

def always_off_drawing_plan(scene):
    if not scene.canvas_always_on:
        clear_canvas(scene)
        add_selected_items_to_scene(scene, QtCore.Qt.blue)
        add_specific_item_to_scene(scene, scene.focused_point_id, QtCore.Qt.darkMagenta)


# computes the centre and radius of a circle in the canvas coordinate system
def get_circle_centre_radius_on_canvas(scene, id):
    assert soj.identify_item_type(scene.eucl, id) == "c"
    assert id != 'crc_default'
    circle = soj.get_item_from_id(scene.eucl, id, "c")
    centre, radius = (0,0)

    if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
        A = scene.mapped_points[circle["points"]["A"]]
        B = scene.mapped_points[circle["points"]["B"]]
        C = scene.mapped_points[circle["points"]["C"]]
        if circle["type"] == "circum_circle":
            centre, radius = em.circum_centre_and_radius(A,B,C)
        elif circle["type"] == "inscribed_circle":
            centre, radius = em.in_centre_and_radius(A,B,C)

    if circle["type"] == "two_point_circle":
        O = scene.mapped_points[circle["points"]["O"]]
        A = scene.mapped_points[circle["points"]["A"]]
        centre, radius = (O, np.linalg.norm(np.array(O)-np.array(A)))
    return centre, radius


# draws/adds a point to the scene with radius and colour given id
def draw_point(scene, id, colour, radius=CANVAS_POINT_RADIUS):
    assert soj.identify_item_type(scene.eucl, id) == "p"
    assert id != 'pt_default'
    x_point, y_point = scene.mapped_points[id]
    graphics_point = QtWidgets.QGraphicsEllipseItem(x_point-radius,y_point-radius, 2*radius, 2*radius)
    graphics_point.setBrush(QtGui.QBrush(colour))
    scene.addItem(graphics_point)


# draws/adds a segment to the scene with thickness and colour given id
def draw_segment(scene, id, colour, thickness=CANVAS_LINE_THICKNESS):
    assert soj.identify_item_type(scene.eucl, id) == "s"
    assert id != 'sg_default'
    segment = soj.get_item_from_id(scene.eucl, id, "s")
    x_from, y_from = scene.mapped_points[segment["points"]["from"]]
    x_to, y_to = scene.mapped_points[segment["points"]["to"]]
    graphics_line = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
    graphics_line.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
    scene.addItem(graphics_line)


# draws/adds a circle to the scene with thickness, colour and number of approximating points given id
def draw_circle(scene, id, colour, num=100, thickness=CANVAS_CIRCLE_THICKNESS):
    assert soj.identify_item_type(scene.eucl, id) == "c"
    assert id != 'crc_default'
    centre, radius = get_circle_centre_radius_on_canvas(scene, id)

    pts = em.circle_approx_pts(centre, radius, num, [0, 360])
    for j in range(len(pts)):
        pt_1 = pts[j]
        pt_2 = pts[(j+1) % len(pts)]
        graphics_line = QtWidgets.QGraphicsLineItem(pt_1[0],pt_1[1], pt_2[0], pt_2[1])
        graphics_line.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
        scene.addItem(graphics_line)


# adds EVERY SELECTED item to the scene with given colour
def add_selected_items_to_scene(scene, colour=QtCore.Qt.blue):
    for point in scene.eucl["points"]:
        if point["id"] == 'pt_default':
            continue
        if point["id"] in scene.selected_objects:
            draw_point(scene, point["id"], colour)
    for segment in scene.eucl["segments"]:
        if segment["id"] == 'sg_default':
            continue
        if segment["id"] in scene.selected_objects:
            draw_segment(scene, segment["id"], colour)
    for circle in scene.eucl["circles"]:
        if circle["id"] == 'crc_default':
            continue
        if circle["id"] in scene.selected_objects:
            draw_circle(scene, circle["id"], colour)


# adds EVERY item to the scene with given colour
def add_all_items_to_scene(scene, colour=QtCore.Qt.blue):
    for point in scene.eucl["points"]:
        if point["id"] == 'pt_default':
            continue
        draw_point(scene, point["id"], colour)
    for segment in scene.eucl["segments"]:
        if segment["id"] == 'sg_default':
            continue
        draw_segment(scene, segment["id"], colour)
    for circle in scene.eucl["circles"]:
        if circle["id"] == 'crc_default':
            continue
        draw_circle(scene, circle["id"], colour)


# adds one specific item with id to the scene
def add_specific_item_to_scene(scene, id, colour=QtCore.Qt.blue):
    if id is None:
        return None
    for point in scene.eucl["points"]:
        if point["id"] == 'pt_default':
            continue
        if id == point["id"]:
            draw_point(scene, point["id"], colour)
            return None
    for segment in scene.eucl["segments"]:
        if segment["id"] == 'sg_default':
            continue
        if id == segment["id"]:
            draw_segment(scene, segment["id"], colour)
            return None
    for circle in scene.eucl["circles"]:
        if circle["id"] == 'crc_default':
            continue
        if id == circle["id"]:
            draw_circle(scene, circle["id"], colour)
            return None














#
