# standard and pip imports
import sys, os, json
import numpy as np
import json
from PyQt5 import QtCore, QtWidgets, QtGui
from collections import namedtuple
from copy import deepcopy

from Dialog.HelpDialog import HelpDialog
from Dialog.MakeGridDialog import MakeGridDialog
from Dialog.PointRotated import PointRotated
from Dialog.PointOnCircleDialog import PointOnCircleDialog
from Dialog.PointOnLineDialog import PointOnLineDialog
import AddNewItem
import EuclMath
import Properties
from Constants import *
import CanvasDrawing as cd
from Utils import canvascoord2tkzcoord, tkzcoord2canvascoord
from SyntaxHighlight import syntax_highlight

save_state = namedtuple('save_state', 'opened_file unsaved_progress')


def compile_tkz_and_render(scene):
    """
    SUMMARY
        performs pdflatex command if in autocompile mode, and updates canvas
        and highlighted tikz code accordingly

    PARAMETERS
        scene: graphicsScene (modifies scene!)

    RETURNS
        None
    """
    with open('settings.json') as f:
        settings = json.load(f)
    LATEX_COMMAND = settings["latex"]
    PDF_TO_JPG = settings["pdf to jpg"].replace('$PIXELSX', str(int(scene.width())))
    PDF_TO_JPG = PDF_TO_JPG.replace('$PIXELSY', str(int(scene.height())))

    #0 BEGIN save current work directory and change to tmp folder,
    # also make tmp folder if does not exist
    current_dir = os.getcwd()
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    os.chdir(current_dir + "/tmp")
    #0 END

    #1 BEGIN: generate latex code, write into file
    write_file = open('temp.tex', "w")
    tikz_text = AddNewItem.eucl2tkz(scene.eucl, scene.left_bottom_scale(), width_height=(scene.width(), scene.height()))
    text_to_write = AddNewItem.tkz2tex(scene.eucl, tikz_text)
    write_file.write(text_to_write)
    write_file.close()
    #1 END

    #2 BEGIN: make syntax highlight, update TikZ source code in the window
    browser_text = syntax_highlight(tikz_text)
    scene.textBrowser.setText(browser_text)
    #2 END

    # run compile with pdflatex, convert into jpg, move back to original directory
    if scene.autocompile:
        scene.textBrowser_pdflatex.setText('Process started: ' + LATEX_COMMAND)
        scene.textBrowser_pdflatex.repaint()
        os.system(LATEX_COMMAND)
        os.system(PDF_TO_JPG)

    #4 BEGIN: adds log text in the main window text browser
    try:
        f = open('temp.log', 'r')
    except:
        f = open('temp.log', 'w')
        f.close()

    with open('temp.log', 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
    escape = False
    for i, line in enumerate(lines):
        try:
            if line[0] == '!':
                escape = True
                scene.textBrowser_pdflatex.setText(
                    'Process started: ' + LATEX_COMMAND + '\Process exited with error(s)\n' + '\n'.join([line, lines[i+1], lines[i+2]]))
        except: pass
        if escape: break
    else:
        scene.textBrowser_pdflatex.setText(
            'Process started: ' + LATEX_COMMAND + '\nProcess exited normally.')
    #4 END


    os.chdir(current_dir)

    #5 BEGIN: remove redundant leftover files from Gnuplot
    # directory = os.path.realpath(__file__)[:-len(__file__)]
    # for item in os.listdir(directory):
    #     if item.endswith(".gnuplot") or item.endswith(".table"):
    #         os.remove(os.path.join(directory, item))
    #5 END

    #6 BEGIN: draw canvas objects if "always on" or "always off" accordingly
    cd.always_on_drawing_plan(scene)
    cd.always_off_drawing_plan(scene)
    #6 END


# finds all points by coordinate on the canvas
def compute_mapped_points(scene, focus_pt_coords=None):
    """
    SUMMARY
        finds the position of all points on the canvas plane

    PARAMETERS
        scene: graphicsScene (scene.mapped_points is modified!)
        focus_pt_coords: if one point is in focus, we pass its coordinates,
            otherwise we pass None

    RETURNS
        None
    """
    mapped_points = {} # dictionary: key is point id, value is a coordinate tuple
    mapped_points['pt_default'] = (0,0)
    num_points = len(scene.eucl["points"])

    # some points depend on the coordinates of other points, one run of this while's
    # body adds exactly one new point to <mapped_points>
    # we always condition the addition of a new point on the inclusion of its prerequisites
    # in <mapped_points>
    while len(mapped_points) < num_points:
        for point in scene.eucl["points"]:
            if point["id"] in mapped_points:
                continue

            # if there is a focused point, we replace its coordinate with focus_pt_coords
            if focus_pt_coords is not None and point["id"] == scene.focused_point_id:
                x,y = focus_pt_coords
                coords = canvascoord2tkzcoord(x, y, scene.left_bottom_scale(), scene.width(), scene.height())
                mapped_points[scene.focused_point_id] = [float(coords[0]), float(coords[1])]
            elif point["from"]["type"] == "free":
                # x and y coordinates can be python/numpy expressions hence the eval
                mapped_points[point["id"]] = [eval(point["x"]), eval(point["y"])]
            elif point["from"]["type"] == "intersection_ll":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    if point["from"]["C"] in mapped_points and point["from"]["D"] in mapped_points:
                        A_ = mapped_points[point["from"]["A"]]
                        B_ = mapped_points[point["from"]["B"]]
                        C_ = mapped_points[point["from"]["C"]]
                        D_ = mapped_points[point["from"]["D"]]
                        inter_coords = EuclMath.ll_intersection(A_,B_,C_,D_)
                        mapped_points[point["id"]] = inter_coords
            elif point["from"]["type"] == "intersection_lc":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    for pt in scene.eucl["points"]:
                        if pt["from"]["type"] == "intersection_lc" and pt["id"] != point["id"] and pt["from"]["lc_id"] == point["from"]["lc_id"]:
                            circle = AddNewItem.get_item_from_id(scene.eucl, point["from"]["circle"], 'c')
                            if circle["type"] == "two_point_circle":
                                if circle["points"]["O"] in mapped_points and circle["points"]["A"] in mapped_points:
                                    centre = mapped_points[circle["points"]["O"]]
                                    circ_A = mapped_points[circle["points"]["A"]]
                                    pt_A = mapped_points[point["from"]["A"]]
                                    pt_B = mapped_points[point["from"]["B"]]
                                    radius = np.linalg.norm(np.array(centre)-np.array(circ_A))
                                    coords, reverse_intersections = EuclMath.lc_intersection(centre, radius, pt_A, pt_B)
                            if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                                if circle["points"]["A"] in mapped_points and circle["points"]["B"] in mapped_points and\
                                   circle["points"]["C"] in mapped_points:
                                    circ_A = mapped_points[circle["points"]["A"]]
                                    circ_B = mapped_points[circle["points"]["B"]]
                                    circ_C = mapped_points[circle["points"]["C"]]
                                    if circle["type"] == "circum_circle":
                                        centre, radius = EuclMath.circum_centre_and_radius(circ_A, circ_B, circ_C)
                                    else:
                                        centre, radius = EuclMath.in_centre_and_radius(circ_A, circ_B, circ_C)
                                    pt_A = mapped_points[point["from"]["A"]]
                                    pt_B = mapped_points[point["from"]["B"]]
                                    coords, reverse_intersections = EuclMath.lc_intersection(centre, radius, pt_A, pt_B)
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
                circle = AddNewItem.get_item_from_id(scene.eucl, circle_id, 'c')
                if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        A_ = mapped_points[circle["points"]["A"]]
                        B_ = mapped_points[circle["points"]["B"]]
                        C_ = mapped_points[circle["points"]["C"]]
                        if circle["type"] == "circum_circle":
                            centre = EuclMath.circumcentre(A_,B_,C_)
                        else:
                            centre = EuclMath.incentre(A_,B_,C_)
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
                circle = AddNewItem.get_item_from_id(scene.eucl, circle_id, 'c')
                if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        A_ = mapped_points[circle["points"]["A"]]
                        B_ = mapped_points[circle["points"]["B"]]
                        C_ = mapped_points[circle["points"]["C"]]
                        if circle["type"] == "circum_circle":
                            centre, radius = EuclMath.circum_centre_and_radius(A_,B_,C_)
                        elif circle["type"] == "inscribed_circle":
                            centre, radius = EuclMath.in_centre_and_radius(A_,B_,C_)
                else:
                    O = mapped_points[circle["points"]["O"]]
                    A = mapped_points[circle["points"]["A"]]
                    centre, radius = O, np.sqrt((O[0]-A[0])**2 + (O[1]-A[1])**2)

                mapped_points[point["id"]] = [centre[0] + radius * np.cos(np.radians(eval(point["from"]["angle"]))),
                                              centre[1] + radius * np.sin(np.radians(eval(point["from"]["angle"])))]
            elif point["from"]["type"] == "projection_point":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points and\
                   point["from"]["P"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    P = mapped_points[point["from"]["P"]]
                    projection_point = EuclMath.orthogonal_projection(A,B,P)
                    mapped_points[point["id"]] = projection_point
            elif point["from"]["type"] == "bisector_point":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points and\
                   point["from"]["C"] in mapped_points:
                    A = mapped_points[point["from"]["A"]]
                    B = mapped_points[point["from"]["B"]]
                    C = mapped_points[point["from"]["C"]]
                    bisector_point = EuclMath.bisector_point(A,B,C)
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

    # converts all TikZ coordinates to canvas coordinates
    for key, value in mapped_points.items():
        mapped_points[key] = tkzcoord2canvascoord(str(value[0]), str(value[1]), scene.left_bottom_scale(), scene.width(), scene.height())
    scene.mapped_points = mapped_points


# when undo is pressed, adds extra undo elements to the undo's list
def add_new_undo_item(scene):
    """
    SUMMARY
        executes all the necessary steps to successfully add an undo point

    PARAMETERS
        scene: graphicsScene (modifies scene!)

    RETURNS
        None
    """

    scene.save_state = save_state(scene.save_state.opened_file, scene.save_state.unsaved_progress + 1)
    scene.undo_history.append(deepcopy(scene.eucl))
    scene.redo_history.clear()
    scene.actionUndo.setEnabled(True)
    scene.actionRedo.setEnabled(False)
    if scene.save_state.unsaved_progress:
        scene.actionSave.setEnabled(True)
    else:
        scene.actionSave.setEnabled(False)


def __is_prefix(pref, word):
    """
    SUMMARY
        returns whether a string is prefix of another

    PARAMETERS
        pref: the string we check whether is prefix
        word: the string we search the prefix in

    RETURNS
        boolean: True if <pref> is prefix of <word> otherwise False
    """
    if word.find(pref) == 0:
        return True
    else:
        return False


def validate_selected_item(scene, item_types, poly_string=0):
    """
    SUMMARY
        checks if the types of the selected objects match the types for
        successful definition of the new object, if no match was found it clears
        the selected objects list in addition to returning values
    PARAMETERS
        scene: graphicsScene (scene.selected_objects may be modified!)
        item_types: list of strings contaning the successful object combinations
        poly_string: if we expect a polygon type object, it tells whether we
            expect 0: not polygon
                   1: linestring
                   2: closed polygon
    RETURNS
        boolean: the selection successfully found a match in the approved list
        str: the type of objects selected in order
    """
    type_sofar_ok = False
    selection_concluded = False
    concluded_item_type = ""
    for item_type in item_types:
        # this if activates if a match is found
        if __is_prefix(scene.selected_item_type_history[-1-len(scene.selected_objects):], item_type):
            type_sofar_ok = True
            scene.selected_objects.append(scene.focused_point_id)
            selected_length = len(scene.selected_objects)
            if selected_length == len(item_type):
                #nothing special
                if poly_string == 0:
                    selection_concluded = True
                    concluded_item_type = item_type
                #linestring (conditions if the last and penultimate points are the same)
                if poly_string == 1 and scene.selected_objects[-2] == scene.selected_objects[-1]:
                    selection_concluded = True
                    concluded_item_type = item_type
                #polygon (conditions if the last and first points are the same)
                if poly_string == 2 and scene.selected_objects[0] == scene.selected_objects[-1]:
                    selection_concluded = True
                    concluded_item_type = item_type
            break
    if not type_sofar_ok:
        scene.selected_objects.clear()
        cd.clear_canvas(scene)
    return (selection_concluded, concluded_item_type)




# class for the graphics scene (canvas)
class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__ (self):
        """
        SUMMARY
            contructor for GraphicsScene

        PARAMETERS
            nothing

        RETURNS
            None
        """
        super(GraphicsScene, self).__init__ ()

        self.mouse_x = 0 # x mouse position on the canvas
        self.mouse_y = 0 # y mouse position on the canvas
        self.current_mode = NEW_POINT # the type of object to be added
        self.eucl = AddNewItem.new_eucl_file() # the object-oriented data-structure to hold all info about the project
        # self.setSceneRect(0,0,rect.width(), rect.height()); # holds the scene rectangle; the bounding rectangle of the scene
        self.focused_point_id = None # id of the point with the mouse pointer over it
        self.selected_objects = [] # the objects making the current selection
        self.movePoint = False ######
        self.move_objects = [] ######
        self.mouse_being_pressed = False # False if mouse is unpressed, True if mouse being pressed
        self.mapped_points = {} # dictionary for the coordinates of all points on the canvas plane
        self.move_canvas = [False, 0, 0] # [True if MOVE_AND_SCALE_CANVAS else False, mouse_x, mouse_y]
        self.undo_history = [AddNewItem.new_eucl_file()] # undo history starts with an empty eucl
        self.redo_history = [] # redo history is empty at the start
        self.zoom_new_window_params = [0,0,0] # [left, bottom, scale]
        self.selected_item_type_history = "" # type of past selected objects "p": point, "s": segment, "c": circle
        self.autocompile = True # boolean whether autocompile is active
        self.canvas_always_on = False # boolean whether canvas always on is active
        self.change_made = False # boolean for whether an actual change has been recorded during selection
        self.show_pdf = True # boolean whether show pdf is activated
        self.aspect_ratio_indicator = False # boolean for whether the aspect ratio indicator is activated
        self.aspect_ratio = "16/9" # string for aspect ratio
        self.save_state = save_state('', False) # used to keep track of the opened file, holds info for case of later save

        # loading settings
        with open('settings.json') as f:
            self.settings = json.load(f) # settings loaded to be an attribute too

    def compile_tkz_and_render(self):
        """
        SUMMARY
            own compile_tkz_and_render for graphicsScene

        PARAMETERS
            nothing

        RETURNS
            None
        """
        compile_tkz_and_render(self)

    def compute_mapped_points(self, focus_pt_coords=None):
        """
        SUMMARY
            own compute_mapped_points for graphicsScene

        PARAMETERS
            focus_pt_coords: optional with the canvas coordinates of the point in focus

        RETURNS
            None
        """
        compute_mapped_points(self, focus_pt_coords=None)

    def add_new_undo_item(self):
        """
        SUMMARY
            own add_new_undo_item for graphicsScene

        PARAMETERS
            nothing

        RETURNS
            None
        """
        add_new_undo_item(self)


    def set_current_mode(self, current_mode):
        """
        SUMMARY
            sets the current mode to new value

        PARAMETERS
            current_mode: the new mode

        RETURNS
            integer
        """

        self.current_mode = current_mode

    def get_textBrowser(self, textBrowser):
        """
        SUMMARY
            get references for textBrowser
            need this to be able to mutate its attributes in scene

        PARAMETERS
            textBrowser: the box with the latex source code in it

        RETURNS
            None
        """
        self.textBrowser = textBrowser

    def get_textBrowser_pdflatex(self, textBrowser_pdflatex):
        """
        SUMMARY
            get references for textBrowser
            need this to be able to mutate its attributes in scene

        PARAMETERS
            textBrowser: the box with the latex source code in it

        RETURNS
            None
        """
        self.textBrowser_pdflatex = textBrowser_pdflatex

    def get_actionRedo(self, actionRedo):
        """
        SUMMARY
            get references for actionRedo
            need this to be able to mutate its attributes in scene

        PARAMETERS
            actionRedo: the redo option accessible from the menubar

        RETURNS
            None
        """
        self.actionRedo = actionRedo

    def get_actionUndo(self, actionUndo):
        """
        SUMMARY
            get references for actionUndo
            need this to be able to mutate its attributes in scene

        PARAMETERS
            actionUndo: the undo option accessible from the menubar

        RETURNS
            None
        """
        self.actionUndo = actionUndo

    def get_actionSave(self, actionSave):
        """
        SUMMARY
            get references for actionSave
            need this to be able to mutate its attributes in scene

        PARAMETERS
            actionSave: the save option accessible from the menubar

        RETURNS
            None
        """
        self.actionSave = actionSave
        self.actionSave.setEnabled(False)

    def get_actionCoordinate(self, x, y, grid):
        """
        SUMMARY
            get references for coordinate checkbuttons in menubar
            need this to be able to mutate its attributes in scene

        PARAMETERS
            x: reference to x axis checkbox
            y: reference to y axis checkbox
            z: reference to grid checkbox

        RETURNS
            None
        """
        self.actionX = x
        self.actionY = y
        self.actionGrid = grid

    def axis_grid_checkbox_shifter(self):
        """
        SUMMARY
            when called checks the project whether it has x/y axes and grid, and
            sets the corresponding checkboxes accordingly

        PARAMETERS
            nothing

        RETURNS
            None
        """
        if self.eucl["axis_x"]["show"]:
            self.actionX.setChecked(True)
        else:
            self.actionX.setChecked(False)
        if self.eucl["axis_y"]["show"]:
            self.actionY.setChecked(True)
        else:
            self.actionY.setChecked(False)
        if self.eucl["grid"]["show"]:
            self.actionGrid.setChecked(True)
        else:
            self.actionGrid.setChecked(False)

    def left_bottom_scale(self):
        """
        SUMMARY
            returns the left, bottom, scale attributes of the window

        PARAMETERS
            nothing

        RETURNS
            [float, float, float]
        """
        return [self.eucl["window"]["left"],\
                self.eucl["window"]["bottom"],\
                self.eucl["window"]["scale"]]

    def get_focused_id(self, x, y):
        """
        SUMMARY
            returns the id of the object in focus, computes which object
            should be highlighted given mouse pointer position

        PARAMETERS
            x: x coordinate of the mouse pointer
            y: y coordinate of the mouse pointer

        RETURNS
            optional (id)
        """

        focused_point_id = None
        min_circle_dist, min_segment_dist = 1000000, 1000000

        #1 BEGIN: we order the point distances from the mouse, and select the closest,
        # check if the point is close enough, if so return the id of the point
        if len(self.eucl["points"]) > 1:
            sorted_distance_to_points = []
            for point in self.eucl["points"]:
                if point["id"] != 'pt_default':
                    canvas_point = self.mapped_points[point["id"]]
                    sorted_distance_to_points.append((point, canvas_point))
            sorted_distance_to_points.sort(key=lambda z : (z[1][0]-x)**2+(z[1][1]-y)**2)
            x_point, y_point = sorted_distance_to_points[0][1]
            minimal_point = sorted_distance_to_points[0][0]
            # close enough distance check
            if (x-x_point)**2+(y-y_point)**2 <= MAX_DISTANCE_TO_HIGHLIGHT**2:
                focused_point_id = minimal_point["id"]
                return focused_point_id
        #1 END

        #2 BEGIN: we order the segment distances from the mouse, and select the closest,
        # check if the segment is close enough, if so set focused_point_id to the segment id
        if len(self.eucl["segments"]) > 1:
            sorted_distance_to_segments = []
            for segment in self.eucl["segments"]:
                if segment["id"] != 'sg_default':
                    A = self.mapped_points[segment["points"]["from"]]
                    B = self.mapped_points[segment["points"]["to"]]
                    sorted_distance_to_segments.append((segment, EuclMath.pt_segment_dist(A, B, (x,y))))
            sorted_distance_to_segments.sort(key=lambda z : z[1])

            if sorted_distance_to_segments[0][1] <= MAX_DISTANCE_TO_HIGHLIGHT:
                minimal_segment, min_segment_dist = sorted_distance_to_segments[0]
                focused_point_id = minimal_segment["id"]
        #2 END

        #3 BEGIN: we do the same with circles as segments plus comparison with
        # segment which one is closer
        if len(self.eucl["circles"]) > 1:
            sorted_distance_to_circles = []
            for circle in self.eucl["circles"]:
                if circle["id"] == 'crc_default':
                    continue
                centre, radius = cd.get_circle_centre_radius_on_canvas(self, circle["id"])
                sorted_distance_to_circles.append((circle, EuclMath.pt_circle_dist(centre, radius, (x,y))))
            sorted_distance_to_circles.sort(key=lambda z : z[1])

            if sorted_distance_to_circles[0][1] <= MAX_DISTANCE_TO_HIGHLIGHT:
                circle, min_circle_dist = sorted_distance_to_circles[0]
                if min_circle_dist < min_segment_dist:
                    focused_point_id = circle["id"]
        #3 END

        return focused_point_id


    def mousePressEvent(self, event):
        """
        SUMMARY
            inherited method from QtWidgets.QGraphicsScene

        PARAMETERS
            event: passes mouse related information

        RETURNS
            None
        """
        if event.buttons() == QtCore.Qt.LeftButton:
            #1 BEGIN: save mouse state
            self.mouse_being_pressed = True # mouse is being pressed down so set to True
            position = QtCore.QPointF(event.scenePos()) # mouse position
            self.mouse_x, self.mouse_y = (position.x(), position.y()) # x & y coordinates of the mouse
            #1 END

            self.change_made = False # boolean for storing if an edit has been recorded

            #2 BEGIN: if an object is in focus, it means we clicked on it, hence we add
            # its type to the selected_item_type_history
            if self.focused_point_id is not None:
                self.selected_item_type_history += AddNewItem.identify_item_type(self.eucl, self.focused_point_id)
            #2 END


            #3 BEGIN: big switch case through all possile modes, sets up the circumstances
            # a new object is added to the project, if everything is ok it adds it
            if self.current_mode == NEW_POINT:
                x_tkz, y_tkz = canvascoord2tkzcoord(self.mouse_x, self.mouse_y, self.left_bottom_scale(), self.width(), self.height())
                AddNewItem.register_new_point(self.eucl, [x_tkz, y_tkz], setup=NEW_POINT)
                self.change_made = True
            elif self.current_mode == SEGMENT_THROUGH:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["pp"])
                    if selection_concluded:
                        AddNewItem.register_new_line(self.eucl, self.selected_objects, setup=SEGMENT_THROUGH)
                        self.change_made = True
            elif self.current_mode == POLYGON:
                if self.focused_point_id is not None:
                    id_options = ['p'*i for i in range(3,101)]
                    selection_concluded, _ = validate_selected_item(self, id_options, 2)
                    if selection_concluded:
                        AddNewItem.register_new_polygon(self.eucl, self.selected_objects[:-1], setup=POLYGON)
                        self.change_made = True
            elif self.current_mode == LINESTRING:
                if self.focused_point_id is not None:
                    id_options = ['p'*i for i in range(3,101)]
                    selection_concluded, _ = validate_selected_item(self, id_options, 1)
                    if selection_concluded:
                        AddNewItem.register_new_polygon(self.eucl, self.selected_objects[:-1], setup=LINESTRING)
                        self.change_made = True
            elif self.current_mode == CIRCUM_CIRCLE:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_circle(self.eucl, self.selected_objects, setup=CIRCUM_CIRCLE)
                        self.change_made = True
            elif self.current_mode == TWO_POINT_CIRCLE:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["pp"])
                    if selection_concluded:
                        AddNewItem.register_new_circle(self.eucl, self.selected_objects, setup=TWO_POINT_CIRCLE)
                        self.change_made = True
            elif self.current_mode == ARC:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_circle(self.eucl, self.selected_objects, setup=ARC)
                        self.change_made = True
            elif self.current_mode == SECTOR:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_circle(self.eucl, self.selected_objects, setup=SECTOR)
                        self.change_made = True
            elif self.current_mode == INSCRIBED_CIRCLE:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_circle(self.eucl, self.selected_objects, setup=INSCRIBED_CIRCLE)
                        self.change_made = True
            elif self.current_mode == INTERSECT_POINT:
                if self.focused_point_id is not None:
                    selection_concluded, concluded_item_type = validate_selected_item(self, ["pppp", "ss", "cs", "sc", "ppc", "cpp"])
                    if selection_concluded:
                        if concluded_item_type == "pppp":
                            data = self.selected_objects
                            AddNewItem.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="pppp")
                        elif concluded_item_type == "ss":
                            segment_1 = AddNewItem.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                            segment_2 = AddNewItem.get_item_from_id(self.eucl, self.selected_objects[1], 's')
                            A, B = [segment_1["points"]["from"], segment_1["points"]["to"]]
                            C, D = [segment_2["points"]["from"], segment_2["points"]["to"]]
                            data = [A,B,C,D]
                            AddNewItem.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="pppp")
                        elif concluded_item_type in ["cs", "sc"]:
                            if concluded_item_type == "sc":
                                self.selected_objects = list(reversed(self.selected_objects))
                            segment = AddNewItem.get_item_from_id(self.eucl, self.selected_objects[1], 's')
                            A, B = [segment["points"]["from"], segment["points"]["to"]]
                            data = [self.selected_objects[0], A, B]
                            AddNewItem.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="cpp")
                        elif concluded_item_type in ["ppc", "cpp"]:
                            if concluded_item_type == "ppc":
                                self.selected_objects = list(reversed(self.selected_objects))
                            data = self.selected_objects
                            AddNewItem.register_new_point(self.eucl, data, setup=INTERSECT_POINT, conf="cpp")
                        self.change_made = True
            elif self.current_mode == MIDPOINT_CIRCLE:
                if self.focused_point_id is not None:
                    self.selected_objects.append(self.focused_point_id)
                    if len(self.selected_objects) == 1:
                        AddNewItem.register_new_point(self.eucl, self.selected_objects, setup=MIDPOINT_CIRCLE)
                        self.change_made = True
            elif self.current_mode == MIDPOINT_SEGMENT:
                if self.focused_point_id is not None:
                    selection_concluded, concluded_item_type = validate_selected_item(self, ["pp", "s"])
                    if selection_concluded:
                        if concluded_item_type == "pp":
                            data = self.selected_objects
                        elif concluded_item_type == "s":
                            segment = AddNewItem.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                            A, B = [segment["points"]["from"], segment["points"]["to"]]
                            data = [A,B]
                        AddNewItem.register_new_point(self.eucl, data, setup=MIDPOINT_SEGMENT)
                        self.change_made = True
            elif self.current_mode == ROTATION:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["pp"])
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
                            segment = AddNewItem.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                            A, B = [segment["points"]["from"], segment["points"]["to"]]
                            data = [A,B]
                        dialog = PointOnLineDialog(self, data)
                        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                        dialog.exec_()
                        self.change_made = True
            elif self.current_mode == POINT_ON_CIRCLE:
                selection_concluded, _ = validate_selected_item(self, ["c"])
                if selection_concluded:
                    data = self.selected_objects
                    dialog = PointOnCircleDialog(self, data)
                    dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                    dialog.exec_()
                    self.change_made = True
            elif self.current_mode == MAKEGRID:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        data = self.selected_objects
                        dialog = MakeGridDialog(self, data)
                        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
                        dialog.exec_()
                        self.change_made = True
            elif self.current_mode == MARK_RIGHT_ANGLE:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_angle(self.eucl, self.selected_objects, setup=MARK_RIGHT_ANGLE)
                        self.change_made = True
            elif self.current_mode == MARK_ANGLE:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_angle(self.eucl, self.selected_objects, setup=MARK_ANGLE)
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
                            segment = AddNewItem.get_item_from_id(self.eucl, self.selected_objects[0], 's')
                            A, B = [segment["points"]["from"], segment["points"]["to"]]
                            data = [A,B, self.selected_objects[1]]
                        AddNewItem.register_new_point(self.eucl, data, setup=ORTHOGONAL_PROJECTION)
                        self.change_made = True
            elif self.current_mode == BISECTOR:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_point(self.eucl, self.selected_objects, setup=BISECTOR)
                        self.change_made = True
            elif self.current_mode == TRANSLATION:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["ppp"])
                    if selection_concluded:
                        AddNewItem.register_new_point(self.eucl, self.selected_objects, setup=TRANSLATION)
                        self.change_made = True
            elif self.current_mode == ORTHOGONAL:
                if self.focused_point_id is not None:
                    selection_concluded, _ = validate_selected_item(self, ["pp"])
                    if selection_concluded:
                        AddNewItem.register_new_point(self.eucl, self.selected_objects, setup=ORTHOGONAL)
                        self.change_made = True
            elif self.current_mode == MOVE_POINT:
                self.movePoint = True
            elif self.current_mode == MOVE_AND_SCALE_CANVAS:
                self.move_canvas = [True, self.mouse_x, self.mouse_y]
            #3 END

            #4 BEGIN: compute point positions and draw objects on canvas
            self.compute_mapped_points()
            cd.always_on_drawing_plan(self)
            cd.always_off_drawing_plan(self)
            #4 END

        # if canvas is right clicked open settings
        if event.buttons() == QtCore.Qt.RightButton:
            self.open_settings()


    def open_settings(self):
        """
        SUMMARY
            brings up window of settings

        PARAMETERS
            nothing

        RETURNS
            None
        """
        dialog = Properties.PropertiesDialog(self)
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()

    def open_help(self):
        """
        SUMMARY
            brings up window of settings

        PARAMETERS
            nothing

        RETURNS
            None
        """
        dialog = HelpDialog()
        dialog.setWindowIcon(QtGui.QIcon("icon/ico.png"))
        dialog.exec_()

    def mouseMoveEvent(self, event):
        position = QtCore.QPointF(event.scenePos())
        self.mouse_x, self.mouse_y = (position.x(), position.y())
        radius = CANVAS_POINT_RADIUS

        if self.current_mode == NEW_POINT:
            cd.always_on_drawing_plan(self)
            cd.always_off_drawing_plan(self)

        if self.current_mode != NEW_POINT:
            if not self.movePoint:
                new_focused_id = self.get_focused_id(self.mouse_x, self.mouse_y)
                if new_focused_id != self.focused_point_id:
                    self.focused_point_id = new_focused_id
                    cd.always_on_drawing_plan(self)
                    cd.always_off_drawing_plan(self)
                if self.focused_point_id is None:
                    cd.always_on_drawing_plan(self)
                    cd.always_off_drawing_plan(self)
        if self.movePoint == True and self.focused_point_id is not None:
            compute_mapped_points(self, [self.mouse_x, self.mouse_y])
            cd.clear_canvas(self)
            # self.clear()
            cd.add_all_items_to_scene(self, QtCore.Qt.darkMagenta)
        if self.current_mode == MOVE_AND_SCALE_CANVAS and self.move_canvas[0] == True:
            saved_mapping = dict(self.mapped_points)
            for id in self.mapped_points:
                x_coord = self.mapped_points[id][0] + self.mouse_x - self.move_canvas[1]
                y_coord = self.mapped_points[id][1] + self.mouse_y - self.move_canvas[2]
                self.mapped_points[id] = (x_coord, y_coord)
            cd.clear_canvas(self)
            # self.clear()
            cd.add_all_items_to_scene(self, QtCore.Qt.darkMagenta)
            self.mapped_points = saved_mapping


    def mouseReleaseEvent(self, event):
        self.mouse_being_pressed = False
        position = QtCore.QPointF(event.scenePos())
        self.mouse_x, self.mouse_y = (position.x(), position.y())

        if self.current_mode == MOVE_POINT and self.focused_point_id is not None:
            for i,point in enumerate(self.eucl["points"]):
                if point["id"] == self.focused_point_id:
                    x_point, y_point = canvascoord2tkzcoord(self.mouse_x, self.mouse_y, self.left_bottom_scale(), self.width(), self.height())
                    self.eucl["points"][i]["x"] = x_point
                    point["y"] = y_point
                    break

            compile_tkz_and_render(self)
            add_new_undo_item(self)
        self.movePoint = False

        if self.current_mode == MOVE_AND_SCALE_CANVAS and self.move_canvas[0] == True:
            for id in self.mapped_points:
                x_coord = self.mapped_points[id][0] + self.mouse_x - self.move_canvas[1]
                y_coord = self.mapped_points[id][1] + self.mouse_y - self.move_canvas[2]
                self.mapped_points[id] = (x_coord, y_coord)
            from_x, from_y = (self.move_canvas[1], self.move_canvas[2])
            self.move_canvas = [False, 0, 0]
            scale = self.eucl["window"]["scale"]
            dx = (from_x-self.mouse_x) * 10 * (scale / INITIAL_GRAPHICSVIEW_SIZE[0])
            dy = (from_y-self.mouse_y) * 10 * (scale / INITIAL_GRAPHICSVIEW_SIZE[1])
            self.eucl["window"]["left"] += dx
            self.eucl["window"]["bottom"] -= dy
            compile_tkz_and_render(self)
            add_new_undo_item(self)

        if self.change_made:
            self.change_made = False
            self.compile_tkz_and_render()
            self.compute_mapped_points()
            add_new_undo_item(self)
            self.selected_objects.clear()

        cd.always_on_drawing_plan(self)
        cd.always_off_drawing_plan(self)
