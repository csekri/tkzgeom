import json, sys, string
import numpy as np
from TikZMaker import eucl2tkz, tkz2tex
from Constants import *

def draw_random_number():
    return np.random.randint(1000, 9999)


def get_item_from_id(eucl, id, type):
    if type == "p":
        for point in eucl["points"]:
            if point["id"] == id:
                return point
    elif type == "s":
        for segment in eucl["segments"]:
            if segment["id"] == id:
                return segment
    elif type == "c":
        for circle in eucl["circles"]:
            if circle["id"] == id:
                return circle
    elif type == "f":
        for function in eucl["functions"]:
            if function["id"] == id:
                return function
    else:
        sys.exit('Item type unknown.')


def identify_item_type(eucl, id):
    for point in eucl["points"]:
        if point["id"] == id:
            return "p"
    for segment in eucl["segments"]:
        if segment["id"] == id:
            return "s"
    for circle in eucl["circles"]:
        if circle["id"] == id:
            return "c"
    for function in eucl["functions"]:
        if function["id"] == id:
            return "f"


def get_geometric_alphabet(depth, case="upper"):
    if case == "upper":
        temp_alphabet = string.ascii_uppercase
    elif case == "lower":
        temp_alphabet = string.ascii_lowercase

    geometric_alphabet = []
    for i in range(depth):
        geometric_alphabet += temp_alphabet
        temp_alphabet = list(map(lambda x: x+"'", temp_alphabet))
    return geometric_alphabet

upper_alphabet = get_geometric_alphabet(100, case="upper")
lower_alphabet = get_geometric_alphabet(100, case="lower")
junk_alphabet = list(map(lambda x : "junk"+x, lower_alphabet))



def new_eucl_file():
    eucl = {}
    eucl["window"] = {}
    eucl["window"]["left"] = -5
    eucl["window"]["bottom"] = -5
    eucl["window"]["scale"] = 1

    eucl["packages"] = []
    eucl["packages"].append('\\usepackage{amsmath,amssymb}')
    eucl["packages"].append('\\usepackage[utf8]{inputenc}')
    eucl["packages"].append('\\usepackage[T1]{fontenc}')
    eucl["packages"].append('\\usepackage{tkz-euclide,tkz-fct}')
    eucl["packages"].append('\\usetikzlibrary{arrows.meta, patterns.meta, hobby, ducks}')
    eucl["packages"].append('\\usetikzlibrary{backgrounds, decorations.pathmorphing, calc}')

    eucl["code_before"] = ''
    eucl["code_after"] = ''
    eucl["bg_colour_name"] = 'none'
    eucl["bg_colour_strength"] = 100

    eucl["axis_x"] = {}
    eucl["axis_x"]["show"] = False
    eucl["axis_x"]["labels"] = {}
    eucl["axis_x"]["labels"]["show"] = True
    eucl["axis_x"]["label"] = {}
    eucl["axis_x"]["label"]["text"] = '$x$'
    eucl["axis_x"]["label"]["anchor"] = 'below'
    eucl["axis_x"]["label"]["distance"] = DEFAULT_ANCHOR_DISTANCE
    eucl["axis_x"]["o_arrow"] = {}
    eucl["axis_x"]["o_arrow"]["tip"] = DEFAULT_AXIS_ARROW_TIP
    eucl["axis_x"]["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
    eucl["axis_x"]["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
    eucl["axis_x"]["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
    eucl["axis_x"]["o_arrow"]["reversed"] = False
    eucl["axis_x"]["o_arrow"]["direction"] = True
    eucl["axis_x"]["is_tick"] = True
    eucl["axis_x"]["is_numprint"] = True
    eucl["axis_x"]["is_orig"] = False
    eucl["axis_x"]["trig"] = 0
    eucl["axis_x"]["frac"] = 0
    eucl["axis_x"]["tick_up"] = 1.0
    eucl["axis_x"]["tick_down"] = 1.0
    eucl["axis_x"]["tick_width"] = 0.8

    eucl["axis_y"] = {}
    eucl["axis_y"]["show"] = False
    eucl["axis_y"]["labels"] = {}
    eucl["axis_y"]["labels"]["show"] = True
    eucl["axis_y"]["label"] = {}
    eucl["axis_y"]["label"]["text"] = '$y$'
    eucl["axis_y"]["label"]["anchor"] = 'left'
    eucl["axis_y"]["label"]["distance"] = DEFAULT_ANCHOR_DISTANCE
    eucl["axis_y"]["o_arrow"] = {}
    eucl["axis_y"]["o_arrow"]["tip"] = DEFAULT_AXIS_ARROW_TIP
    eucl["axis_y"]["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
    eucl["axis_y"]["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
    eucl["axis_y"]["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
    eucl["axis_y"]["o_arrow"]["reversed"] = False
    eucl["axis_y"]["o_arrow"]["direction"] = True
    eucl["axis_y"]["is_tick"] = True
    eucl["axis_y"]["is_numprint"] = True
    eucl["axis_y"]["is_orig"] = False
    eucl["axis_y"]["trig"] = 0
    eucl["axis_y"]["frac"] = 0
    eucl["axis_y"]["tick_up"] = 1.0
    eucl["axis_y"]["tick_down"] = 1.0
    eucl["axis_y"]["tick_width"] = 0.8


    eucl["axis"] = {}
    eucl["axis"]["line_width"] = DEFAULT_POINT_LINE_WIDTH
    eucl["axis"]["line_colour_name"] = DEFAULT_POINT_LINE_COLOUR_NAME
    eucl["axis"]["line_strength"] = DEFAULT_POINT_LINE_STRENGTH
    eucl["axis"]["labels"] = {}
    eucl["axis"]["labels"]["show"] = ''
    eucl["axis"]["labels"]["size"] = ''
    eucl["axis"]["labels"]["colour"] = DEFAULT_POINT_LINE_COLOUR_NAME
    eucl["axis"]["labels"]["x_rotate"] = 0
    eucl["axis"]["labels"]["x_below"] = 0


    eucl["grid"] = {}
    eucl["grid"]["show"] = False
    eucl["grid"]["sub_x"] = 1
    eucl["grid"]["sub_y"] = 1
    eucl["grid"]["line_width"] = DEFAULT_SEGMENT_LINE_WIDTH
    eucl["grid"]["line_colour_name"] = 'teal'
    eucl["grid"]["line_opacity"] = DEFAULT_POINT_LINE_OPACITY
    eucl["grid"]["colour"] = 'teal'
    eucl["grid"]["line_stroke"] = DEFAULT_POINT_LINE_STROKE
    eucl["grid"]["line_stroke_custom"] = DEFAULT_POINT_LINE_STROKE_CUSTOM
    eucl["grid"]["sub_line_stroke"] = DEFAULT_SEGMENT_LINE_STROKE
    eucl["grid"]["sub_line_stroke_custom"] = DEFAULT_SEGMENT_LINE_STROKE_CUSTOM



    eucl["points"] = []
    eucl["segments"] = []
    eucl["circles"] = []
    eucl["angles"] = []
    eucl["polygons"] = []
    eucl["functions"] = []


    register_new_point(eucl, [0,0])
    eucl["points"][0]["id"] = 'pt_default'
    eucl["points"][0]["label"]["text"] = ''
    eucl["points"][0]["show"] = True
    eucl["points"][0]["label"]["show"] = True
    eucl["points"][0]["duck"]["show"] = False

    register_new_line(eucl, ['',''])
    eucl["segments"][0]["id"] = 'sg_default'
    eucl["segments"][0]["label"]["text"] = ''
    eucl["segments"][0]["show"] = True
    eucl["segments"][0]["label"]["show"] = False

    register_new_circle(eucl, ['', '', ''])
    eucl["circles"][0]["id"] = 'crc_default'
    eucl["circles"][0]["show"] = True
    eucl["circles"][0]["type"] = 'default'

    register_new_angle(eucl, ['','',''])
    eucl["angles"][0]["id"] = 'ang_default'
    eucl["angles"][0]["label"]["text"] = ''
    eucl["angles"][0]["show"] = True
    eucl["angles"][0]["label"]["show"] = False

    register_new_polygon(eucl, ['',''])
    eucl["polygons"][0]["id"] = 'pol_default'
    eucl["polygons"][0]["show"] = True

    register_new_function(eucl, ['','0', '1'])
    eucl["functions"][0]["id"] = 'fct_default'
    eucl["functions"][0]["show"] = True

    return eucl


def point_name_set(eucl):
    name_set = []
    for point in eucl["points"]:
        name_set.append(point['id'])
    return name_set

def first_disengaged_name(eucl, alpha="upper"):
    if alpha == "upper":
        for letter in upper_alphabet:
            if letter not in point_name_set(eucl):
                return letter
    if alpha == "lower":
        for letter in lower_alphabet:
            if letter not in point_name_set(eucl):
                return letter
    if alpha == "junk":
        for letter in junk_alphabet:
            if letter not in point_name_set(eucl):
                return letter

def add_label(point, eucl, alpha="upper"):
    letter = first_disengaged_name(eucl, alpha)
    point["id"] = letter
    point["label"] = {}
    point["label"]["show"] = True
    point["label"]["angle"] = DEFAULT_POINT_LABEL_ANGLE
    point["label"]["distance"] = DEFAULT_POINT_LABEL_DISTANCE
    point["label"]["text"] = '$' + letter + '$'
    point["label"]["anchor"] = DEFAULT_POINT_LABEL_ANCHOR

def add_common_default_point_data(point, eucl, alpha='upper', coord=None):
    if coord is None:
        point["x"], point["y"] = ('0','0')
    else:
        point["x"], point["y"] = coord

    add_label(point, eucl, alpha)
    point["size"] = DEFAULT_POINT_SIZE
    point["line_width"] = DEFAULT_POINT_LINE_WIDTH
    point["fill_colour_name"] = DEFAULT_POINT_FILL_COLOUR_NAME
    point["fill_strength"] = DEFAULT_POINT_FILL_STRENGTH
    point["fill_opacity"] = DEFAULT_POINT_FILL_OPACITY
    point["line_colour_name"] = DEFAULT_POINT_LINE_COLOUR_NAME
    point["line_strength"] = DEFAULT_POINT_LINE_STRENGTH
    point["line_opacity"] = DEFAULT_POINT_LINE_OPACITY
    point["line_stroke"] = DEFAULT_POINT_LINE_STROKE
    point["line_stroke_custom"] = DEFAULT_POINT_LINE_STROKE_CUSTOM
    point["show"] = True
    point["duck"] = {}
    point["duck"]["show"] = False
    point["duck"]["type"] = 'custom'
    point["duck"]["size"] = 0.5
    point["duck"]["body_colour"] = 'default'
    point["duck"]["special"] = 'horse'
    point["duck"]["chess"] = 'wbauer'
    point["duck"]["bill"] = 'sweet'
    point["duck"]["bill_colour"] = 'default'
    point["duck"]["clothing"] = {}
    point["duck"]["clothing"]["show"] = False
    point["duck"]["clothing"]["tshirt"] = 'F-default'
    point["duck"]["clothing"]["jacket"] = 'F-default'
    point["duck"]["clothing"]["tie"]= 'F-default'
    point["duck"]["clothing"]["bowtie"]= 'F-default'
    point["duck"]["clothing"]["aodai"] = 'F-default'
    point["duck"]["clothing"]["cape"] = 'F-default'
    point["duck"]["water"] = 'F-default'
    point["duck"]["eyebrows"] = 'F-default'
    point["duck"]["beard"] = 'F-default'
    point["duck"]["buttons"] = 'F-default'
    point["duck"]["lapel"] = 'F-default'
    point["duck"]["horsetail"] = 'F-default'
    point["duck"]["hair"] = 'none'
    point["duck"]["hair_colour"] = 'default'
    point["duck"]["hat"] = 'none'
    point["duck"]["hat_colour"] = 'default'
    point["duck"]["hat_extra"] = False
    point["duck"]["hat_extra_colour"] = 'default'
    point["duck"]["accessories"] = 'none'
    point["duck"]["accessories_colour"] = 'default'
    point["duck"]["accessories_extra_colour"] = 'default'
    point["duck"]["accessories_text"] = ''
    point["duck"]["necklace"] = 'none'
    point["duck"]["necklace_colour"] = 'default'
    point["duck"]["glasses"] = 'none'
    point["duck"]["glasses_colour"] = 'default'
    point["duck"]["thought"] = 'none'
    point["duck"]["thought_colour"] = 'default'
    point["duck"]["thought_text"] = ''

def register_new_point(eucl, point_data, setup=NEW_POINT, conf="p"):
    point = {}
    if setup == NEW_POINT:
        add_common_default_point_data(point, eucl, alpha='upper', coord=point_data)
        point["from"] = {}
        point["from"]["type"] = "free"
        eucl["points"].append(point)
    if setup == INTERSECT_POINT:
        if conf == "pppp":
            A,B,C,D = point_data
            add_common_default_point_data(point, eucl, alpha='upper')
            point["from"] = {}
            point["from"]["type"] = "intersection_ll"
            point["from"]["A"] = A
            point["from"]["B"] = B
            point["from"]["C"] = C
            point["from"]["D"] = D
            point["reverse_intersections"] = False
            eucl["points"].append(point)
        if conf == "cpp":
            circle_id, A_id, B_id = point_data
            lc_id = draw_random_number()
            add_common_default_point_data(point, eucl, alpha='upper')
            point["from"] = {}
            point["from"]["type"] = "intersection_lc"
            point["from"]["lc_id"] = lc_id
            point["from"]["circle"] = circle_id
            point["from"]["A"] = A_id
            point["from"]["B"] = B_id
            point["reverse_intersections"] = False
            eucl["points"].append(point)
            point = {}
            add_common_default_point_data(point, eucl, alpha='upper')
            point["from"] = {}
            point["from"]["type"] = "intersection_lc"
            point["from"]["lc_id"] = lc_id
            point["from"]["circle"] = circle_id
            point["from"]["A"] = A_id
            point["from"]["B"] = B_id
            point["reverse_intersections"] = False
            eucl["points"].append(point)

    if setup == MIDPOINT_CIRCLE:
        circle_id = point_data[0]
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "circle_midpoint"
        point["from"]["circle"] = circle_id
        eucl["points"].append(point)

    if setup == MIDPOINT_SEGMENT:
        A_id,B_id = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "segment_midpoint"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        eucl["points"].append(point)

    if setup == ROTATION:
        A_id,B_id, angle = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "rotation"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        point["from"]["angle"] = angle
        eucl["points"].append(point)

    if setup == POINT_ON_LINE:
        A_id,B_id, ratio = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "point_on_line"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        point["from"]["ratio"] = ratio
        eucl["points"].append(point)

    if setup == POINT_ON_CIRCLE:
        circle,angle = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "point_on_circle"
        point["from"]["circle"] = circle
        point["from"]["angle"] = angle
        eucl["points"].append(point)

    if setup == ORTHOGONAL_PROJECTION:
        A_id,B_id,P_id = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "projection_point"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        point["from"]["P"] = P_id
        eucl["points"].append(point)

    if setup == BISECTOR:
        A_id,B_id,C_id = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "bisector_point"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        point["from"]["C"] = C_id
        eucl["points"].append(point)

    if setup == TRANSLATION:
        A_id,B_id,P_id = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "translation_point"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        point["from"]["P"] = P_id
        eucl["points"].append(point)

    if setup == ORTHOGONAL:
        A_id,B_id = point_data
        add_common_default_point_data(point, eucl, alpha='upper')
        point["from"] = {}
        point["from"]["type"] = "orthogonal_point"
        point["from"]["A"] = A_id
        point["from"]["B"] = B_id
        eucl["points"].append(point)

def register_new_line(eucl, data, setup=SEGMENT_THROUGH):
    from_id, to_id = data
    segment = {}
    if setup == SEGMENT_THROUGH:
        segment["id"] = draw_random_number()
        segment["points"] = {}
        segment["points"]["from"] = from_id
        segment["points"]["to"] = to_id
        segment["line_width"] = DEFAULT_SEGMENT_LINE_WIDTH
        segment["line_stroke"] = DEFAULT_SEGMENT_LINE_STROKE
        segment["line_stroke_custom"] = DEFAULT_SEGMENT_LINE_STROKE_CUSTOM
        segment["line_colour_name"] = DEFAULT_SEGMENT_LINE_COLOUR_NAME
        segment["line_strength"] = DEFAULT_SEGMENT_LINE_STRENGTH
        segment["line_opacity"] = DEFAULT_SEGMENT_LINE_OPACITY
        # segment["pos_from"] = DEFAULT
        # segment["pos_to"] = DEFAULT
        segment["label"] = {}
        segment["label"]["show"] = False
        segment["label"]["angle"] = DEFAULT_SEGMENT_LABEL_ANGLE
        segment["label"]["distance"] = DEFAULT_SEGMENT_LABEL_DISTANCE
        segment["label"]["text"] = ''
        segment["label"]["anchor"] = DEFAULT_SEGMENT_LABEL_ANCHOR
        segment["label"]["position"] = DEFAULT_SEGMENT_LABEL_POSITION
        segment["o_arrow"] = {}
        segment["o_arrow"]["tip"] = DEFAULT_SEGMENT_O_ARROW_TIP
        segment["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
        segment["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
        segment["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
        segment["o_arrow"]["reversed"] = False
        segment["d_arrow"] = {}
        segment["d_arrow"]["tip"] = DEFAULT_SEGMENT_D_ARROW_TIP
        segment["d_arrow"]["length"] = DEFAULT_SEGMENT_D_ARROW_LENGTH
        segment["d_arrow"]["width"] = DEFAULT_SEGMENT_D_ARROW_WIDTH
        segment["d_arrow"]["side"] = DEFAULT_SEGMENT_D_ARROW_SIDE
        segment["d_arrow"]["reversed"] = False
        segment["mark"] = {}
        segment["mark"]["width"] = DEFAULT_SEGMENT_MARK_WIDTH
        segment["mark"]["colour"] = DEFAULT_SEGMENT_MARK_COLOUR
        segment["mark"]["position"] = DEFAULT_SEGMENT_MARK_POSITION
        segment["mark"]["size"] = DEFAULT_SEGMENT_MARK_SIZE
        segment["mark"]["symbol"] = DEFAULT_SEGMENT_MARK_SYMBOL
        segment["extension"] = {}
        segment["extension"]["origin"] = DEFAULT_SEGMENT_O_EXTENSION
        segment["extension"]["destination"] = DEFAULT_SEGMENT_D_EXTENSION
        segment["show"] = True
        eucl["segments"].append(segment)

def register_new_circle(eucl, circle_data, setup=CIRCUM_CIRCLE):
    circle = {}
    circle["id"] = draw_random_number()
    circle["show"] = True
    circle["line_width"] = DEFAULT_SEGMENT_LINE_WIDTH
    circle["line_stroke"] = DEFAULT_SEGMENT_LINE_STROKE
    circle["line_stroke_custom"] = DEFAULT_SEGMENT_LINE_STROKE_CUSTOM
    circle["line_colour_name"] = DEFAULT_SEGMENT_LINE_COLOUR_NAME
    circle["line_strength"] = DEFAULT_SEGMENT_LINE_STRENGTH
    circle["line_opacity"] = DEFAULT_SEGMENT_LINE_OPACITY
    circle["fill_colour_name"] = DEFAULT_POINT_FILL_COLOUR_NAME
    circle["fill_strength"] = DEFAULT_POINT_FILL_STRENGTH
    circle["fill_opacity"] = DEFAULT_POINT_FILL_OPACITY
    circle["label"] = {}
    circle["label"]["show"] = False
    circle["label"]["angle"] = DEFAULT_SEGMENT_LABEL_ANGLE
    circle["label"]["distance"] = DEFAULT_CIRCLE_LABEL_DISTANCE
    circle["label"]["text"] = ''
    circle["label"]["anchor"] = DEFAULT_CIRCLE_LABEL_ANCHOR
    circle["label"]["position"] = DEFAULT_SEGMENT_LABEL_POSITION
    circle["pattern"] = {}
    circle["pattern"]["type"] = DEFAULT_PATTERN_TYPE
    circle["pattern"]["distance"] = DEFAULT_PATTERN_DISTANCE
    circle["pattern"]["size"] = DEFAULT_PATTERN_SIZE
    circle["pattern"]["rotation"] = DEFAULT_PATTERN_ROTATION
    circle["pattern"]["xshift"] = DEFAULT_PATTERN_XSHIFT
    circle["pattern"]["yshift"] = DEFAULT_PATTERN_YSHIFT


    if setup == CIRCUM_CIRCLE:
        pt_1_id, pt_2_id, pt_3_id = circle_data
        circle["type"] = "circum_circle"
        circle["points"] = {}
        circle["points"]["A"] = pt_1_id
        circle["points"]["B"] = pt_2_id
        circle["points"]["C"] = pt_3_id
        eucl["circles"].append(circle)
    if setup == TWO_POINT_CIRCLE:
        pt_centre, pt_on_circle = circle_data
        circle["type"] = "two_point_circle"
        circle["points"] = {}
        circle["points"]["O"] = pt_centre
        circle["points"]["A"] = pt_on_circle
        eucl["circles"].append(circle)
    if setup == INSCRIBED_CIRCLE:
        pt_1_id, pt_2_id, pt_3_id = circle_data
        circle["type"] = "inscribed_circle"
        circle["points"] = {}
        circle["points"]["A"] = pt_1_id
        circle["points"]["B"] = pt_2_id
        circle["points"]["C"] = pt_3_id
        eucl["circles"].append(circle)
    if setup == ARC:
        pt_1_id, pt_2_id, pt_3_id = circle_data
        circle["type"] = "arc"
        circle["points"] = {}
        circle["points"]["O"] = pt_1_id
        circle["points"]["A"] = pt_2_id
        circle["points"]["B"] = pt_3_id
        circle["o_arrow"] = {}
        circle["o_arrow"]["tip"] = DEFAULT_SEGMENT_O_ARROW_TIP
        circle["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
        circle["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
        circle["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
        circle["o_arrow"]["reversed"] = False
        circle["d_arrow"] = {}
        circle["d_arrow"]["tip"] = DEFAULT_SEGMENT_D_ARROW_TIP
        circle["d_arrow"]["length"] = DEFAULT_SEGMENT_D_ARROW_LENGTH
        circle["d_arrow"]["width"] = DEFAULT_SEGMENT_D_ARROW_WIDTH
        circle["d_arrow"]["side"] = DEFAULT_SEGMENT_D_ARROW_SIDE
        circle["d_arrow"]["reversed"] = False
        eucl["circles"].append(circle)
    if setup == SECTOR:
        pt_1_id, pt_2_id, pt_3_id = circle_data
        circle["type"] = "sector"
        circle["points"] = {}
        circle["points"]["O"] = pt_1_id
        circle["points"]["A"] = pt_2_id
        circle["points"]["B"] = pt_3_id
        eucl["circles"].append(circle)

def register_new_polygon(eucl, polygon_data, setup=POLYGON):
    polygon = {}

    if setup == POLYGON:
        polygon["type"] = "polygon"
    if setup == LINESTRING:
        polygon["type"] = "linestring"

    polygon["id"] = draw_random_number()
    polygon["points"] = polygon_data.copy()
    polygon["show"] = True
    polygon["line_width"] = DEFAULT_SEGMENT_LINE_WIDTH
    polygon["line_stroke"] = DEFAULT_SEGMENT_LINE_STROKE
    polygon["line_stroke_custom"] = DEFAULT_SEGMENT_LINE_STROKE_CUSTOM
    polygon["line_colour_name"] = DEFAULT_SEGMENT_LINE_COLOUR_NAME
    polygon["line_strength"] = DEFAULT_SEGMENT_LINE_STRENGTH
    polygon["line_opacity"] = DEFAULT_SEGMENT_LINE_OPACITY
    polygon["fill_colour_name"] = DEFAULT_POINT_FILL_COLOUR_NAME
    polygon["fill_strength"] = DEFAULT_POINT_FILL_STRENGTH
    polygon["fill_opacity"] = DEFAULT_POINT_FILL_OPACITY
    polygon["curve"] = {}
    polygon["curve"]["strategy"] = DEFAULT_CURVE_STRATEGY
    polygon["curve"]["in_angle"] = DEFAULT_CURVE_IN_ANGLE
    polygon["curve"]["out_angle"] = DEFAULT_CURVE_OUT_ANGLE
    polygon["curve"]["bend_angle"] = DEFAULT_CURVE_BEND_ANGLE
    polygon["curve"]["loop"] = False
    polygon["curve"]["loop_size"] = DEFAULT_LOOP_SIZE
    polygon["curve"]["corner_radius"] = DEFAULT_CURVE_CORNER_RADIUS
    polygon["pattern"] = {}
    polygon["pattern"]["type"] = DEFAULT_PATTERN_TYPE
    polygon["pattern"]["distance"] = DEFAULT_PATTERN_DISTANCE
    polygon["pattern"]["size"] = DEFAULT_PATTERN_SIZE
    polygon["pattern"]["rotation"] = DEFAULT_PATTERN_ROTATION
    polygon["pattern"]["xshift"] = DEFAULT_PATTERN_XSHIFT
    polygon["pattern"]["yshift"] = DEFAULT_PATTERN_YSHIFT
    polygon["decoration"] = {}
    polygon["decoration"]["type"] = DEFAULT_DECORATOR_TYPE
    polygon["decoration"]["amplitude"] = DEFAULT_DECORATOR_AMPLITUDE
    polygon["decoration"]["wave_length"] = DEFAULT_DECORATOR_WAVE_LENGTH
    polygon["decoration"]["text"] = ''
    polygon["o_arrow"] = {}
    polygon["o_arrow"]["tip"] = DEFAULT_SEGMENT_O_ARROW_TIP
    polygon["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
    polygon["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
    polygon["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
    polygon["o_arrow"]["reversed"] = False
    polygon["d_arrow"] = {}
    polygon["d_arrow"]["tip"] = DEFAULT_SEGMENT_D_ARROW_TIP
    polygon["d_arrow"]["length"] = DEFAULT_SEGMENT_D_ARROW_LENGTH
    polygon["d_arrow"]["width"] = DEFAULT_SEGMENT_D_ARROW_WIDTH
    polygon["d_arrow"]["side"] = DEFAULT_SEGMENT_D_ARROW_SIDE
    polygon["d_arrow"]["reversed"] = False

    eucl["polygons"].append(polygon)

def register_new_angle(eucl, angle_data, setup=MARK_ANGLE):
    angle = {}
    A, B, C = angle_data
    angle["id"] = draw_random_number()
    angle["show"] = True
    angle["points"] = {}
    angle["points"]["A"] = A
    angle["points"]["B"] = B
    angle["points"]["C"] = C
    angle["type"] = DEFAULT_RIGHT_ANGLE_TYPE
    if setup == MARK_ANGLE:
        angle["right_angle"] = False
    else:
        angle["right_angle"] = True
    angle["arc"] = DEFAULT_ANGLE_ARC
    angle["size"] = DEFAULT_ANGLE_SIZE
    angle["mksize"] = DEFAULT_ANGLE_MARK_SIZE
    angle["mkcolour"] = DEFAULT_ANGLE_MARK_COLOUR
    angle["mkpos"] = DEFAULT_ANGLE_MARK_POSITION
    angle["mksymbol"] = DEFAULT_ANGLE_MARK_SYMBOL

    angle["line_width"] = DEFAULT_ANGLE_LINE_WIDTH
    angle["line_stroke"] = DEFAULT_ANGLE_LINE_STROKE
    angle["line_stroke_custom"] = DEFAULT_ANGLE_LINE_STROKE_CUSTOM
    angle["line_colour_name"] = DEFAULT_ANGLE_LINE_COLOUR_NAME
    angle["line_strength"] = DEFAULT_ANGLE_LINE_STRENGTH
    angle["line_opacity"] = DEFAULT_ANGLE_LINE_OPACITY
    angle["fill_colour_name"] = DEFAULT_ANGLE_FILL_COLOUR_NAME
    angle["fill_strength"] = DEFAULT_ANGLE_FILL_STRENGTH
    angle["fill_opacity"] = DEFAULT_ANGLE_FILL_OPACITY

    angle["label"] = {}
    angle["label"]["show"] = False
    angle["label"]["distance"] = DEFAULT_ANGLE_LABEL_DISTANCE
    angle["label"]["text"] = ''
    angle["label"]["anchor"] = DEFAULT_ANGLE_LABEL_ANCHOR

    angle["o_arrow"] = {}
    angle["o_arrow"]["tip"] = DEFAULT_SEGMENT_O_ARROW_TIP
    angle["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
    angle["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
    angle["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
    angle["o_arrow"]["reversed"] = False
    angle["d_arrow"] = {}
    angle["d_arrow"]["tip"] = DEFAULT_SEGMENT_D_ARROW_TIP
    angle["d_arrow"]["length"] = DEFAULT_SEGMENT_D_ARROW_LENGTH
    angle["d_arrow"]["width"] = DEFAULT_SEGMENT_D_ARROW_WIDTH
    angle["d_arrow"]["side"] = DEFAULT_SEGMENT_D_ARROW_SIDE
    angle["d_arrow"]["reversed"] = False

    eucl["angles"].append(angle)

def register_new_function(eucl, function_data, setup=YFX_FUNCTION):
    function = {}
    func, start, end = function_data

    left = eucl["window"]["left"]
    right = str(left + 10 * eucl["window"]["scale"])
    left = str(left)

    if setup == YFX_FUNCTION:
        function["type"] = 'yfx'
        if start == '':
            function["domain_start"] = left
        else:
            try:
                function["domain_start"] = start
            except:
                function["domain_start"] = left
        if end == '':
            function["domain_end"] = right
        else:
            try:
                function["domain_end"] = end
            except:
                function["domain_end"] = right
    elif setup == POLAR_FUNCTION:
        function["type"] = 'polar'
        if start == '':
            function["domain_start"] = '0'
        else:
            try:
                function["domain_start"] = start
            except:
                function["domain_start"] = '0'
        if end == '':
            function["domain_end"] = str(2*np.pi)
        else:
            try:
                function["domain_end"] = end
            except:
                function["domain_end"] = str(2*np.pi)
    elif setup == PARAMETRIC_FUNCTION:
        function["type"] = 'parametric'
        if start == '':
            function["domain_start"] = '0'
        else:
            try:
                function["domain_start"] = start
            except:
                function["domain_start"] = '0'
        if end == '':
            function["domain_end"] = '1'
        else:
            try:
                function["domain_end"] = end
            except:
                function["domain_end"] = '1'


    function["id"] = draw_random_number()
    function["show"] = True
    function["def"] = func
    function["samples"] = DEFAULT_FUNCTION_SAMPLES

    function["line_width"] = DEFAULT_SEGMENT_LINE_WIDTH
    function["line_stroke"] = DEFAULT_SEGMENT_LINE_STROKE
    function["line_stroke_custom"] = DEFAULT_SEGMENT_LINE_STROKE_CUSTOM
    function["line_colour_name"] = DEFAULT_SEGMENT_LINE_COLOUR_NAME
    function["line_strength"] = DEFAULT_SEGMENT_LINE_STRENGTH
    function["line_opacity"] = DEFAULT_SEGMENT_LINE_OPACITY
    function["fill_colour_name"] = DEFAULT_POINT_FILL_COLOUR_NAME
    function["fill_strength"] = DEFAULT_POINT_FILL_STRENGTH
    function["fill_opacity"] = DEFAULT_FUNCTION_FILL_OPACITY
    function["between"] = -1



    function["sum"] = {}
    function["sum"]["type"] = DEFAULT_FUNCTION_TYPE
    function['sum']['number'] = DEFAULT_FUNCTION_NUMBER
    function["sum"]["start"] = '%s' % ( eval(function["domain_start"]) + (eval(function["domain_end"])-eval(function["domain_start"])) * 0.1 )
    function["sum"]["end"] = '%s' % ( eval(function["domain_end"]) - (eval(function["domain_end"])-eval(function["domain_start"])) * 0.1 )
    function["sum"]["fill_colour_name"] = 'same'
    function["sum"]["fill_strength"] = DEFAULT_POINT_FILL_STRENGTH
    function["sum"]["fill_opacity"] = DEFAULT_FUNCTION_FILL_OPACITY
    function["sum"]["line_colour_name"] = DEFAULT_POINT_LINE_COLOUR_NAME
    function["sum"]["line_strength"] = DEFAULT_POINT_LINE_STRENGTH
    function["sum"]["line_opacity"] = DEFAULT_POINT_LINE_OPACITY

    function["area_start"] = function["domain_start"]
    function["area_end"] = function["domain_end"]

    function["o_arrow"] = {}
    function["o_arrow"]["tip"] = DEFAULT_SEGMENT_O_ARROW_TIP
    function["o_arrow"]["length"] = DEFAULT_SEGMENT_O_ARROW_LENGTH
    function["o_arrow"]["width"] = DEFAULT_SEGMENT_O_ARROW_WIDTH
    function["o_arrow"]["side"] = DEFAULT_SEGMENT_O_ARROW_SIDE
    function["o_arrow"]["reversed"] = False
    function["d_arrow"] = {}
    function["d_arrow"]["tip"] = DEFAULT_SEGMENT_D_ARROW_TIP
    function["d_arrow"]["length"] = DEFAULT_SEGMENT_D_ARROW_LENGTH
    function["d_arrow"]["width"] = DEFAULT_SEGMENT_D_ARROW_WIDTH
    function["d_arrow"]["side"] = DEFAULT_SEGMENT_D_ARROW_SIDE
    function["d_arrow"]["reversed"] = False

    function["pattern"] = {}
    function["pattern"]["type"] = DEFAULT_PATTERN_TYPE
    function["pattern"]["distance"] = DEFAULT_PATTERN_DISTANCE
    function["pattern"]["size"] = DEFAULT_PATTERN_SIZE
    function["pattern"]["rotation"] = DEFAULT_PATTERN_ROTATION
    function["pattern"]["xshift"] = DEFAULT_PATTERN_XSHIFT
    function["pattern"]["yshift"] = DEFAULT_PATTERN_YSHIFT

    eucl["functions"].append(function)
