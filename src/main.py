#!/usr/bin/env python

"""
this file contains the definition of the main qui window
"""


import sys, os, json
import numpy as np
import son_of_j as soj
import eucl_math as em
import properties
from constants import *
import canvas_drawing as cd
from math import trunc
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from copy import deepcopy
from pandas.io.clipboard import copy as copy_to_clipboard
from collections import namedtuple

save_state = namedtuple('save_state', 'opened_file unsaved_progress')

# returns CSS/HTML formatted tikz code from source if pygments is installed
def pygments_syntax_highlight(text):
    style = get_style_by_name('colorful')
    formatter = HtmlFormatter(full=True, noclasses=True, style=style)
    lex = lexers.get_lexer_by_name("latex")
    return highlight(text, lex, formatter)


# returns CSS/HTML formatted tikz code from source if pygments is NOT installed
def alternative_syntax_highlight(text):
    def replace_pivot_spaces(text):
        exit_condition = True
        while exit_condition:
            exit_condition = False
            for i in range(len(text)-1):
                if text[i] == '\n' and text[i+1] == ' ':
                    numspace = 1
                    while text[i+1+numspace] == ' ':
                        numspace += 1
                    text = text[:i+1] + numspace*'&nbsp;' + text[i+1+numspace:]
                    exit_condition = True
        return text
    # only full rows starting with %
    def highlight_comments(text):
        text = text.split('\n')
        for i in range(len(text)):
            if len(text[i]) > 0 and text[i][0] == "%":
                text[i] = '<span style="color:blue;font-weight:bold">' + text[i] + '</span>'
        return '\n'.join(text)

    text = replace_pivot_spaces(text)
    text = highlight_comments(text)
    text = text.replace('\\begin', '<span style="color:brown;font-weight:bold">\\begin</span>')
    text = text.replace('\\end', '<span style="color:brown;font-weight:bold">\\end</span>')
    text = text.replace('\n', '<br>')
    return text


# check for pygments
try:
    from pygments import highlight, lexers
    from pygments.styles import get_style_by_name
    from pygments.formatters import HtmlFormatter
    print(i == 1/0)
    syntax_highlight = pygments_syntax_highlight
except:
    syntax_highlight = alternative_syntax_highlight


# loading the settings from file
with open('settings.json') as f:
        settings = json.load(f)

# the canvas is PIXELS by PIXELS read from the settings file
PIXELS = settings['pixels']
WIDTH, HEIGHT = PIXELS, PIXELS

# the latex command line command for compiling the generated tex file
LATEX_COMMAND = settings['latex']
PDF_TO_JPG = settings['pdf to jpg'].replace('$PIXELS', str(PIXELS))



# check if <pref> is prefix for <word>
def is_prefix(pref, word):
    if word.find(pref) == 0:
        return True
    else:
        return False


# item types: list of object types the concludes an edit,
# poly strings: special edit types for linestrings and polygons
# validates whether the end of typehistory matches any type in <item_types>
def validate_selected_item(scene, item_types, poly_string=0):
    type_sofar_ok = False
    selection_concluded = False
    concluded_item_type = None
    for item_type in item_types:
        if is_prefix(scene.selected_item_type_history[-1-len(scene.selected_objects):], item_type):
            type_sofar_ok = True
            scene.selected_objects.append(scene.focused_point_id)
            selected_length = len(scene.selected_objects)
            if selected_length == len(item_type):
                if poly_string == 0: #nothing special
                    selection_concluded = True
                    concluded_item_type = item_type
                if poly_string == 1 and scene.selected_objects[-2] == scene.selected_objects[-1]: #linestring
                    selection_concluded = True
                    concluded_item_type = item_type
                if poly_string == 2 and scene.selected_objects[0] == scene.selected_objects[-1]: #polygon
                    selection_concluded = True
                    concluded_item_type = item_type
            break
    if not type_sofar_ok:
        scene.selected_objects.clear()
        cd.clear_canvas(scene)
    return (selection_concluded, concluded_item_type)


# converts canvas coordinates to tikz coordinates
def canvascoord2tkzcoord(x_canvas, y_canvas, lbs):
    left, bottom, scale = lbs
    x_tkz = left + x_canvas/WIDTH * scale*10
    y_tkz = bottom + (HEIGHT-y_canvas) / HEIGHT * scale*10

    return str(x_tkz), str(y_tkz)


# converts tikz coordinates to canvas coordinates
def tkzcoord2canvascoord(x_tkz, y_tkz, lbs):
    left, bottom, scale = lbs
    x_canvas = (eval(x_tkz) - left) * WIDTH / (scale * 10)
    y_canvas = -(eval(y_tkz) - bottom) * HEIGHT / (scale * 10) + HEIGHT

    return [x_canvas, y_canvas]


# when undo is pressed, adds extra undo elements to the undo's list
def add_new_undo_item(scene):
    scene.save_state = save_state(scene.save_state.opened_file, True)
    scene.undo_history.append(deepcopy(scene.eucl))
    scene.redo_history.clear()
    scene.actionUndo.setEnabled(True)
    scene.actionRedo.setEnabled(False)
    if scene.save_state.unsaved_progress:
        scene.actionSave.setEnabled(True)
    else:
        scene.actionSave.setEnabled(False)


# performs pdflatex command if autocompile, and updates canvas and highlighted
# tikz code accordingly
def compile_tkz_and_render(scene):
    write_file = open('tmp/temp.tex', "w")
    tikz_text = soj.eucl2tkz(scene.eucl, scene.left_bottom_scale())
    text_to_write = soj.tkz2tex(scene.eucl, tikz_text)
    write_file.write(text_to_write)
    write_file.close()

    browser_text = syntax_highlight(tikz_text)
    scene.textBrowser.setText(browser_text)
    if scene.autocompile:
        os.system(LATEX_COMMAND)
        os.system(PDF_TO_JPG)

    directory = os.path.realpath(__file__)[:-len(__file__)]
    for item in os.listdir(directory):
        if item.endswith(".gnuplot") or item.endswith(".table"):
            os.remove(os.path.join(directory, item))
    cd.always_on_drawing_plan(scene)
    cd.always_off_drawing_plan(scene)


# finds all points by coordinate on the canvas
def compute_mapped_points(scene, focus_pt_coords=None):
    mapped_points = {}
    mapped_points['pt_default'] = (0,0)
    if focus_pt_coords is not None:
        x,y = focus_pt_coords

    num_points = len(scene.eucl["points"])

    while len(mapped_points) < num_points:
        for point in scene.eucl["points"]:
            if point["id"] in mapped_points:
                continue

            if focus_pt_coords is not None and point["id"] == scene.focused_point_id:
                coords = canvascoord2tkzcoord(x, y, scene.left_bottom_scale())
                mapped_points[scene.focused_point_id] = [float(coords[0]), float(coords[1])]
            elif point["from"]["type"] == "free":
                mapped_points[point["id"]] = [eval(point["x"]), eval(point["y"])]
            elif point["from"]["type"] == "intersection_ll":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    if point["from"]["C"] in mapped_points and point["from"]["D"] in mapped_points:
                        A_ = mapped_points[point["from"]["A"]]
                        B_ = mapped_points[point["from"]["B"]]
                        C_ = mapped_points[point["from"]["C"]]
                        D_ = mapped_points[point["from"]["D"]]
                        inter_coords = em.ll_intersection(A_,B_,C_,D_)
                        mapped_points[point["id"]] = inter_coords
            elif point["from"]["type"] == "intersection_lc":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    for pt in scene.eucl["points"]:
                        if pt["from"]["type"] == "intersection_lc" and pt["id"] != point["id"] and pt["from"]["lc_id"] == point["from"]["lc_id"]:
                            circle = soj.get_item_from_id(scene.eucl, point["from"]["circle"], 'c')
                            if circle["type"] == "two_point_circle":
                                if circle["points"]["O"] in mapped_points and circle["points"]["A"] in mapped_points:
                                    centre = mapped_points[circle["points"]["O"]]
                                    circ_A = mapped_points[circle["points"]["A"]]
                                    pt_A = mapped_points[point["from"]["A"]]
                                    pt_B = mapped_points[point["from"]["B"]]
                                    radius = np.linalg.norm(np.array(centre)-np.array(circ_A))
                                    coords, reverse_intersections = em.lc_intersection(centre, radius, pt_A, pt_B)
                            if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                                if circle["points"]["A"] in mapped_points and circle["points"]["B"] in mapped_points and\
                                   circle["points"]["C"] in mapped_points:
                                    circ_A = mapped_points[circle["points"]["A"]]
                                    circ_B = mapped_points[circle["points"]["B"]]
                                    circ_C = mapped_points[circle["points"]["C"]]
                                    if circle["type"] == "circum_circle":
                                        centre, radius = em.circum_centre_and_radius(circ_A, circ_B, circ_C)
                                    else:
                                        centre, radius = em.in_centre_and_radius(circ_A, circ_B, circ_C)
                                    pt_A = mapped_points[point["from"]["A"]]
                                    pt_B = mapped_points[point["from"]["B"]]
                                    coords, reverse_intersections = em.lc_intersection(centre, radius, pt_A, pt_B)
                            mapped_points[point["id"]] = coords[0]
                            mapped_points[pt["id"]] = coords[1]
                            if reverse_intersections:
                                point["reverse_intersections"] = True
                                pt["reverse_intersections"] = True
                            else:
                                point["reverse_intersections"] = False
                                pt["reverse_intersections"] = False

            elif point["from"]["type"] == "circle_midpoint":
                circle_id = point["from"]["circle"]
                circle = soj.get_item_from_id(scene.eucl, circle_id, 'c')
                if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        A_ = mapped_points[circle["points"]["A"]]
                        B_ = mapped_points[circle["points"]["B"]]
                        C_ = mapped_points[circle["points"]["C"]]
                        if circle["type"] == "circum_circle":
                            centre = em.circumcentre(A_,B_,C_)
                        else:
                            centre = em.incentre(A_,B_,C_)
                        mapped_points[point["id"]] = centre
            elif point["from"]["type"] == "segment_midpoint":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    midpoint = [(A[0]+B[0])/2, (A[1]+B[1])/2]
                    mapped_points[point["id"]] = midpoint
            elif point["from"]["type"] == "rotation":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    A = np.array(mapped_points[point["from"]["A"]]).reshape(2,1)
                    B = np.array(mapped_points[point["from"]["B"]]).reshape(2,1)
                    angle = eval(point["from"]["angle"])
                    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],\
                                               [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])
                    angle_point = list((A+rotation_matrix@(B-A)).flatten())
                    mapped_points[point["id"]] = angle_point
            elif point["from"]["type"] == "point_on_line":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    r = eval(point["from"]["ratio"])
                    point_on_line = [(A[0]+r*B[0])/(1+r), (A[1]+r*B[1])/(1+r)]
                    point_on_line = [A[0]+r*(B[0]-A[0]), A[1]+r*(B[1]-A[1])]
                    mapped_points[point["id"]] = point_on_line

            elif point["from"]["type"] == "point_on_circle":
                circle_id = point["from"]["circle"]
                circle = soj.get_item_from_id(scene.eucl, circle_id, 'c')
                if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        A_ = mapped_points[circle["points"]["A"]]
                        B_ = mapped_points[circle["points"]["B"]]
                        C_ = mapped_points[circle["points"]["C"]]
                        if circle["type"] == "circum_circle":
                            centre, radius = em.circum_centre_and_radius(A_,B_,C_)
                        elif circle["type"] == "inscribed_circle":
                            centre, radius = em.in_centre_and_radius(A_,B_,C_)
                else:
                    O = mapped_points[circle["points"]["O"]]
                    A = mapped_points[circle["points"]["A"]]
                    centre, radius = O, np.sqrt((O[0]-A[0])**2 + (O[1]-A[1])**2)

                mapped_points[point["id"]] = [centre[0] + radius * np.cos(np.radians(eval(point["from"]["angle"]))),
                                              centre[1] - radius * np.sin(np.radians(eval(point["from"]["angle"])))]
            elif point["from"]["type"] == "projection_point":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points and\
                   point["from"]["P"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    P = mapped_points[point["from"]["P"]]
                    projection_point = em.orthogonal_projection(A,B,P)
                    mapped_points[point["id"]] = projection_point
            elif point["from"]["type"] == "bisector_point":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points and\
                   point["from"]["C"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    C = mapped_points[point["from"]["C"]]
                    bisector_point = em.bisector_point(A,B,C)
                    mapped_points[point["id"]] = bisector_point
            elif point["from"]["type"] == "translation_point":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points and\
                   point["from"]["P"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    P = mapped_points[point["from"]["P"]]
                    translation_point = [P[0]+B[0]-A[0], P[1]+B[1]-A[1]]
                    mapped_points[point["id"]] = translation_point
            elif point["from"]["type"] == "orthogonal_point":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    orthogonal_point = [A[0] - B[1]+A[1], A[1] - A[0]+B[0]]
                    mapped_points[point["id"]] = orthogonal_point

    for key, value in mapped_points.items():
        mapped_points[key] = tkzcoord2canvascoord(str(value[0]), str(value[1]), scene.left_bottom_scale())
    scene.mapped_points = mapped_points


# class for the graphics scene (canvas)
class graphicsScene(QtWidgets.QGraphicsScene):
    def __init__ (self):
        super(graphicsScene, self).__init__ ()
        self.mouse_x = 0
        self.mouse_y = 0
        self.current_mode = 0
        self.eucl = soj.new_eucl_file()
        self.setSceneRect(0, 0, PIXELS-1, PIXELS-1);
        self.focused_point_id = None
        self.selected_objects = []
        self.movePoint = False
        self.move_objects = []
        self.mouse_being_pressed = False
        self.mapped_points = {}
        self.move_canvas = [False, 0, 0] # [True if MOVE_AND_SCALE_CANVAS else False, mouse_x, mouse_y]
        self.undo_history = [soj.new_eucl_file()] # undo history starts with empty eucl
        self.redo_history = [] # redo history is empty at the start
        self.zoom_new_window_params = [0,0,0] # [left, bottom, scale]
        self.selected_item_type_history = "" # type of past selected objects "p": point, "s": segment, "c": circle
        self.autocompile = True
        self.canvas_always_on = False
        self.change_made = False # an actual change has been recorded
        self.show_pdf = True
        self.aspect_ratio_indicator = False
        self.aspect_ratio = "16/9"
        self.save_state = save_state(None, False)

        # loading settings
        with open('settings.json') as f:
            self.settings = json.load(f)


    def compile_tkz_and_render(self):
        compile_tkz_and_render(self)

    def compute_mapped_points(self, focus_pt_coords=None):
        compute_mapped_points(self, focus_pt_coords=None)

    def add_new_undo_item(self):
        add_new_undo_item(self)


    # get current_mode
    def get_current_mode(self, current_mode):
        self.current_mode = current_mode

    # get references for textBrowser
    def get_textBrowser(self, textBrowser):
        self.textBrowser = textBrowser

    # get references for actionRedo
    def get_actionRedo(self, actionRedo):
        self.actionRedo = actionRedo

    # get references for actionUndo
    def get_actionUndo(self, actionUndo):
        self.actionUndo = actionUndo

    def get_actionSave(self, actionSave):
        self.actionSave = actionSave
        self.actionSave.setEnabled(False)

    # get references for left, bottom, scale
    def left_bottom_scale(self):
        return [self.eucl["window"]["left"],\
                self.eucl["window"]["bottom"],\
                self.eucl["window"]["scale"]]

    # get the id of an object in highlight
    def get_focused_id(self, x, y):
        point_in_focus = False
        focused_point_id = None
        if len(self.eucl["points"]) > 1:
            sorted_distance_to_points = []
            for point in self.eucl["points"]:
                if point["id"] != 'pt_default':
                    canvas_point = self.mapped_points[point["id"]]
                    sorted_distance_to_points.append((point, canvas_point))
            sorted_distance_to_points.sort(key=lambda z : (z[1][0]-x)**2+(z[1][1]-y)**2)
            x_point, y_point = sorted_distance_to_points[0][1]
            minimal_point = sorted_distance_to_points[0][0]

            if (x-x_point)**2+(y-y_point)**2 <= MAX_DISTANCE_TO_HIGHLIGHT**2:
                focused_point_id = minimal_point["id"]
                point_in_focus = True
            else:
                focused_point_id = None

        min_segment_dist = 10000000
        if len(self.eucl["segments"]) > 1 and not point_in_focus:
            sorted_distance_to_segments = []
            for segment in self.eucl["segments"]:
                if segment["id"] != 'sg_default':
                    A = self.mapped_points[segment["points"]["from"]]
                    B = self.mapped_points[segment["points"]["to"]]
                    sorted_distance_to_segments.append((segment, em.pt_segment_dist(A, B, (x,y))))
            sorted_distance_to_segments.sort(key=lambda z : z[1])

            if sorted_distance_to_segments[0][1] <= MAX_DISTANCE_TO_HIGHLIGHT:
                minimal_segment, min_segment_dist = sorted_distance_to_segments[0]
                focused_point_id = minimal_segment["id"]
            else:
                focused_point_id = None
        if len(self.eucl["circles"]) > 1 and not point_in_focus:
            sorted_distance_to_circles = []
            for circle in self.eucl["circles"]:
                if circle["id"] == 'crc_default':
                    continue
                centre, radius = cd.get_circle_centre_radius_on_canvas(self, circle["id"])
                sorted_distance_to_circles.append((circle, em.pt_circle_dist(centre, radius, (x,y))))
            sorted_distance_to_circles.sort(key=lambda z : z[1])

            if sorted_distance_to_circles[0][1] <= MAX_DISTANCE_TO_HIGHLIGHT:
                circle, _ = sorted_distance_to_circles[0]
                focused_point_id = circle["id"]

            elif min_segment_dist > 8:
                focused_point_id = None
        return focused_point_id


    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mouse_being_pressed = True
            position = QtCore.QPointF(event.scenePos())
            x,y = (position.x(), position.y())
            print ("pressed here: " + str(x) + ", " + str(y))
            self.mouse_x = x
            self.mouse_y = y
            self.change_made = False
            if self.current_mode == NEW_POINT:
                x_tkz, y_tkz = canvascoord2tkzcoord(x, y, self.left_bottom_scale())
                soj.register_new_point(self.eucl, [x_tkz, y_tkz], setup=NEW_POINT)
                self.change_made = True
            else:
                if self.focused_point_id is not None:
                    self.selected_item_type_history += soj.identify_item_type(self.eucl, self.focused_point_id)

                if self.current_mode == SEGMENT_THROUGH:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pp"])
                        if selection_concluded:
                            soj.register_new_line(self.eucl, self.selected_objects, setup=SEGMENT_THROUGH)
                            self.change_made = True
                elif self.current_mode == POLYGON:
                    if self.focused_point_id is not None:
                        id_options = ['p'*i for i in range(3,101)]
                        selection_concluded, concluded_item_type = validate_selected_item(self, id_options, 2)
                        if selection_concluded:
                            soj.register_new_polygon(self.eucl, self.selected_objects[:-1], setup=POLYGON)
                            self.change_made = True
                elif self.current_mode == LINESTRING:
                    if self.focused_point_id is not None:
                        id_options = ['p'*i for i in range(3,101)]
                        selection_concluded, concluded_item_type = validate_selected_item(self, id_options, 1)
                        if selection_concluded:
                            soj.register_new_polygon(self.eucl, self.selected_objects[:-1], setup=LINESTRING)
                            self.change_made = True
                elif self.current_mode == CIRCUM_CIRCLE:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_circle(self.eucl, self.selected_objects, setup=CIRCUM_CIRCLE)
                            self.change_made = True
                elif self.current_mode == TWO_POINT_CIRCLE:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pp"])
                        if selection_concluded:
                            soj.register_new_circle(self.eucl, self.selected_objects, setup=TWO_POINT_CIRCLE)
                            self.change_made = True
                elif self.current_mode == ARC:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_circle(self.eucl, self.selected_objects, setup=ARC)
                            self.change_made = True
                elif self.current_mode == SECTOR:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_circle(self.eucl, self.selected_objects, setup=SECTOR)
                            self.change_made = True
                elif self.current_mode == INSCRIBED_CIRCLE:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_circle(self.eucl, self.selected_objects, setup=INSCRIBED_CIRCLE)
                            self.change_made = True
                elif self.current_mode == INTERSECT_POINT:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pppp", "ss", "cs", "sc", "ppc", "cpp"])
                        if selection_concluded:
                            if concluded_item_type == "pppp":
                                data = self.selected_objects
                                soj.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="pppp")
                            elif concluded_item_type == "ss":
                                segment_1 = soj.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                                segment_2 = soj.get_item_from_id(self.eucl, self.selected_objects[1], 's')
                                A, B = [segment_1["points"]["from"], segment_1["points"]["to"]]
                                C, D = [segment_2["points"]["from"], segment_2["points"]["to"]]
                                data = [A,B,C,D]
                                soj.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="pppp")
                            elif concluded_item_type in ["cs", "sc"]:
                                if concluded_item_type == "sc":
                                    self.selected_objects = list(reversed(self.selected_objects))
                                segment = soj.get_item_from_id(self.eucl, self.selected_objects[1], 's')
                                A, B = [segment["points"]["from"], segment["points"]["to"]]
                                data = [self.selected_objects[0], A, B]
                                soj.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="cpp")
                            elif concluded_item_type in ["ppc", "cpp"]:
                                if concluded_item_type == "ppc":
                                    self.selected_objects = list(reversed(self.selected_objects))
                                data = self.selected_objects
                                soj.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="cpp")
                            self.change_made = True
                elif self.current_mode == MIDPOINT_CIRCLE:
                    if self.focused_point_id is not None:
                        self.selected_objects.append(self.focused_point_id)
                        if len(self.selected_objects) == 1:
                            soj.register_new_point(self.eucl, self.selected_objects, setup=MIDPOINT_CIRCLE)
                            self.change_made = True
                elif self.current_mode == MIDPOINT_SEGMENT:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pp", "s"])
                        if selection_concluded:
                            if concluded_item_type == "pp":
                                data = self.selected_objects
                            elif concluded_item_type == "s":
                                segment = soj.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                                A, B = [segment["points"]["from"], segment["points"]["to"]]
                                data = [A,B]
                            soj.register_new_point(self.eucl, data, setup=MIDPOINT_SEGMENT)
                            self.change_made = True
                elif self.current_mode == ROTATION:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pp"])
                        if selection_concluded:
                            data = self.selected_objects
                            dialog = PointRotated(self, data)
                            dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                            dialog.exec_()
                            self.change_made = True
                elif self.current_mode == POINT_ON_LINE:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pp", "s"])
                        if selection_concluded:
                            if concluded_item_type == "pp":
                                data = self.selected_objects
                            elif concluded_item_type == "s":
                                segment = soj.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                                A, B = [segment["points"]["from"], segment["points"]["to"]]
                                data = [A,B]

                            dialog = PointOnLineDialog(self, data)
                            dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                            dialog.exec_()
                            # do something to bring up dialog
                            self.change_made = True
                elif self.current_mode == POINT_ON_CIRCLE:
                    selection_concluded, concluded_item_type = validate_selected_item(self, ["c"])
                    if selection_concluded:
                        data = self.selected_objects

                        dialog = PointOnCircleDialog(self, data)
                        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                        dialog.exec_()
                        # do something to bring up dialog
                        self.change_made = True
                elif self.current_mode == MAKEGRID:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            data = self.selected_objects
                            dialog = MakeGridDialog(self, data)
                            dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                            dialog.exec_()
                            # do something to bring up dialog
                            self.change_made = True
                elif self.current_mode == MARK_RIGHT_ANGLE:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_angle(self.eucl, self.selected_objects, setup=MARK_RIGHT_ANGLE)
                            self.change_made = True
                elif self.current_mode == MARK_ANGLE:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_angle(self.eucl, self.selected_objects, setup=MARK_ANGLE)
                            self.change_made = True
                elif self.current_mode == ORTHOGONAL_PROJECTION:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp", "sp", "ps"])
                        if selection_concluded:
                            if concluded_item_type == "ppp":
                                data = self.selected_objects
                            elif concluded_item_type == "sp" or concluded_item_type == "ps":
                                if concluded_item_type == "ps":
                                    self.selected_objects = list(reversed(self.selected_objects))
                                segment = soj.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                                A, B = [segment["points"]["from"], segment["points"]["to"]]
                                data = [A,B, self.selected_objects[1]]
                            soj.register_new_point(self.eucl, data, setup=ORTHOGONAL_PROJECTION)
                            self.change_made = True
                elif self.current_mode == BISECTOR:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_point(self.eucl, self.selected_objects, setup=BISECTOR)
                            self.change_made = True
                elif self.current_mode == TRANSLATION:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["ppp"])
                        if selection_concluded:
                            soj.register_new_point(self.eucl, self.selected_objects, setup=TRANSLATION)
                            self.change_made = True
                elif self.current_mode == ORTHOGONAL:
                    if self.focused_point_id is not None:
                        selection_concluded, concluded_item_type = validate_selected_item(self, ["pp"])
                        if selection_concluded:
                            soj.register_new_point(self.eucl, self.selected_objects, setup=ORTHOGONAL)
                            self.change_made = True

            if self.current_mode == MOVE_POINT:
                self.movePoint = True
            elif self.current_mode == MOVE_AND_SCALE_CANVAS:
                self.move_canvas = [True, x, y]
            compute_mapped_points(self)
            if self.canvas_always_on:
                cd.add_all_items_to_scene(self, QtCore.Qt.darkCyan)
                if self.focused_point_id is not None:
                    cd.add_specific_item_to_scene(self, self.focused_point_id, QtCore.Qt.darkMagenta)


        if event.buttons() == QtCore.Qt.RightButton:
            self.open_settings()

        if self.canvas_always_on:
            cd.add_selected_items_to_scene(self)

    def open_settings(self):
        dialog = properties.PropertiesDialog(self)
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()

    def open_help(self):
        class HelpDialog(QtWidgets.QDialog):
            def __init__(self):
                super(HelpDialog, self).__init__()
                self.ui = uic.loadUi('layouts/help.ui', self)
                self.setWindowTitle("Help")

        dialog = HelpDialog()
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()

    def mouseMoveEvent(self, event):
        position = QtCore.QPointF(event.scenePos())
        x,y = (position.x(), position.y())
        # print ("moved here: " + str(x) + ", " + str(y))
        self.mouse_x = x
        self.mouse_y = y
        radius = CANVAS_POINT_RADIUS

        if self.current_mode == NEW_POINT:
            cd.always_on_drawing_plan(self)
            cd.always_off_drawing_plan(self)

        if self.current_mode != NEW_POINT:
            if not self.movePoint:
                new_focused_id = self.get_focused_id(x, y)
                if new_focused_id != self.focused_point_id:
                    self.focused_point_id = new_focused_id
                    cd.always_on_drawing_plan(self)
                    cd.always_off_drawing_plan(self)
                if self.focused_point_id is None:
                    cd.always_on_drawing_plan(self)
                    cd.always_off_drawing_plan(self)
        if self.movePoint == True and self.focused_point_id is not None:
            compute_mapped_points(self, [x,y])
            cd.clear_canvas(self)
            # self.clear()
            cd.add_all_items_to_scene(self, QtCore.Qt.darkMagenta)
        if self.current_mode == MOVE_AND_SCALE_CANVAS and self.move_canvas[0] == True:
            saved_mapping = dict(self.mapped_points)
            for id in self.mapped_points:
                self.mapped_points[id] = (self.mapped_points[id][0] +x - self.move_canvas[1], self.mapped_points[id][1] +y - self.move_canvas[2])
            cd.clear_canvas(self)
            # self.clear()
            cd.add_all_items_to_scene(self, QtCore.Qt.darkMagenta)
            self.mapped_points = saved_mapping


    def mouseReleaseEvent(self, event):
        self.mouse_being_pressed = False
        position = QtCore.QPointF(event.scenePos())
        x,y = (position.x(), position.y())
        # print ("released here: " + str(x) + ", " + str(y))
        self.mouse_x = x
        self.mouse_y = y

        if self.current_mode == MOVE_POINT and self.focused_point_id is not None:
            for i,point in enumerate(self.eucl["points"]):
                if point["id"] == self.focused_point_id:
                    x_point, y_point = canvascoord2tkzcoord(x, y, self.left_bottom_scale())
                    self.eucl["points"][i]["x"] = x_point
                    point["y"] = y_point
                if point["from"]["type"] == "intersection_ll":
                    pt = self.mapped_points[point["id"]]
                    x_point, y_point = canvascoord2tkzcoord(pt[0], pt[1], self.left_bottom_scale())
                    self.eucl["points"][i]["x"] = x_point
                    point["y"] = y_point

            compile_tkz_and_render(self)
            add_new_undo_item(self)
        self.movePoint = False

        if self.current_mode == MOVE_AND_SCALE_CANVAS and self.move_canvas[0] == True:
            for id in self.mapped_points:
                self.mapped_points[id] = (self.mapped_points[id][0] +x - self.move_canvas[1], self.mapped_points[id][1] +y - self.move_canvas[2])
            from_x, from_y = (self.move_canvas[1], self.move_canvas[2])
            self.move_canvas = [False, 0, 0]
            scale = self.eucl["window"]["scale"]
            dx = (from_x-x)/WIDTH *scale*10
            dy = (from_y-y)/HEIGHT *scale*10
            self.eucl["window"]["left"] += dx
            self.eucl["window"]["bottom"] -= dy
            compile_tkz_and_render(self)
            add_new_undo_item(self)

        if self.change_made:
            self.change_made = False
            compile_tkz_and_render(self)
            compute_mapped_points(self)
            add_new_undo_item(self)
            self.selected_objects.clear()

        cd.always_on_drawing_plan(self)
        cd.always_off_drawing_plan(self)


# class for the whole main window
class EuclMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(EuclMainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        self.ui = uic.loadUi('layouts/main.ui', self)
        self.scene = graphicsScene() # QtWidgets.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.get_textBrowser(self.ui.textBrowser)
        self.scene.get_actionRedo(self.ui.actionRedo)
        self.scene.get_actionUndo(self.ui.actionUndo)
        self.scene.get_actionSave(self.ui.actionSave)
        self.mouse_x = 0
        self.mouse_y = 0

        self.current_mode = 0
        self.current_tool = 0

        self.point_index = 0
        self.line_index = 0
        self.circle_index = 0
        self.move_index = 0
        self.decorator_index = 0

        self.ui.comboBox.currentIndexChanged.connect(self.combobox_point_change)
        self.ui.comboBox_2.currentIndexChanged.connect(self.combobox_line_change)
        self.ui.comboBox_3.currentIndexChanged.connect(self.combobox_circle_change)
        self.ui.comboBox_4.currentIndexChanged.connect(self.combobox_move_change)
        self.ui.comboBox_5.currentIndexChanged.connect(self.combobox_decorator_change)
        self.ui.radioButton.clicked.connect(self.radiobutton_triggered)
        self.ui.radioButton_2.clicked.connect(self.radiobutton_triggered_2)
        self.ui.radioButton_3.clicked.connect(self.radiobutton_triggered_3)
        self.ui.radioButton_4.clicked.connect(self.radiobutton_triggered_4)
        self.ui.radioButton_5.clicked.connect(self.radiobutton_triggered_5)
        self.ui.actionSave_As.triggered.connect(self.save_into_file)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionNew.triggered.connect(self.new_file)
        self.ui.actionopen_settings.triggered.connect(self.scene.open_settings)
        self.ui.menuHelp.aboutToShow.connect(self.scene.open_help)
        self.ui.horizontalSlider.sliderMoved.connect(self.scale_slider_move)
        self.ui.horizontalSlider.sliderPressed.connect(self.scale_slider_pressed)
        self.ui.horizontalSlider.sliderReleased.connect(self.scale_slider_release)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.x_axis_show.stateChanged.connect(
        lambda state: self.checkb_state_changed(state, "axis_x", "show"))
        self.ui.y_axis_show.stateChanged.connect(
        lambda state: self.checkb_state_changed(state, "axis_y", "show"))
        self.ui.grid_show.stateChanged.connect(
        lambda state: self.checkb_state_changed(state, "grid", "show"))
        self.ui.pb_add_function.clicked.connect(self.pb_add_function_clicked)
        self.ui.pb_copy_tikzpicture.clicked.connect(self.pb_copy_tikzpicture_clicked)
        self.ui.pb_copy_document.clicked.connect(self.pb_copy_document_clicked)
        self.ui.checkb_autocompile.stateChanged.connect(self.checkb_autocompile_stateChanged)
        self.ui.checkb_autocompile.setChecked(True)
        self.ui.checkb_canvas_always_on.stateChanged.connect(self.checkb_canvas_always_on_stateChanged)
        self.ui.checkb_canvas_always_on.setChecked(False)
        self.ui.checkb_show_pdf.stateChanged.connect(self.checkb_show_pdf_state_changed)
        self.ui.checkb_show_pdf.setChecked(True)

        # self.scene.compile_tkz_and_render()
        cd.empty_jpg(PIXELS, PIXELS)
        browser_text = soj.eucl2tkz(self.scene.eucl, self.scene.left_bottom_scale())
        browser_text = syntax_highlight(browser_text)
        self.scene.textBrowser.setText(browser_text)
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
        self.show()

    def axis_grid_checkbox_shifter(self):
        if self.scene.eucl["axis_x"]["show"]:
            self.ui.x_axis_show.setChecked(True)
        else:
            self.ui.x_axis_show.setChecked(False)
        if self.scene.eucl["axis_y"]["show"]:
            self.ui.y_axis_show.setChecked(True)
        else:
            self.ui.y_axis_show.setChecked(False)
        if self.scene.eucl["grid"]["show"]:
            self.ui.grid_show.setChecked(True)
        else:
            self.ui.grid_show.setChecked(False)


    def keyPressEvent(self,event):
        # performs autocompile when f5 is pressed
        if event.matches(QtGui.QKeySequence.Refresh):
            previous_autocompile = self.scene.autocompile
            self.scene.autocompile = True
            self.scene.compile_tkz_and_render()
            self.scene.autocompile = previous_autocompile

    def combobox_point_change(self, i):
        self.point_index = i
        if self.current_tool == POINT:
            self.current_mode = 100*self.current_tool+i
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def combobox_line_change(self, i):
        self.line_index = i
        if self.current_tool == SEGMENT:
            self.current_mode = 100*self.current_tool+i
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def combobox_circle_change(self, i):
        self.circle_index = i
        if self.current_tool == CIRCLE:
            self.current_mode = 100*self.current_tool+i
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def combobox_move_change(self, i):
        self.move_index = i
        if self.current_tool == MOVE:
            self.current_mode = 100*self.current_tool+i
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def combobox_decorator_change(self, i):
        self.decorator_index = i
        if self.current_tool == DECORATOR:
            self.current_mode = 100*self.current_tool+i
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def radiobutton_triggered(self):
        self.current_tool = POINT
        self.current_mode = 100*self.current_tool+self.point_index
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def radiobutton_triggered_2(self):
        self.current_tool = SEGMENT
        self.current_mode = 100*self.current_tool+self.line_index
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def radiobutton_triggered_3(self):
        self.current_tool = CIRCLE
        self.current_mode = 100*self.current_tool+self.circle_index
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def radiobutton_triggered_4(self):
        self.current_tool = MOVE
        self.current_mode = 100*self.current_tool+self.move_index
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def radiobutton_triggered_5(self):
        self.current_tool = DECORATOR
        self.current_mode = 100*self.current_tool+self.decorator_index
        self.scene.get_current_mode(self.current_mode)
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def save_into_file(self):
        if self.scene.save_state.opened_file is None:
            fname = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption="Save file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
            if fname[0] != '':
                self.scene.save_state = save_state(fname[0], False)
        if fname[0] != '':
            soj.save_eucl_file(fname[0], self.scene.eucl)
            self.scene.actionSave.setEnabled(False)
    def save(self):
        if self.scene.save_state.opened_file is not None:
            soj.save_eucl_file(self.scene.save_state.opened_file, self.scene.eucl)
            self.scene.actionSave.setEnabled(False)
        else:
            self.save_into_file()
    def open_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption="Open a file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
        if fname[0] != '':
            self.scene.eucl = soj.read_eucl_file(fname[0])
            compute_mapped_points(self.scene)
            compile_tkz_and_render(self.scene)
            add_new_undo_item(self.scene)
            cd.always_on_drawing_plan(self.scene)
            cd.always_off_drawing_plan(self.scene)
            self.axis_grid_checkbox_shifter()
            self.scene.save_state = save_state(fname[0], False)

    def new_file(self):
        cd.empty_jpg(PIXELS, PIXELS)
        self.scene.eucl = soj.new_eucl_file()
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
        previous_autocompile = self.scene.autocompile
        self.scene.autocompile = False
        compile_tkz_and_render(self.scene)
        self.scene.autocompile = previous_autocompile
        add_new_undo_item(self.scene)

        self.axis_grid_checkbox_shifter()


    def scale_slider_move(self, value):
        old_left, old_bottom, old_scale = self.scene.zoom_new_window_params
        self.scene.eucl["window"]["scale"] = old_scale * (value+512+0.5)/512
        scale = self.scene.eucl["window"]["scale"]
        self.scene.eucl["window"]["left"] = old_left - 5 * (scale-old_scale)
        self.scene.eucl["window"]["bottom"] = old_bottom - 5 * (scale-old_scale)
        compute_mapped_points(self.scene)
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
        self.scene.selected_objects.clear()
        cd.add_all_items_to_scene(self.scene, QtCore.Qt.darkMagenta)
    def scale_slider_pressed(self):
        self.scene.zoom_new_window_params = self.scene.left_bottom_scale()
    def scale_slider_release(self):
        self.horizontalSlider.setValue(0)
        self.zoom_new_window_params = [0,0,0]
        self.scene.selected_objects.clear()
        compile_tkz_and_render(self.scene)
        compute_mapped_points(self.scene)
        add_new_undo_item(self.scene)
    def undo(self):
        if len(self.scene.undo_history) > 1:
            self.scene.eucl = deepcopy(self.scene.undo_history[-2])
            self.scene.redo_history.append(self.scene.undo_history.pop())
            self.scene.selected_objects.clear()
            compute_mapped_points(self.scene)
            compile_tkz_and_render(self.scene)
            if len(self.scene.undo_history) == 1:
                self.ui.actionUndo.setEnabled(False)
            self.ui.actionRedo.setEnabled(True)
            self.axis_grid_checkbox_shifter()

    def redo(self):
        if self.scene.redo_history != []:
            self.scene.eucl = deepcopy(self.scene.redo_history[-1])
            self.scene.undo_history.append(self.scene.redo_history.pop())
            self.scene.selected_objects.clear()
            compute_mapped_points(self.scene)
            compile_tkz_and_render(self.scene)
            if self.scene.redo_history == []:
                self.ui.actionRedo.setEnabled(False)
            self.ui.actionUndo.setEnabled(True)
            self.axis_grid_checkbox_shifter()

    def checkb_state_changed(self, state, property, secondary_property=None):
        if secondary_property is None:
            item = self.scene.eucl
            my_property = property
        else:
            item = self.scene.eucl[property]
            my_property = secondary_property

        if state == QtCore.Qt.Unchecked and item[my_property] == True:
            item[my_property] = False
            self.scene.selected_objects.clear()
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()
        elif state == QtCore.Qt.Checked and item[my_property] == False:
            item[my_property] = True
            self.scene.selected_objects.clear()
            self.scene.compile_tkz_and_render()
            self.scene.add_new_undo_item()

    def pb_add_function_clicked(self):
        dialog = AddFunctionDialog(self.scene)
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def pb_copy_tikzpicture_clicked(self):
        copy_to_clipboard(soj.eucl2tkz(self.scene.eucl, self.scene.left_bottom_scale()))
    def pb_copy_document_clicked(self):
        tikzpicture_string = soj.eucl2tkz(self.scene.eucl, self.scene.left_bottom_scale())
        copy_to_clipboard(soj.tkz2tex(self.scene.eucl, tikzpicture_string))

    def checkb_autocompile_stateChanged(self, state):
        if state == QtCore.Qt.Unchecked:
            self.scene.autocompile = False
        else:
            self.scene.autocompile = True
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)


    def checkb_canvas_always_on_stateChanged(self, state):
        if state == QtCore.Qt.Unchecked:
            self.scene.canvas_always_on = False
        else:
            self.scene.canvas_always_on = True
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)

    def checkb_show_pdf_state_changed(self, state):
        if state == QtCore.Qt.Unchecked:
            self.scene.show_pdf = False
        else:
            self.scene.show_pdf = True
        self.scene.selected_objects.clear()
        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)


# class for the function pop-up window
class AddFunctionDialog(QtWidgets.QDialog):
    def __init__(self, scene):
        super(AddFunctionDialog, self).__init__()
        self.ui = uic.loadUi('layouts/function_dialog.ui', self)
        self.setWindowTitle("Add function")
        self.scene = scene
        self.function_type = YFX_FUNCTION
        self.function = ''
        self.start = ''
        self.end = ''
        self.ui.radioButton.clicked.connect(self.rad_yfx)
        self.ui.radioButton_2.clicked.connect(self.rad_polar)
        self.ui.radioButton_3.clicked.connect(self.rad_parametric)
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)
        self.ui.textEdit.textChanged.connect(self.le_function_editing_finished)
        self.ui.lineEdit.editingFinished.connect(self.le_start_editing_finished)
        self.ui.lineEdit_2.editingFinished.connect(self.le_end_editing_finished)

    def rad_yfx(self):
        self.function_type = YFX_FUNCTION
    def rad_polar(self):
        self.function_type = POLAR_FUNCTION
    def rad_parametric(self):
        self.function_type = PARAMETRIC_FUNCTION
    def accepted(self):
        soj.register_new_function(self.scene.eucl, [self.function, self.start, self.end], setup=self.function_type)
        self.scene.add_new_undo_item()
        self.scene.compile_tkz_and_render()
    def rejected(self):
        pass

    def le_function_editing_finished(self):
        self.function = self.ui.textEdit.toPlainText()
    def le_start_editing_finished(self):
        self.start = self.ui.lineEdit.text()
    def le_end_editing_finished(self):
        self.end = self.ui.lineEdit_2.text()

# class for the function pop-up window
class PointOnLineDialog(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(PointOnLineDialog, self).__init__()
        self.ui = uic.loadUi('layouts/point_on_line_dialog.ui', self)
        self.setWindowTitle("Enter ratio")
        self.scene = scene
        self.ratio = ""
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)
        self.ui.lineEdit.editingFinished.connect(self.le_editing_finished)

    def le_editing_finished(self):
        self.ratio = self.ui.lineEdit.text()

    def accepted(self):
        soj.register_new_point(self.scene.eucl, self.data + [self.ratio], setup=POINT_ON_LINE)
        #self.scene.add_new_undo_item()
        #self.scene.compile_tkz_and_render()
        self.scene.compute_mapped_points()
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.scene.selected_objects.clear()

        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def rejected(self):
        pass

    def le_function_editing_finished(self):
        self.function = self.ui.textEdit.toPlainText()
    def le_start_editing_finished(self):
        self.start = self.ui.lineEdit.text()
    def le_end_editing_finished(self):
        self.end = self.ui.lineEdit_2.text()

# class for the function pop-up window
class PointOnCircleDialog(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(PointOnCircleDialog, self).__init__()
        self.ui = uic.loadUi('layouts/point_on_circle_dialog.ui', self)
        self.setWindowTitle("Enter angle")
        self.scene = scene
        self.angle = ""
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)
        self.ui.lineEdit.editingFinished.connect(self.le_editing_finished)

    def le_editing_finished(self):
        self.angle = self.ui.lineEdit.text()

    def accepted(self):
        soj.register_new_point(self.scene.eucl, self.data + [self.angle], setup=POINT_ON_CIRCLE)
        #self.scene.add_new_undo_item()
        #self.scene.compile_tkz_and_render()
        self.scene.compute_mapped_points()
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.scene.selected_objects.clear()

        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def rejected(self):
        pass

    def le_function_editing_finished(self):
        self.function = self.ui.textEdit.toPlainText()
    def le_start_editing_finished(self):
        self.start = self.ui.lineEdit.text()
    def le_end_editing_finished(self):
        self.end = self.ui.lineEdit_2.text()


# class for the function pop-up window
class PointRotated(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(PointRotated, self).__init__()
        self.ui = uic.loadUi('layouts/point_rotate_dialog.ui', self)
        self.setWindowTitle("Enter angle")
        self.scene = scene
        self.angle = ""
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)
        self.ui.lineEdit.editingFinished.connect(self.le_editing_finished)

    def le_editing_finished(self):
        self.angle = self.ui.lineEdit.text()

    def accepted(self):
        soj.register_new_point(self.scene.eucl, self.data + [self.angle], setup=ROTATION)
        #self.scene.add_new_undo_item()
        #self.scene.compile_tkz_and_render()
        self.scene.compute_mapped_points()
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.scene.selected_objects.clear()

        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def rejected(self):
        pass

    def le_function_editing_finished(self):
        self.function = self.ui.textEdit.toPlainText()
    def le_start_editing_finished(self):
        self.start = self.ui.lineEdit.text()
    def le_end_editing_finished(self):
        self.end = self.ui.lineEdit_2.text()


# class for the function pop-up window
class MakeGridDialog(QtWidgets.QDialog):
    def __init__(self, scene, data):
        super(MakeGridDialog, self).__init__()
        self.ui = uic.loadUi('layouts/make_grid_dialog.ui', self)
        self.setWindowTitle("Enter grid parameters")
        self.scene = scene
        self.rows = 1
        self.cols = 1
        self.data = data
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.rejected.connect(self.rejected)

        self.ui.hslider_col.valueChanged.connect(self.hslider_col_func)
        self.ui.hslider_row.valueChanged.connect(self.hslider_row_func)


    def hslider_col_func(self, value):
        self.cols = value
        self.ui.col_label.setText(str(value))

    def hslider_row_func(self, value):
        self.rows = value
        self.ui.row_label.setText(str(value))


    def accepted(self):
        origin, right, bottom = self.data
        x, y = right, bottom
        for j in range(self.rows):
            for i in range(self.cols-1):
                if j == i == 0:
                    continue
                next_name = soj.first_disengaged_name(self.scene.eucl, "upper")
                soj.register_new_point(self.scene.eucl, [origin, right, x], setup=TRANSLATION)
                x = next_name

            if (j != self.rows - 1) and (j != 0):
                next_name = soj.first_disengaged_name(self.scene.eucl, "upper")
                soj.register_new_point(self.scene.eucl, [origin, bottom, y], setup=TRANSLATION)
                y = next_name
            x = y


        #self.scene.add_new_undo_item()
        #self.scene.compile_tkz_and_render()
        self.scene.compute_mapped_points()
        self.scene.compile_tkz_and_render()
        self.scene.add_new_undo_item()
        self.scene.selected_objects.clear()

        cd.always_on_drawing_plan(self.scene)
        cd.always_off_drawing_plan(self.scene)
    def rejected(self):
        pass


# the function for the main
def main():
    app = QtWidgets.QApplication(sys.argv)
    eucl_main_window = EuclMainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
