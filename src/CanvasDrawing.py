"""
contains drawing routines for primitives
"""


from PyQt5 import QtCore, QtWidgets, QtGui
import AddNewItem
import EuclMath
import numpy as np # for white image
from cv2 import imwrite # for white image
from Constants import CANVAS_POINT_RADIUS, CANVAS_LINE_THICKNESS, CANVAS_CIRCLE_THICKNESS

def clear_canvas(scene):
    """
    SUMMARY
        clears all objects on the canvas and adds the last compiled pdf image

    PARAMETERS
        scene: GraphicsScene

    RETURNS
        None
    """
    scene.clear()
    pixmap = QtGui.QPixmap("tmp/temp-1.png")
    if not scene.show_pdf:
        pixmap.fill()
    tkz_jpg = QtWidgets.QGraphicsPixmapItem(pixmap)
    scene.addItem(tkz_jpg)
    if scene.aspect_ratio_indicator:
        draw_aspect_ratio(scene, QtCore.Qt.black)


def draw_aspect_ratio(scene, colour):
    """
    SUMMARY
        draws two lines onto the canvas where the given aspect ratio crops the canvas

    PARAMETERS
        scene: GraphicsScene
        colour: colour of the two lines

    RETURNS
        None
    """
    aspect_ratio = eval(scene.aspect_ratio)
    width, height = scene.width(), scene.height()
    window_aspect = width / height
    # aspect_ratio < 1 means we draw vertical lines
    if aspect_ratio < width/height:
        x_from, y_from, x_to, y_to = ((width-height*aspect_ratio)/2, 0, (width-height*aspect_ratio)/2, height)
        graphics_line_1 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
        x_from, y_from, x_to, y_to = (width-(width-height*aspect_ratio)/2, 0, width-(width-height*aspect_ratio)/2, height)
        graphics_line_2 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
    # aspect_ratio > 1 means we draw horizontal lines
    else:
        x_from, y_from, x_to, y_to = (0, (height-width/aspect_ratio)/2, width, (height-width/aspect_ratio)/2)
        graphics_line_1 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
        x_from, y_from, x_to, y_to = (0, height-(height-width/aspect_ratio)/2, width, height-(height-width/aspect_ratio)/2)
        graphics_line_2 = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
    # if aspect ratio is 1 we don't draw at all
    if aspect_ratio != width/height:
        graphics_line_1.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
        graphics_line_2.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
        scene.addItem(graphics_line_1)
        scene.addItem(graphics_line_2)

def empty_jpg(width, height):
    """
    SUMMARY
        makes empty white jpg

    PARAMETERS
        width: float
        height: float

    RETURNS
        None
    """
    empty_image = 255 * np.ones((int(width), int(height))) # blank white bw-matrix
    imwrite('tmp/temp-1.png', empty_image)

def always_on_drawing_plan(scene):
    """
    SUMMARY
        draws on the canvas with always on policy

    PARAMETERS
        scene: GraphicsScene

    RETURNS
        None
    """
    if scene.canvas_always_on:
        clear_canvas(scene)
        add_all_items_to_scene(scene, QtCore.Qt.darkCyan)
        add_selected_items_to_scene(scene, QtCore.Qt.blue)
        add_specific_item_to_scene(scene, scene.focused_point_id, QtCore.Qt.darkMagenta)

def always_off_drawing_plan(scene):
    """
    SUMMARY
        draws on the canvas with always off policy

    PARAMETERS
        scene: GraphicsScene

    RETURNS
        None
    """
    if not scene.canvas_always_on:
        clear_canvas(scene)
        add_selected_items_to_scene(scene, QtCore.Qt.blue)
        add_specific_item_to_scene(scene, scene.focused_point_id, QtCore.Qt.darkMagenta)


def get_circle_centre_radius_on_canvas(scene, id):
    """
    SUMMARY
        computes the centre and radius of a circle in the canvas coordinate system

    PARAMETERS
        scene: GraphicsScene
        id: id of a circle

    RETURNS
        None
    """
    assert AddNewItem.identify_item_type(scene.eucl, id) == "c"
    assert id != 'crc_default'
    circle = AddNewItem.get_item_from_id(scene.eucl, id, "c")
    centre, radius = (0,0)

    if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
        A = scene.mapped_points[circle["points"]["A"]]
        B = scene.mapped_points[circle["points"]["B"]]
        C = scene.mapped_points[circle["points"]["C"]]
        if circle["type"] == "circum_circle":
            centre, radius = EuclMath.circum_centre_and_radius(A,B,C)
        elif circle["type"] == "inscribed_circle":
            centre, radius = EuclMath.in_centre_and_radius(A,B,C)

    if circle["type"] == "two_point_circle":
        O = scene.mapped_points[circle["points"]["O"]]
        A = scene.mapped_points[circle["points"]["A"]]
        centre, radius = (O, np.linalg.norm(np.array(O)-np.array(A)))
    return centre, radius


def draw_point(scene, id, colour, radius=CANVAS_POINT_RADIUS):
    """
    SUMMARY
        draws/adds a point to the scene with radius and colour given id

    PARAMETERS
        scene: GraphicsScene
        id: id of a point
        colour: colour of the point
        radius: radius of the point

    RETURNS
        None
    """
    assert AddNewItem.identify_item_type(scene.eucl, id) == "p"
    assert id != 'pt_default'
    x_point, y_point = scene.mapped_points[id]
    graphics_point = QtWidgets.QGraphicsEllipseItem(x_point-radius,y_point-radius, 2*radius, 2*radius)
    graphics_point.setBrush(QtGui.QBrush(colour))
    scene.addItem(graphics_point)


def draw_segment(scene, id, colour, thickness=CANVAS_LINE_THICKNESS):
    """
    SUMMARY
        draws/adds a segment to the scene with thickness and colour given id


    PARAMETERS
        scene: GraphicsScene
        id: id of a segment
        colour: colour of the segment
        thickness: thickness of the segment

    RETURNS
        None
    """
    assert AddNewItem.identify_item_type(scene.eucl, id) == "s"
    assert id != 'sg_default'
    segment = AddNewItem.get_item_from_id(scene.eucl, id, "s")
    x_from, y_from = scene.mapped_points[segment["points"]["from"]]
    x_to, y_to = scene.mapped_points[segment["points"]["to"]]
    graphics_line = QtWidgets.QGraphicsLineItem(x_from, y_from, x_to, y_to)
    graphics_line.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
    scene.addItem(graphics_line)


def draw_circle(scene, id, colour, num=100, thickness=CANVAS_CIRCLE_THICKNESS):
    assert AddNewItem.identify_item_type(scene.eucl, id) == "c"
    assert id != 'crc_default'
    centre, radius = get_circle_centre_radius_on_canvas(scene, id)

    pts = EuclMath.circle_approx_pts(centre, radius, num, [0, 360])
    for j in range(len(pts)):
        pt_1 = pts[j]
        pt_2 = pts[(j+1) % len(pts)]
        graphics_line = QtWidgets.QGraphicsLineItem(pt_1[0],pt_1[1], pt_2[0], pt_2[1])
        graphics_line.setPen(QtGui.QPen(QtGui.QBrush(colour), CANVAS_LINE_THICKNESS))
        scene.addItem(graphics_line)


def add_selected_items_to_scene(scene, colour=QtCore.Qt.blue):
    """
    SUMMARY
        adds every selected item to the scene with given colour

    PARAMETERS
        scene: GraphicsScene
        colour: colour for the items

    RETURNS
        None
    """
    for point in scene.eucl["points"]:
        if point["id"] in scene.selected_objects and point["id"] != 'pt_default':
            draw_point(scene, point["id"], colour)
    for segment in scene.eucl["segments"]:
        if segment["id"] in scene.selected_objects and segment["id"] != 'sg_default':
            draw_segment(scene, segment["id"], colour)
    for circle in scene.eucl["circles"]:
        if circle["id"] in scene.selected_objects and circle["id"] == 'crc_default':
            draw_circle(scene, circle["id"], colour)


def add_all_items_to_scene(scene, colour=QtCore.Qt.blue):
    """
    SUMMARY
        adds every item to the scene with given colour

    PARAMETERS
        scene: GraphicsScene
        colour: colour for the items

    RETURNS
        None
    """
    for point in scene.eucl["points"]:
        if point["id"] != 'pt_default':
            draw_point(scene, point["id"], colour)
    for segment in scene.eucl["segments"]:
        if segment["id"] != 'sg_default':
            draw_segment(scene, segment["id"], colour)
    for circle in scene.eucl["circles"]:
        if circle["id"] != 'crc_default':
            draw_circle(scene, circle["id"], colour)

def add_specific_item_to_scene(scene, id, colour=QtCore.Qt.blue):
    """
    SUMMARY
        adds one specific item with id to the scene

    PARAMETERS
        scene: GraphicsScene
        id: id of item

    RETURNS
        None
    """
    if id is None:
        return None
    for point in scene.eucl["points"]:
        if id == point["id"] and point["id"] != 'pt_default':
            draw_point(scene, point["id"], colour)
            return None
    for segment in scene.eucl["segments"]:
        if id == segment["id"] and segment["id"] != 'sg_default':
            draw_segment(scene, segment["id"], colour)
            return None
    for circle in scene.eucl["circles"]:
        if id == circle["id"] and circle["id"] != 'crc_default':
            draw_circle(scene, circle["id"], colour)
            return None
