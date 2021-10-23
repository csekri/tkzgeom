"""
contains functions that converts the eucl dictionary data structure into tikz
"""

from Constants import *
import PresetModels
import numpy as np # needed because of eval(), in order to use numpy inside


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

def line_stroke_custom_to_tkz(lengths):
    return_string = ''
    for i in range(len(lengths)):
        if i % 2 == 0:
            return_string += "on %s pt" % str(lengths[i])
        else:
            return_string += "off %s pt" % str(lengths[i])
        if i <= len(lengths)-1:
            return_string += ' '
    return return_string


def arrow_tip_to_tkz_option(tip_str):
    splitted = tip_str.split('^')
    if len(splitted) == 2:
        if splitted[1] == 'o':
            return splitted[0], 'open'
        if splitted[1] == 'r':
            return splitted[0], 'round'
        if splitted[1] == 'or':
            return splitted[0], 'open, round'
    else:
        return splitted[0] ,''


def tikzify_duck_new_commands(eucl):
    return_string = ''
    for model in DUCK_SPECIAL:
        for point in eucl["points"]:
            if point["duck"]["special"] == model and\
               point["duck"]["type"] == 'special' and point["duck"]["show"] == True:
                if model == 'horse':
                    add_model = PresetModels.horse()
                elif model == 'unicorn':
                    add_model = PresetModels.unicorn()
                elif model == 'bunny':
                    add_model = PresetModels.bunny()
                elif model == 'sheep':
                    add_model = PresetModels.sheep()
                elif model == 'girlwithpearlearring':
                    return_string += PresetModels.girl_with_pearl_earring_colours()
                    add_model = PresetModels.girl_with_pearl_earring()
                elif model == 'queenuk':
                    return_string += PresetModels.queen_uk_colours()
                    add_model = PresetModels.queen_uk()
                elif model == 'snowman':
                    add_model = PresetModels.snowman()
                elif model == 'overleaf':
                    add_model = PresetModels.overleaf()
                elif model == 'ceasar':
                    add_model = PresetModels.ceasar()
                elif model == 'ghost':
                    return_string += PresetModels.ghost_colours()
                    add_model = PresetModels.ghost()
                elif model == 'yoda':
                    return_string += PresetModels.yoda_colours()
                    add_model = PresetModels.yoda()
                elif model == 'vader':
                    add_model = PresetModels.vader()
                elif model == 'leila':
                    add_model = PresetModels.leila()

                return_string += add_model
                break
    for model in DUCK_CHESS:
        for point in eucl["points"]:
            if point["duck"]["chess"] == model and\
               point["duck"]["type"] == 'chess' and point["duck"]["show"] == True:
                add_model = ''
                if model == 'wbauer' or model == 'bbauer':
                    add_model = PresetModels.bauer()
                elif model == 'wturm' or model == 'bturm':
                    add_model = PresetModels.turm()
                elif model == 'wspringer' or model == 'bspringer':
                    add_model = PresetModels.springer()
                elif model == 'wlaeufer' or model == 'blaeufer':
                    add_model = PresetModels.laeufer()
                elif model == 'wdame' or model == 'bdame':
                    add_model = PresetModels.dame()
                elif model == 'wkoenig' or model == 'bkoenig':
                    add_model = PresetModels.koenig()
                if add_model != '':
                    return_string += PresetModels.chess_colours()
                return_string += add_model
                break
    return return_string



def tikzify_init(eucl, margin, top, bottom, left, right):
    scale = eucl["window"]["scale"]
    if eucl["bg_colour_name"] == 'none':
        return_string = "\\begin{tikzpicture}\n"
    else:
        return_string = "\\begin{tikzpicture}[background rectangle/.style={fill=%s!%s}, show background rectangle]\n" % (eucl["bg_colour_name"], eucl["bg_colour_strength"])
    return_string += "\\edef\\xmin{%f}\\edef\\xmax{%f}\n"  % (left, right)
    return_string += "\\edef\\ymin{%f}\\edef\\ymax{%f}\n"  % (bottom, top)
    return_string += "\\edef\\m{%f}"  % margin
    return_string += "\\edef\\xstep{%f}"  % max(round(scale),1)
    return_string += "\\edef\\ystep{%f}\n"  % max(round(scale),1)
    return return_string


def tikzify_grid(eucl):
    grid_options_a = 'sub, subxstep=\\xstep/%s, subystep=\\ystep/%s' % (eucl["grid"]["sub_x"], eucl["grid"]["sub_y"])
    grid_options_a += ', color=%s' % (eucl["grid"]["line_colour_name"])
    grid_options_b = 'color=%s' % (eucl["grid"]["line_colour_name"])
    grid = ''
    if eucl["grid"]["line_width"] != DEFAULT_POINT_LINE_WIDTH:
        grid_options_a += ', line width=%s' % (eucl["grid"]["line_width"])
        grid_options_b += ', line width=%s' % (eucl["grid"]["line_width"])

    if eucl["grid"]["line_stroke"] != DEFAULT_SEGMENT_LINE_STROKE or\
       eucl["grid"]["sub_line_stroke"] != DEFAULT_SEGMENT_LINE_STROKE:
        stroke_options = ''
        if eucl["grid"]["line_stroke"] == "custom":
            stroke_options += "dash pattern=%s" % line_stroke_custom_to_tkz(eucl["grid"]["line_stroke_custom"])
        else:
            stroke_options += str(eucl["grid"]["line_stroke"])
        if eucl["grid"]["line_stroke"] == DEFAULT_SEGMENT_LINE_STROKE:
            stroke_options = ''
        grid += '\\begin{scope}[%s]\n\\tkzGrid[%s]\n\\end{scope}\n' % (stroke_options, grid_options_b)

        stroke_options = ''
        if eucl["grid"]["sub_line_stroke"] == "custom":
            stroke_options += "dash pattern=%s" % line_stroke_custom_to_tkz(eucl["grid"]["sub_line_stroke_custom"])
        else:
            stroke_options += str(eucl["grid"]["sub_line_stroke"])
        if eucl["grid"]["sub_line_stroke"] == DEFAULT_SEGMENT_LINE_STROKE:
            stroke_options = ''
        grid += '\\begin{scope}[%s]\n\\tkzGrid[%s]\n\\end{scope}\n' % (stroke_options, grid_options_a)
    else:
        grid += '\\tkzGrid[%s]\n' % grid_options_a
    return grid


def tikzify_grid_with_any_axis(eucl, grid):
    return_string = "\\pgfmathparse{\\xmin+\\m}\\edef\\mxmin{\\pgfmathresult}"
    return_string += "\\pgfmathparse{\\ymin+\\m}\\edef\\mymin{\\pgfmathresult}"
    return_string += "\\pgfmathparse{\\xmax-\\m}\\edef\\mxmax{\\pgfmathresult}"
    return_string += "\\pgfmathparse{\\ymax-\\m}\\edef\\mymax{\\pgfmathresult}\n"
    return_string += "\\tkzInit[xmin=\\mxmin, ymin=\\mymin, xmax=\\mxmax, ymax=\\mymax, xstep=\\xstep, ystep=\\ystep]\n"
    if eucl["grid"]["show"]:
        return_string += '%GRID\n'
        if eucl["grid"]["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
            return_string += '\\begin{scope}[opacity=%s]\n' % eucl["grid"]["line_opacity"]
        return_string += grid
        if eucl["grid"]["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
            return_string += '\\end{scope}\n'
    return return_string


def tikzify_x_axis(eucl):
    return_string = ''
    if eucl["axis_x"]["show"]:
        if eucl["axis_x"]["labels"]["show"]:
            if eucl["axis"]["labels"]["x_rotate"] != 0:
                return_string += '\\begin{scope}[xlabel style/.append style={rotate=%s}]\n' % eucl["axis"]["labels"]["x_rotate"]
            options = ''
            if eucl["axis"]["labels"]["size"] != '':
                options += 'font=%s' % (eucl["axis"]["labels"]["size"])
            if eucl["axis"]["labels"]["colour"] != '':
                if options != '':
                    options += ', '
                options += 'text=%s' % (eucl["axis"]["labels"]["colour"])
            if not eucl["axis_x"]["is_orig"]:
                if options != '':
                    options += ', '
                options += 'orig=false'
            if not eucl["axis_x"]["is_numprint"]:
                if options != '':
                    options += ', '
                options += 'np off=true'
            if eucl["axis_x"]["trig"] != 0:
                if options != '':
                    options += ', '
                options += 'trig=%s' % eucl["axis_x"]["trig"]
            elif eucl["axis_x"]["frac"] != 0:
                if options != '':
                    options += ', '
                options += 'frac=%s' % eucl["axis_x"]["frac"]
            if eucl["axis"]["labels"]["x_below"] != 0:
                options += ', below=%s pt' % eucl["axis"]["labels"]["x_below"]

            return_string += "\\tkzLabelX[%s]\n" % options
            if eucl["axis"]["labels"]["x_rotate"] != 0:
                return_string += '\\end{scope}\n'

        options = 'label=%s' % eucl["axis_x"]["label"]["text"]
        if eucl["axis_x"]["label"]["anchor"] != 'below':
            options += ', ' + eucl["axis_x"]["label"]["anchor"]
            if eucl["axis_x"]["label"]["distance"] != DEFAULT_ANCHOR_DISTANCE:
                options += '=%s' % eucl["axis_x"]["label"]["distance"]
        elif eucl["axis_x"]["label"]["distance"] != DEFAULT_ANCHOR_DISTANCE:
            options += ', below=%s' % eucl["axis_x"]["label"]["distance"]
        if eucl["axis"]["line_colour_name"] != DEFAULT_POINT_LINE_COLOUR_NAME or\
           eucl["axis"]["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
            options += ', color=%s' % eucl["axis"]["line_colour_name"]
            if eucl["axis"]["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
                options += '!%s' % eucl["axis"]["line_strength"]
        if eucl["axis"]["line_width"] != DEFAULT_POINT_LINE_WIDTH:
                options += ", line width=%s" % eucl["axis"]["line_width"]
        if not eucl["axis_x"]["is_tick"]:
                options += ', noticks=true'
        if eucl["axis_x"]["trig"] != 0:
            options += ', trig=%s' % eucl["axis_x"]["trig"]
        if eucl["axis_x"]["tick_up"] != 1.0:
            options += ', tickup=%s pt' % eucl["axis_x"]["tick_up"]
        if eucl["axis_x"]["tick_down"] != 1.0:
            options += ', tickdn=%s pt' % eucl["axis_x"]["tick_down"]
        if eucl["axis_x"]["tick_width"] != 0.8:
            options += ', tickwd=%s pt' % eucl["axis_x"]["tick_width"]

        if eucl["axis_x"]["o_arrow"]["tip"] != 'none':
            o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(eucl["axis_x"]["o_arrow"]["tip"])
            if eucl["axis_x"]["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += "scale length=%f" % eucl["axis_x"]["o_arrow"]["length"]
            if eucl["axis_x"]["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += "scale width=%f" % eucl["axis_x"]["o_arrow"]["width"]
            if eucl["axis_x"]["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += eucl["axis_x"]["o_arrow"]["side"]
            if eucl["axis_x"]["o_arrow"]["reversed"]:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += "reversed"

        if eucl["axis_x"]["o_arrow"]["tip"] == 'none':
            return_string += '\\tikzset{xaxe style/.style={-}}\n'
        else:
            if eucl["axis_x"]["o_arrow"]["direction"]:
                return_string += '\\tikzset{xaxe style/.style={arrows={-%s[%s]}}}\n' % (o_arrow_name, o_arrow_options)
            else:
                return_string += '\\tikzset{xaxe style/.style={arrows={%s[%s]-}}}\n' % (o_arrow_name, o_arrow_options)

        return_string += "\\tkzDrawX[%s]\n" % options
    if return_string != '':
        return_string = '%X AXIS\n' + return_string
    return return_string


def tikzify_y_axis(eucl):
    return_string = ''
    if eucl["axis_y"]["show"]:
        if eucl["axis_y"]["labels"]["show"]:
            options = ''
            if eucl["axis"]["labels"]["size"] != '':
                options += 'font=%s' % (eucl["axis"]["labels"]["size"])
            if eucl["axis"]["labels"]["colour"] != '':
                if options != '':
                    options += ', '
                options += 'text=%s' % (eucl["axis"]["labels"]["colour"])
            if not eucl["axis_y"]["is_orig"]:
                if options != '':
                    options += ', '
                options += 'orig=false'
            if not eucl["axis_y"]["is_numprint"]:
                if options != '':
                    options += ', '
                options += 'np off=true'
            if eucl["axis_y"]["trig"] != 0:
                if options != '':
                    options += ', '
                options += 'trig=%s' % eucl["axis_y"]["trig"]
            elif eucl["axis_y"]["frac"] != 0:
                if options != '':
                    options += ', '
                options += 'frac=%s' % eucl["axis_y"]["frac"]
            return_string += "\\tkzLabelY[%s]\n" % options

        options = 'label=%s' % eucl["axis_y"]["label"]["text"]
        if eucl["axis_y"]["label"]["anchor"] != 'left':
            options += ', ' + eucl["axis_y"]["label"]["anchor"]
            if eucl["axis_y"]["label"]["distance"] != DEFAULT_ANCHOR_DISTANCE:
                options += '=%s' % eucl["axis_y"]["label"]["distance"]
        elif eucl["axis_y"]["label"]["distance"] != DEFAULT_ANCHOR_DISTANCE:
            options += ', left=%s' % eucl["axis_y"]["label"]["distance"]
        if eucl["axis"]["line_colour_name"] != DEFAULT_POINT_LINE_COLOUR_NAME or\
           eucl["axis"]["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
            options += ', color=%s' % eucl["axis"]["line_colour_name"]
            if eucl["axis"]["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
                options += '!%s' % eucl["axis"]["line_strength"]
        if eucl["axis"]["line_width"] != DEFAULT_POINT_LINE_WIDTH:
                options += ", line width=%s" % eucl["axis"]["line_width"]
        if not eucl["axis_y"]["is_tick"]:
                options += ', noticks=true'
        if eucl["axis_y"]["trig"] != 0:
            options += ', trig=%s' % eucl["axis_y"]["trig"]
        if eucl["axis_y"]["tick_up"] != 1.0:
            options += ', ticklt=%s pt' % eucl["axis_y"]["tick_up"]
        if eucl["axis_y"]["tick_down"] != 1.0:
            options += ', tickrt=%s pt' % eucl["axis_y"]["tick_down"]
        if eucl["axis_y"]["tick_width"] != 0.8:
            options += ', tickwd=%s pt' % eucl["axis_y"]["tick_width"]

        if eucl["axis_y"]["o_arrow"]["tip"] != 'none':
            o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(eucl["axis_y"]["o_arrow"]["tip"])
            if eucl["axis_y"]["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += "scale length=%f" % eucl["axis_y"]["o_arrow"]["length"]
            if eucl["axis_y"]["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += "scale width=%f" % eucl["axis_y"]["o_arrow"]["width"]
            if eucl["axis_y"]["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += eucl["axis_y"]["o_arrow"]["side"]
            if eucl["axis_y"]["o_arrow"]["reversed"]:
                if o_arrow_options != "":
                    o_arrow_options += ", "
                o_arrow_options += "reversed"

        if eucl["axis_y"]["o_arrow"]["tip"] == 'none':
            return_string += '\\tikzset{yaxe style/.style={-}}\n'
        else:
            if eucl["axis_y"]["o_arrow"]["direction"]:
                return_string += '\\tikzset{yaxe style/.style={arrows={-%s[%s]}}}\n' % (o_arrow_name, o_arrow_options)
            else:
                return_string += '\\tikzset{yaxe style/.style={arrows={%s[%s]-}}}\n' % (o_arrow_name, o_arrow_options)

        return_string += "\\tkzDrawY[%s]\n" % options
    if return_string != '':
        return_string = '%Y AXIS\n' + return_string
    return return_string


def tikzify_axis_clip(eucl):
    return_string = "%CLIP TO AXES\n"
    return_string += "\\tkzClip[space=\\m/\\xstep]\n"
    return_string += "\\tkzDefPoints{\\mxmin/\\mymin/cornerA,\\mxmax/\\mymin/cornerB,\\mxmax/\\mymax/cornerC,\\mxmin/\\mymax/cornerD}\n"
    return_string += "\\tkzClipPolygon(cornerA, cornerB, cornerC, cornerD)\n"
    return return_string


def tikzify_grid_without_axis(eucl, grid):
    return_string = "\\tkzInit[xmin=\\xmin, ymin=\\ymin, xmax=\\xmax, ymax=\\ymax, xstep=\\xstep, ystep=\\ystep]\n"
    return_string += "\\tkzClip\n"
    if eucl["grid"]["show"]:
        return_string += "%GRID\n"
        if eucl["grid"]["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
            return_string += '\\begin{scope}[opacity=%s]\n' % eucl["grid"]["line_opacity"]
        return_string += grid
        if eucl["grid"]["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
            return_string += '\\end{scope}\n'
    return return_string


def tikzify_all_point_declarations(eucl):
    return_string = ''
    mapped_points = ['pt_default']
    num_points = len(eucl["points"])

    while len(mapped_points) < num_points:
        for point in eucl["points"]:
            if point["id"] in mapped_points:
                continue

            if point["from"]["type"] == "free":
                mapped_points.append(point["id"])
                return_string += "\\tkzDefPoint(%f, %f){%s}\n" % (eval(point["x"]), eval(point["y"]), point["id"])
            elif point["from"]["type"] == "intersection_ll":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    if point["from"]["C"] in mapped_points and point["from"]["D"] in mapped_points:
                        mapped_points.append(point["id"])
                        return_string += "\\tkzInterLL(%s,%s)(%s,%s)" % (point["from"]["A"],point["from"]["B"],point["from"]["C"],point["from"]["D"])
                        return_string += "\\tkzGetPoint{%s}\n" % (point["id"])
            elif point["from"]["type"] == "intersection_lc":
                if point["from"]["A"] in mapped_points and point["from"]["B"] in mapped_points:
                    for pt in eucl["points"]:
                        if pt["from"]["type"] == "intersection_lc" and pt["id"] != point["id"] and pt["from"]["lc_id"] == point["from"]["lc_id"]:
                            circle = get_item_from_id(eucl, point["from"]["circle"], 'c')
                            if circle["type"] == "two_point_circle":
                                if circle["points"]["O"] in mapped_points and circle["points"]["A"] in mapped_points:
                                    O = circle["points"]["O"]
                                    A = circle["points"]["A"]
                                    mapped_points.append(point["id"])
                                    mapped_points.append(pt["id"])
                                    return_string += "\\tkzInterLC(%s,%s)(%s,%s)" % (point["from"]["A"],point["from"]["B"],O,A)
                                    if point["reverse_intersections"] == True:
                                        return_string += "\\tkzGetPoints{%s}{%s}\n" % (pt["id"], point["id"])
                                    else:
                                        return_string += "\\tkzGetPoints{%s}{%s}\n" % (point["id"], pt["id"])
                            if circle["type"] == "circum_circle" or circle["type"] == "inscribed_circle":
                                if circle["points"]["A"] in mapped_points and circle["points"]["B"] in mapped_points and\
                                   circle["points"]["C"] in mapped_points:
                                    circle_type = 'circum' if circle["type"] == "circum_circle" else 'in'
                                    mapped_points.append(point["id"])
                                    mapped_points.append(pt["id"])
                                    return_string += "\\tkzDefCircle[%s](%s,%s,%s)\n" % (circle_type, circle["points"]["A"],circle["points"]["B"],circle["points"]["C"])
                                    return_string += "\\tkzInterLC[R](%s,%s)(tkzPointResult, \\tkzLengthResult pt)" % (point["from"]["A"],point["from"]["B"])
                                    return_string += "\\tkzGetPoints{%s}{%s}\n" % (pt["id"], point["id"])

            elif point["from"]["type"] == "circle_midpoint":
                circle_id = point["from"]["circle"]
                circle = get_item_from_id(eucl, circle_id, 'c')
                if circle["type"] == "circum_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        mapped_points.append(point["id"])
                        A = circle["points"]["A"]
                        B = circle["points"]["B"]
                        C = circle["points"]["C"]
                        center_name = f"circum_{A}_{B}_{C}"
                        return_string += "\\tkzDefCircle[circum](%s,%s,%s) \\tkzGetPoint{%s}\\tkzGetLength{%s}\n" % (A, B, C, point["id"], center_name)
                if circle["type"] == "inscribed_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        mapped_points.append(point["id"])
                        A = circle["points"]["A"]
                        B = circle["points"]["B"]
                        C = circle["points"]["C"]
                        center_name = f"in_{A}_{B}_{C}"
                        return_string += "\\tkzDefCircle[in](%s,%s,%s) \\tkzGetPoint{%s}\\tkzGetLength{%s}\n" % (A, B, C, point["id"], center_name)
            elif point["from"]["type"] == "segment_midpoint":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    return_string += "\\tkzDefMidPoint(%s,%s) \\tkzGetPoint{%s}\n" % (A, B, point["id"])
            elif point["from"]["type"] == "point_on_line":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    ratio = eval(point["from"]["ratio"])
                    return_string += "\\tkzDefPointBy[homothety=center %s ratio %s](%s) \\tkzGetPoint{%s}\n" % (A, ratio, B, point["id"])
            elif point["from"]["type"] == "point_on_circle":
                circle_id = point["from"]["circle"]
                circle = get_item_from_id(eucl, circle_id, 'c')
                if circle["type"] == "circum_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        mapped_points.append(point["id"])
                        A = circle["points"]["A"]
                        B = circle["points"]["B"]
                        C = circle["points"]["C"]
                        angle = point["from"]["angle"]
                        name = f"in_{A}_{B}_{C}"
                        return_string += "\\tkzDefCircle[circum](%s,%s,%s)\\tkzDefPointOnCircle[angle=%s, center=tkzPointResult, radius=\\tkzLengthResult pt] \\tkzGetPoint{%s}\\tkzGetLength{%s}\n" % (A, B, C, angle, point["id"], name)
                if circle["type"] == "inscribed_circle":
                    if circle["points"]["A"] in mapped_points and\
                       circle["points"]["B"] in mapped_points and\
                       circle["points"]["C"] in mapped_points:
                        mapped_points.append(point["id"])
                        A = circle["points"]["A"]
                        B = circle["points"]["B"]
                        C = circle["points"]["C"]
                        angle = point["from"]["angle"]
                        return_string += "\\tkzDefCircle[in](%s,%s,%s)\\tkzDefPointOnCircle[angle=%s, center=tkzPointResult, radius=\\tkzLengthResult pt] \\tkzGetPoint{%s}\n" % (A, B, C, angle, point["id"])
            elif point["from"]["type"] == "projection_point":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points and\
                   point["from"]["P"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    P = point["from"]["P"]
                    return_string += "\\tkzDefPointBy[projection=onto %s--%s](%s)\\tkzGetPoint{%s}\n" % (A, B, P, point["id"])
            elif point["from"]["type"] == "bisector_point":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points and\
                   point["from"]["C"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    C = point["from"]["C"]
                    return_string += "\\tkzDefLine[bisector](%s,%s,%s)\\tkzGetPoint{%s}\n" % (A, B, C, point["id"])
            elif point["from"]["type"] == "translation_point":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points and\
                   point["from"]["P"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    P = point["from"]["P"]
                    return_string += "\\tkzDefPointWith[colinear=at %s](%s,%s)\\tkzGetPoint{%s}\n" % (P, A, B, point["id"])
            elif point["from"]["type"] == "orthogonal_point":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    return_string += "\\tkzDefPointWith[orthogonal](%s,%s)\\tkzGetPoint{%s}\n" % (A, B, point["id"])
            elif point["from"]["type"] == "rotation":
                if point["from"]["A"] in mapped_points and\
                   point["from"]["B"] in mapped_points:
                    mapped_points.append(point["id"])
                    A = point["from"]["A"]
                    B = point["from"]["B"]
                    angle = eval(point["from"]["angle"])
                    return_string += "\\tkzDefPointBy[rotation=center %s angle %s](%s)\\tkzGetPoint{%s}" % (A, angle, B, point["id"])
    if return_string != '':
        return_string = '%POINT/COORDINATE DEFINITIONS\n' + return_string
    return return_string


def tikzify_polygons_and_linestrings(eucl):
    return_string = ''
    for polygon in eucl["polygons"]:
        if polygon["show"] and polygon["id"] != 'pol_default':
            common_options = ''
            if polygon["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                common_options += "line width=%s" % polygon["line_width"]
            if polygon["line_stroke"] != DEFAULT_SEGMENT_LINE_STROKE:
                if common_options != "":
                    common_options += ", "
                if polygon["line_stroke"] == "custom":
                    common_options += "dash pattern=%s" % line_stroke_custom_to_tkz(polygon["line_stroke_custom"])
                else:
                    common_options += str(polygon["line_stroke"])
            if polygon["line_colour_name"] != DEFAULT_SEGMENT_LINE_COLOUR_NAME or\
               polygon["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                if common_options != "":
                    common_options += ", "
                common_options += "draw=%s" % polygon["line_colour_name"]
                if polygon["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                    common_options += "!%s" % polygon["line_strength"]
            if polygon["pattern"]["type"] == 'solid':
                if common_options != "":
                    common_options += ", "
                common_options += "fill=%s" % polygon["fill_colour_name"]
                if polygon["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                    common_options += "!%s" % polygon["fill_strength"]

            if polygon["decoration"]["type"] != DEFAULT_DECORATOR_TYPE:
                if common_options != "":
                    common_options += ", "
                if polygon["decoration"]["type"] == 'text along path':
                    common_options += "decoration={%s, text={%s}}, decorate\n" % (polygon["decoration"]["type"], polygon["decoration"]["text"])
                else:
                    common_options += "decoration={%s, amplitude=%s, segment length=%s}, decorate\n" % (polygon["decoration"]["type"], polygon["decoration"]["amplitude"], polygon["decoration"]["wave_length"])

            if polygon["fill_opacity"] != DEFAULT_POINT_FILL_OPACITY:
                if common_options != '':
                    common_options += ', '
                common_options += 'fill opacity=%s' % polygon["fill_opacity"]

            if polygon["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
                if common_options != '':
                    common_options += ', '
                common_options += 'draw opacity=%s' % polygon["line_opacity"]

            if not polygon["pattern"]["type"] in ['none', 'solid']:
                if polygon["fill_colour_name"] != DEFAULT_POINT_FILL_COLOUR_NAME or\
                   polygon["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                    if common_options != "":
                        common_options += ", "
                    common_options += "pattern color=%s" % polygon["fill_colour_name"]
                    if polygon["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                        common_options += "!%s" % polygon["fill_strength"]
                if common_options != '':
                    common_options += ', '
                if not polygon["pattern"]["type"] in\
                   ['Lines', 'Hatch', 'Dots', 'Fivepointed stars', 'Sixpointed stars']:
                    common_options += 'pattern=%s' % polygon["pattern"]["type"]
                else:
                    pattern_options = ''
                    if polygon["pattern"]["rotation"] != DEFAULT_PATTERN_ROTATION:
                        pattern_options += 'angle=%s' % polygon["pattern"]["rotation"]
                    if polygon["pattern"]["distance"] != DEFAULT_PATTERN_DISTANCE:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'distance=%s' % polygon["pattern"]["distance"]
                        if polygon["pattern"]["type"] in ['Fivepointed stars', 'Sixpointed stars']:
                            pattern_options += ' mm'
                    if polygon["pattern"]["xshift"] != DEFAULT_PATTERN_XSHIFT:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'xshift=%s' % polygon["pattern"]["xshift"]
                    if polygon["pattern"]["yshift"] != DEFAULT_PATTERN_YSHIFT:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'yshift=%s' % polygon["pattern"]["yshift"]
                    if polygon["pattern"]["type"] in ['Dots', 'Fivepointed stars', 'Sixpointed stars']:
                        if polygon["pattern"]["size"] != DEFAULT_PATTERN_SIZE:
                            if pattern_options != '':
                                pattern_options += ', '
                            pattern_options += 'radius=%s mm' % polygon["pattern"]["size"]
                    else:
                        if polygon["pattern"]["size"] != DEFAULT_PATTERN_SIZE:
                            if pattern_options != '':
                                pattern_options += ', '
                            pattern_options += 'line width=%s' % polygon["pattern"]["size"]
                    if polygon["pattern"]["type"] == 'Fivepointed stars':
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'points=5'
                    if polygon["pattern"]["type"] == 'Sixpointed stars':
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'points=6'
                    if polygon["pattern"]["type"] in ['Sixpointed stars', 'Fivepointed stars']:
                        common_options += 'pattern={Stars[%s]}' % pattern_options
                    else:
                        common_options += 'pattern={%s[%s]}' % (polygon["pattern"]["type"], pattern_options)


            if polygon["type"] == 'polygon':
                options = common_options

                if polygon["curve"]["strategy"] == 'smooth':
                    if options != '':
                        options = 'use Hobby shortcut, ' + options
                    else:
                        options = 'use Hobby shortcut'
                    points = "([closed,]%s)" % ((')..(').join(polygon["points"]))
                    return_string += "\\draw[%s] %s;\n" % (options, points)
                elif polygon["curve"]["strategy"] == 'nothing':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    points = "%s" % ((')--(').join(polygon["points"]))
                    return_string += "\\draw[%s] (%s)--cycle;\n" % (options, points)
                elif polygon["curve"]["strategy"] == 'segment_in_out':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    in_out_option = 'out=%s, in=%s' % (polygon["curve"]["out_angle"], polygon["curve"]["in_angle"])
                    if polygon["curve"]["loop"]:
                        in_out_option += ", loop, min distance=%s" % polygon["curve"]["loop_size"]
                    points = "%s" % ((')--(').join(polygon["points"][1:]))
                    return_string += "\\draw[%s] (%s) to[%s] (%s)--cycle;\n" % (common_options,polygon["points"][0], in_out_option, points)
                elif polygon["curve"]["strategy"] == 'segment_bend_left':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    bend_options = 'bend left=%s' % polygon["curve"]["bend_angle"]
                    points = "%s" % ((f') to [{bend_options}] (').join(polygon["points"]))
                    return_string += "\\draw[%s] (%s) to[%s] cycle;\n" % (options, points, bend_options)
                elif polygon["curve"]["strategy"] == 'segment_bend_right':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    bend_options = 'bend right=%s' % polygon["curve"]["bend_angle"]
                    points = "%s" % ((f') to [{bend_options}] (').join(polygon["points"]))
                    return_string += "\\draw[%s] (%s) to[%s] cycle;\n" % (options, points, bend_options)

            elif polygon["type"] == 'linestring':
                options = ''

                if polygon["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP or\
                   polygon["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    if options != "":
                        options += ", "
                    if polygon["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP:
                        o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(polygon["o_arrow"]["tip"])
                        if polygon["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "scale length=%f" % polygon["o_arrow"]["length"]
                        if polygon["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "scale width=%f" % polygon["o_arrow"]["width"]
                        if polygon["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += polygon["o_arrow"]["side"]
                        if polygon["o_arrow"]["reversed"]:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "reversed"
                    if polygon["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                        d_arrow_name, d_arrow_options = arrow_tip_to_tkz_option(polygon["d_arrow"]["tip"])
                        if polygon["d_arrow"]["length"] != DEFAULT_SEGMENT_D_ARROW_LENGTH:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "scale length=%f" % polygon["d_arrow"]["length"]
                        if polygon["d_arrow"]["width"] != DEFAULT_SEGMENT_D_ARROW_WIDTH:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "scale width=%f" % polygon["d_arrow"]["width"]
                        if polygon["d_arrow"]["side"] != DEFAULT_SEGMENT_D_ARROW_SIDE:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += polygon["d_arrow"]["side"]
                        if polygon["d_arrow"]["reversed"]:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "reversed"

                    if polygon["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP and\
                       polygon["d_arrow"]["tip"] == DEFAULT_SEGMENT_D_ARROW_TIP:
                        options += "arrows={%s[%s]-}" % (o_arrow_name, o_arrow_options)
                    elif polygon["o_arrow"]["tip"] == DEFAULT_SEGMENT_O_ARROW_TIP and\
                       polygon["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                        options += "arrows={-%s[%s]}" % (d_arrow_name, d_arrow_options)
                    else:
                        options += "arrows={%s[%s]-%s[%s]}" % (o_arrow_name, o_arrow_options, d_arrow_name, d_arrow_options)

                if options != '':
                    options += ', '
                options += common_options

                if polygon["curve"]["strategy"] == 'smooth':
                    if options != '':
                        options = 'use Hobby shortcut, ' + options
                    else:
                        options = 'use Hobby shortcut'
                    points = "(%s)" % ((')..(').join(polygon["points"]))
                    return_string += "\\draw[%s] %s;\n" % (options, points)
                elif polygon["curve"]["strategy"] == 'nothing':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    points = "%s" % ((')--(').join(polygon["points"]))
                    return_string += "\\draw[%s] (%s);\n" % (options, points)
                elif polygon["curve"]["strategy"] == 'segment_in_out':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    in_out_option = 'out=%s, in=%s' % (polygon["curve"]["out_angle"], polygon["curve"]["in_angle"])
                    if polygon["curve"]["loop"]:
                        in_out_option += ", loop, min distance=%s" % polygon["curve"]["loop_size"]
                    points = "%s" % ((')--(').join(polygon["points"][1:]))
                    return_string += "\\draw[%s] (%s) to[%s] (%s);\n" % (options,polygon["points"][0], in_out_option, points)
                elif polygon["curve"]["strategy"] == 'segment_bend_left':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    bend_options = 'bend left=%s' % polygon["curve"]["bend_angle"]
                    points = "%s" % ((f') to [{bend_options}] (').join(polygon["points"]))
                    return_string += "\\draw[%s] (%s);\n" % (options, points)
                elif polygon["curve"]["strategy"] == 'segment_bend_right':
                    if polygon["curve"]["corner_radius"] != 0:
                        if options != '':
                            options += ', '
                        options += 'rounded corners=%s' % polygon["curve"]["corner_radius"]
                    bend_options = 'bend right=%s' % polygon["curve"]["bend_angle"]
                    points = "%s" % ((f') to [{bend_options}] (').join(polygon["points"]))
                    return_string += "\\draw[%s] (%s);\n" % (options, points)
    if return_string != '':
        return_string = '%POLYGONS/LINESTRINGS\n' + return_string
    return return_string


def tikzify_functions(eucl):
    return_string = ''
    for function in eucl["functions"]:
        if function["show"] and function["id"] != 'fct_default':
            options = 'domain=%s:%s, samples=%s' % (eval(function["domain_start"]), eval(function["domain_end"]), function["samples"])
            if function["line_colour_name"] != DEFAULT_SEGMENT_LINE_COLOUR_NAME or\
               function["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                options += ", draw=%s" % function["line_colour_name"]
                if function["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                    options += "!%s" % function["line_strength"]
            if function["line_opacity"] != DEFAULT_SEGMENT_LINE_OPACITY:
                if options != "":
                    options += ", "
                options += "draw opacity=%s" % (function["line_opacity"])
            if function["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                if options != "":
                    options += ", "
                options += "line width=%s pt" % function["line_width"]
            if function["line_stroke"] != DEFAULT_SEGMENT_LINE_STROKE:
                if options != "":
                    options += ", "
                if function["line_stroke"] == "custom":
                    options += "dash pattern=%s" % line_stroke_custom_to_tkz(function["line_stroke_custom"])
                else:
                    options += str(function["line_stroke"])
            if function["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP or\
               function["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                if options != "":
                    options += ", "
                if function["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP:
                    o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(function["o_arrow"]["tip"])
                    if function["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += "scale length=%f" % function["o_arrow"]["length"]
                    if function["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += "scale width=%f" % function["o_arrow"]["width"]
                    if function["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += function["o_arrow"]["side"]
                    if function["o_arrow"]["reversed"]:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += "reversed"
                if function["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    d_arrow_name, d_arrow_options = arrow_tip_to_tkz_option(function["d_arrow"]["tip"])
                    if function["d_arrow"]["length"] != DEFAULT_SEGMENT_D_ARROW_LENGTH:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += "scale length=%f" % function["d_arrow"]["length"]
                    if function["d_arrow"]["width"] != DEFAULT_SEGMENT_D_ARROW_WIDTH:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += "scale width=%f" % function["d_arrow"]["width"]
                    if function["d_arrow"]["side"] != DEFAULT_SEGMENT_D_ARROW_SIDE:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += function["d_arrow"]["side"]
                    if function["d_arrow"]["reversed"]:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += "reversed"

                if function["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP and\
                   function["d_arrow"]["tip"] == DEFAULT_SEGMENT_D_ARROW_TIP:
                    options += "arrows={%s[%s]-}" % (o_arrow_name, o_arrow_options)
                elif function["o_arrow"]["tip"] == DEFAULT_SEGMENT_O_ARROW_TIP and\
                   function["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    options += "arrows={-%s[%s]}" % (d_arrow_name, d_arrow_options)
                else:
                    options += "arrows={%s[%s]-%s[%s]}" % (o_arrow_name, o_arrow_options, d_arrow_name, d_arrow_options)


            return_string += '\\begin{scope}\n'


            all_pattern_options = ''

            if not function["pattern"]["type"] in ['none', 'solid']:
                if function["fill_colour_name"] != DEFAULT_POINT_FILL_COLOUR_NAME or\
                   function["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                    all_pattern_options += "pattern color=%s" % function["fill_colour_name"]
                    if function["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                        all_pattern_options += "!%s" % function["fill_strength"]
                if all_pattern_options != '':
                    all_pattern_options += ', '
                if not function["pattern"]["type"] in\
                   ['Lines', 'Hatch', 'Dots', 'Fivepointed stars', 'Sixpointed stars']:
                    all_pattern_options += 'pattern=%s' % function["pattern"]["type"]
                else:
                    pattern_options = ''
                    if function["pattern"]["rotation"] != DEFAULT_PATTERN_ROTATION:
                        pattern_options += 'angle=%s' % function["pattern"]["rotation"]
                    if function["pattern"]["distance"] != DEFAULT_PATTERN_DISTANCE:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'distance=%s' % function["pattern"]["distance"]
                        if function["pattern"]["type"] in ['Fivepointed stars', 'Sixpointed stars']:
                            pattern_options += ' mm'
                    if function["pattern"]["xshift"] != DEFAULT_PATTERN_XSHIFT:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'xshift=%s' % function["pattern"]["xshift"]
                    if function["pattern"]["yshift"] != DEFAULT_PATTERN_YSHIFT:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'yshift=%s' % function["pattern"]["yshift"]
                    if function["pattern"]["type"] in ['Dots', 'Fivepointed stars', 'Sixpointed stars']:
                        if function["pattern"]["size"] != DEFAULT_PATTERN_SIZE:
                            if pattern_options != '':
                                pattern_options += ', '
                            pattern_options += 'radius=%s mm' % function["pattern"]["size"]
                    else:
                        if function["pattern"]["size"] != DEFAULT_PATTERN_SIZE:
                            if pattern_options != '':
                                pattern_options += ', '
                            pattern_options += 'line width=%s' % function["pattern"]["size"]
                    if function["pattern"]["type"] == 'Fivepointed stars':
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'points=5'
                    if function["pattern"]["type"] == 'Sixpointed stars':
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'points=6'
                    if function["pattern"]["type"] in ['Sixpointed stars', 'Fivepointed stars']:
                        all_pattern_options += 'pattern={Stars[%s]}' % pattern_options
                    else:
                        all_pattern_options += 'pattern={%s[%s]}' % (function["pattern"]["type"], pattern_options)

            if function["pattern"]["type"] != 'none':
                if function["pattern"]["type"] == 'solid':
                    if all_pattern_options != "":
                        all_pattern_options += ", "
                    all_pattern_options += "fill=%s" % function["fill_colour_name"]
                    if function["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                        all_pattern_options += "!%s" % function["fill_strength"]
                all_pattern_options += ", fill opacity=%s, draw opacity=%s" % (function["fill_opacity"], function["fill_opacity"])




            if function["type"] == 'yfx':
                if all_pattern_options != '':
                    if function["between"] != -1:
                        return_string += '\\begin{scope}\n'
                        return_string += '\\tkzFct[%s]{%s}\n' % (options,function["def"])
                        func = get_item_from_id(eucl, function["between"], 'f')
                        return_string += '\\tkzFct[domain=%s:%s, samples=%s]{%s}\n' % (eval(func["domain_start"]), eval(func["domain_end"]), func["samples"], func["def"])
                        return_string += '\\tkzDrawAreafg[between= a and b, %s, domain=%s:%s]\n' % (all_pattern_options, eval(function["area_start"]),eval(function["area_end"]))
                        return_string += '\\end{scope}\n'

                return_string += '\\tkzFct[%s]{%s}\n' % (options,function["def"])
                if all_pattern_options != '' and function["between"] == -1:
                    return_string += '\\tkzDrawArea[%s, domain=%s:%s]\n' % (all_pattern_options, eval(function["area_start"]),eval(function["area_end"]))
            elif function["type"] == 'polar':
                return_string += '\\tkzFctPolar[%s]{%s}\n' % (options+', '+all_pattern_options,function["def"])
            elif function["type"] == 'parametric':
                func = function["def"].split('||')
                return_string += '\\tkzFctPar[%s]{%s}{%s}\n' % (options+', '+all_pattern_options, func[0], func[1])



            if function["type"] == 'yfx':
                if function["sum"]["type"] != DEFAULT_FUNCTION_TYPE:
                    options = 'interval=%s:%s, number=%s' % (eval(function["sum"]["start"]), eval(function["sum"]["end"]), function["sum"]["number"])
                    options += ", draw=%s" % function["sum"]["line_colour_name"]
                    if function["sum"]["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                        options += "!%s" % function["sum"]["line_strength"]

                    if function["sum"]["fill_colour_name"] != 'same':
                        if options != "":
                            options += ", "
                        options += "fill=%s" % function["sum"]["fill_colour_name"]
                        if function["sum"]["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                            options += "!%s" % function["sum"]["fill_strength"]

                        options += ", fill opacity=%s" % function["sum"]["fill_opacity"]

                    if function["sum"]["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
                        if options != "":
                            options += ", "
                        options += "draw opacity=%s" % function["sum"]["line_opacity"]


                    if function["sum"]["type"] == 'sup':
                        return_string += '\\tkzDrawRiemannSumSup[%s]' % options
                    if function["sum"]["type"] == 'inf':
                        return_string += '\\tkzDrawRiemannSumInf[%s]' % options
                    if function["sum"]["type"] == 'mid':
                        return_string += '\\tkzDrawRiemannSumMid[%s]' % options

            return_string += '\\end{scope}\n'
    if return_string != '':
        return_string = '%FUNCTIONS\n' + return_string
    return return_string


def tikzify_segments(eucl):
    return_string = ''
    for segment in eucl["segments"]:
        if segment["show"] and segment["id"] != 'sg_default':
            options = ''
            if segment["line_colour_name"] != DEFAULT_SEGMENT_LINE_COLOUR_NAME or\
               segment["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                # if options != "":
                #     options += ", "
                options += "draw=%s" % segment["line_colour_name"]
                if segment["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                    options += "!%s" % segment["line_strength"]
            if segment["line_stroke"] != DEFAULT_SEGMENT_LINE_STROKE:
                if options != "":
                    options += ", "
                if segment["line_stroke"] == "custom":
                    options += "dash pattern=%s" % line_stroke_custom_to_tkz(segment["line_stroke_custom"])
                else:
                    options += str(segment["line_stroke"])
            if segment["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                if options != "":
                    options += ", "
                options += "line width=%s pt" % segment["line_width"]
            if segment["line_opacity"] != DEFAULT_SEGMENT_LINE_OPACITY:
                if options != "":
                    options += ", "
                options += "draw opacity=%s, fill opacity=%s" % (segment["line_opacity"], segment["line_opacity"])
            if segment["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP or\
               segment["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                if options != "":
                    options += ", "
                if segment["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP:
                    o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(segment["o_arrow"]["tip"])
                    if segment["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += "scale length=%f" % segment["o_arrow"]["length"]
                    if segment["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += "scale width=%f" % segment["o_arrow"]["width"]
                    if segment["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += segment["o_arrow"]["side"]
                    if segment["o_arrow"]["reversed"]:
                        if o_arrow_options != "":
                            o_arrow_options += ", "
                        o_arrow_options += "reversed"
                if segment["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    d_arrow_name, d_arrow_options = arrow_tip_to_tkz_option(segment["d_arrow"]["tip"])
                    if segment["d_arrow"]["length"] != DEFAULT_SEGMENT_D_ARROW_LENGTH:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += "scale length=%f" % segment["d_arrow"]["length"]
                    if segment["d_arrow"]["width"] != DEFAULT_SEGMENT_D_ARROW_WIDTH:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += "scale width=%f" % segment["d_arrow"]["width"]
                    if segment["d_arrow"]["side"] != DEFAULT_SEGMENT_D_ARROW_SIDE:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += segment["d_arrow"]["side"]
                    if segment["d_arrow"]["reversed"]:
                        if d_arrow_options != "":
                            d_arrow_options += ", "
                        d_arrow_options += "reversed"

                if segment["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP and\
                   segment["d_arrow"]["tip"] == DEFAULT_SEGMENT_D_ARROW_TIP:
                    options += "arrows={%s[%s]-}" % (o_arrow_name, o_arrow_options)
                elif segment["o_arrow"]["tip"] == DEFAULT_SEGMENT_O_ARROW_TIP and\
                   segment["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    options += "arrows={-%s[%s]}" % (d_arrow_name, d_arrow_options)
                else:
                    options += "arrows={%s[%s]-%s[%s]}" % (o_arrow_name, o_arrow_options, d_arrow_name, d_arrow_options)

            if segment["extension"]["origin"] != DEFAULT_SEGMENT_O_EXTENSION or\
               segment["extension"]["destination"] != DEFAULT_SEGMENT_D_EXTENSION:
                if options != "":
                    options += ", "
                options += "add=%f and %f" % (segment["extension"]["origin"], segment["extension"]["destination"])


            if segment["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                return_string += "\\begin{scope}\n"
            if options == '':
                return_string += "\\tkzDrawSegment(%s,%s)\n" % (segment["points"]["from"], segment["points"]["to"])
            else:
                return_string += "\\tkzDrawSegment[%s](%s,%s)\n" % (options, segment["points"]["from"], segment["points"]["to"])
            if segment["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                return_string += "\\end{scope}\n"
    if return_string != '':
        return_string = '%SEGMENTS\n' + return_string
    return return_string


def tikzify_segment_marks(eucl):
    return_string = ''
    for segment in eucl["segments"]:
        if segment["id"] == 'sg_default':
            continue
        if segment["mark"]["symbol"] != DEFAULT_SEGMENT_MARK_SYMBOL:
            if segment["mark"]["width"] != DEFAULT_SEGMENT_MARK_WIDTH or\
               (segment["mark"]["colour"] == DEFAULT_SEGMENT_MARK_COLOUR and\
               segment["line_opacity"] != DEFAULT_SEGMENT_LINE_OPACITY):
                options = ''
                if segment["mark"]["width"] != DEFAULT_SEGMENT_MARK_WIDTH:
                    options += "line width=%f" % segment["mark"]["width"]
                if segment["mark"]["colour"] == DEFAULT_SEGMENT_MARK_COLOUR and\
                   segment["line_opacity"] != DEFAULT_SEGMENT_LINE_OPACITY:
                    if options != "":
                        options += ", "
                    options += "fill opacity=%f, draw opacity=%f" % (segment["line_opacity"] ,segment["line_opacity"])

                return_string += "\\begin{scope}[%s]\n" % options
            options = ''
            options += "mark=%s" % segment["mark"]["symbol"]
            if segment["mark"]["size"] != DEFAULT_SEGMENT_MARK_SIZE:
                if options != "":
                    options += ", "
                options += "size=%s" % segment["mark"]["size"]
            if segment["mark"]["colour"] == DEFAULT_SEGMENT_MARK_COLOUR:
                if segment["line_colour_name"] != DEFAULT_SEGMENT_LINE_COLOUR_NAME or\
                   segment["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                    if options != "":
                        options += ", "
                    options += "color=%s" % segment["line_colour_name"]
                    if segment["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                        options += "!%s" % segment["line_strength"]
            else:
                if segment["mark"]["colour"] != DEFAULT_SEGMENT_LINE_COLOUR_NAME:
                    if options != "":
                        options += ", "
                    options += "color=%s" % segment["mark"]["colour"]
            if segment["mark"]["position"] != DEFAULT_SEGMENT_MARK_POSITION:
                if options != "":
                    options += ", "
                options += "pos=%s" % segment["mark"]["position"]

            return_string += "\\tkzMarkSegment[%s](%s,%s)" % (options, segment["points"]["from"], segment["points"]["to"])

            if segment["mark"]["width"] != DEFAULT_SEGMENT_MARK_WIDTH or\
               (segment["mark"]["colour"] == DEFAULT_SEGMENT_MARK_COLOUR and\
               segment["line_opacity"] != DEFAULT_SEGMENT_LINE_OPACITY):
                return_string += "\\end{scope}"
    if return_string != '':
        return_string = '%SEGMENT MARKS\n' + return_string
    return return_string


def tikzify_filled_angles(eucl):
    return_string = ''
    for angle in eucl["angles"]:
        if angle["id"] != 'ang_default' and angle["show"] and not angle["right_angle"]:
            if angle["fill_opacity"] != DEFAULT_ANGLE_FILL_OPACITY:
                return_string += "\\begin{scope}[fill opacity=%s]" % angle["fill_opacity"]
            options = 'size=%s, ' % angle["size"]
            if angle["fill_colour_name"] != DEFAULT_ANGLE_FILL_COLOUR_NAME:
                options += "fill=%s" % angle["fill_colour_name"]
                if angle["fill_strength"] != DEFAULT_ANGLE_FILL_STRENGTH:
                    options += "!%s" % angle["fill_strength"]
                return_string += "\\tkzFillAngle[%s](%s,%s,%s)\n" % (options, angle["points"]["A"], angle["points"]["B"], angle["points"]["C"])
            if angle["fill_opacity"] != DEFAULT_ANGLE_FILL_OPACITY:
                return_string += "\\end{scope}\n"
    if return_string != '':
        return_string = '%FILLED ANGLES\n' + return_string
    return return_string


def tikzify_angles(eucl):
    return_string = ''
    for angle in eucl["angles"]:
        if angle["id"] != 'ang_default' and angle["show"]:
            if angle["line_width"] != DEFAULT_ANGLE_LINE_WIDTH or\
               angle["line_opacity"] != DEFAULT_ANGLE_FILL_OPACITY:
                options = 'line width=%s' % angle["line_width"]
                if angle["line_opacity"] != DEFAULT_ANGLE_FILL_OPACITY:
                    options += ", draw opacity=%s" % angle["line_opacity"]
                return_string += "\\begin{scope}[%s]\n" % options
            options = ''
            if angle["right_angle"]:
                if angle["type"] != DEFAULT_RIGHT_ANGLE_TYPE:
                    options += 'german'
                if options != '':
                    options += ', '
                options += "size=%s" % (angle["size"])
                return_string += "\\tkzMarkRightAngle[%s](%s,%s,%s)\n" % (options, angle["points"]["A"], angle["points"]["B"], angle["points"]["C"])
            else:
                options += "size=%s cm" % (angle["size"])
                if angle["arc"] != DEFAULT_ANGLE_ARC:
                    if options != '':
                        options += ', '
                    options += "arc=%s" % (angle["arc"] * 'l')

                if options != '':
                    options += ', '
                options += "mark=%s" % angle["mksymbol"]

                if angle["mksize"] != DEFAULT_ANGLE_MARK_SIZE:
                    if options != '':
                        options += ', '
                    options += "mksize=%s pt" % angle["mksize"]
                if angle["mkcolour"] != DEFAULT_ANGLE_MARK_COLOUR:
                    if options != '':
                        options += ', '
                    options += "mkcolor=%s" % angle["mkcolour"]
                if angle["mkpos"] != DEFAULT_ANGLE_MARK_POSITION:
                    if options != '':
                        options += ', '
                    options += "mkpos=%s" % angle["mkpos"]
                if angle["line_colour_name"] != DEFAULT_ANGLE_LINE_COLOUR_NAME or\
                   angle["line_strength"] != DEFAULT_ANGLE_LINE_STRENGTH:
                    if options != "":
                        options += ", "
                    options += "color=%s" % angle["line_colour_name"]
                    if angle["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
                        options += "!%s" % angle["line_strength"]
                if angle["line_stroke"] != DEFAULT_ANGLE_LINE_STROKE:
                    if options != "":
                        options += ", "
                    if angle["line_stroke"] == "custom":
                        options += "dash pattern=%s" % line_stroke_custom_to_tkz(angle["line_stroke_custom"])
                    else:
                        options += str(angle["line_stroke"])
                if angle["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP or\
                   angle["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    if options != "":
                        options += ", "
                    if angle["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP:
                        o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(angle["o_arrow"]["tip"])
                        if angle["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "scale length=%f" % angle["o_arrow"]["length"]
                        if angle["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "scale width=%f" % angle["o_arrow"]["width"]
                        if angle["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += angle["o_arrow"]["side"]
                        if angle["o_arrow"]["reversed"]:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "reversed"
                    if angle["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                        d_arrow_name, d_arrow_options = arrow_tip_to_tkz_option(angle["d_arrow"]["tip"])
                        if angle["d_arrow"]["length"] != DEFAULT_SEGMENT_D_ARROW_LENGTH:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "scale length=%f" % angle["d_arrow"]["length"]
                        if angle["d_arrow"]["width"] != DEFAULT_SEGMENT_D_ARROW_WIDTH:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "scale width=%f" % angle["d_arrow"]["width"]
                        if angle["d_arrow"]["side"] != DEFAULT_SEGMENT_D_ARROW_SIDE:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += angle["d_arrow"]["side"]
                        if angle["d_arrow"]["reversed"]:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "reversed"

                    if angle["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP and\
                       angle["d_arrow"]["tip"] == DEFAULT_SEGMENT_D_ARROW_TIP:
                        options += "arrows={%s[%s]-}" % (o_arrow_name, o_arrow_options)
                    elif angle["o_arrow"]["tip"] == DEFAULT_SEGMENT_O_ARROW_TIP and\
                       angle["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                        options += "arrows={-%s[%s]}" % (d_arrow_name, d_arrow_options)
                    else:
                        options += "arrows={%s[%s]-%s[%s]}" % (o_arrow_name, o_arrow_options, d_arrow_name, d_arrow_options)

                return_string += "\\tkzMarkAngle[%s](%s,%s,%s)\n" % (options, angle["points"]["A"], angle["points"]["B"], angle["points"]["C"])
            if angle["line_width"] != DEFAULT_ANGLE_LINE_WIDTH or\
               angle["line_opacity"] != DEFAULT_ANGLE_FILL_OPACITY:
                return_string += "\\end{scope}\n"
    if return_string != '':
        return_string = '%ANGLES\n' + return_string
    return return_string


def tikzify_angle_labels(eucl):
    return_string = ''
    for angle in eucl["angles"]:
        if angle["id"] != 'ang_default' and angle["label"]["show"]:
            options = ""
            if angle["label"]["distance"] != DEFAULT_ANGLE_LABEL_DISTANCE:
                options += "pos=%s" % angle["label"]["distance"]
            if angle["label"]["anchor"] != DEFAULT_ANGLE_LABEL_ANCHOR:
                if options != '':
                    options += ', '
                options += "%s" % angle["label"]["anchor"]

            return_string += "\\tkzLabelAngle[%s](%s,%s,%s){%s}" % (options, angle["points"]["A"], angle["points"]["B"], angle["points"]["C"], angle["label"]["text"])
    if return_string != '':
        return_string = '%ANGLE LABELS\n' + return_string
    return return_string


def tikzify_segment_labels(eucl):
    return_string = ''
    for segment in eucl["segments"]:
        if segment["id"] == 'sg_default':
            continue
        if segment["label"]["show"]:
            options = ''
            if segment["label"]["anchor"] != DEFAULT_SEGMENT_LABEL_ANCHOR:
                options += "%s" % segment["label"]["anchor"]
            if segment["label"]["position"] != DEFAULT_SEGMENT_LABEL_POSITION:
                if options != "":
                    options += ", "
                options += "pos=%s" % segment["label"]["position"]
            if segment["label"]["angle"] != DEFAULT_SEGMENT_LABEL_ANGLE or\
               segment["label"]["distance"] != DEFAULT_SEGMENT_LABEL_DISTANCE:
                if options != "":
                    options += ", "
                options += "shift={(%s:%s)}" % (segment["label"]["angle"], segment["label"]["distance"])

            if options == ' ':
                return_string += "\\tkzLabelSegment(%s,%s){%s}\n" % (segment["points"]["from"], segment["points"]["to"], segment["label"]["text"])
            else:
                return_string += "\\tkzLabelSegment[%s](%s,%s){%s}\n" % (options, segment["points"]["from"], segment["points"]["to"], segment["label"]["text"])
    if return_string != '':
        return_string = '%SEGMENT LABELS\n' + return_string
    return return_string


def tikzify_circles(eucl):
    return_string = ''
    for circle in eucl["circles"]:
        if circle["show"] and circle["id"] != 'crc_default':
            if circle["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                return_string += '\\begin{scope}\n'

            options = ''

            if circle["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                options += 'line width=%s' % circle["line_width"]

            if circle["fill_opacity"] != DEFAULT_POINT_FILL_OPACITY:
                if options != '':
                    options += ', '
                options += 'fill opacity=%s' % circle["fill_opacity"]

            if circle["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
                if options != '':
                    options += ', '
                options += 'draw opacity=%s' % circle["line_opacity"]


            if circle["line_stroke"] != DEFAULT_ANGLE_LINE_STROKE:
                if options != '':
                    options += ', '
                if circle["line_stroke"] == "custom":
                    options += "dash pattern=%s" % line_stroke_custom_to_tkz(circle["line_stroke_custom"])
                else:
                    options += str(circle["line_stroke"])


            if options != "":
                options += ", "
            options += "draw=%s" % circle["line_colour_name"]
            if circle["line_strength"] != DEFAULT_SEGMENT_LINE_STRENGTH:
                options += "!%s" % circle["line_strength"]

            if circle["pattern"]["type"] == 'solid':
                if options != "":
                    options += ", "
                options += "fill=%s" % circle["fill_colour_name"]
                if circle["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                    options += "!%s" % circle["fill_strength"]

            if circle["type"] == 'arc':
                if circle["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP or\
                   circle["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                    if options != "":
                        options += ", "
                    if circle["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP:
                        o_arrow_name, o_arrow_options = arrow_tip_to_tkz_option(circle["o_arrow"]["tip"])
                        if circle["o_arrow"]["length"] != DEFAULT_SEGMENT_O_ARROW_LENGTH:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "scale length=%f" % circle["o_arrow"]["length"]
                        if circle["o_arrow"]["width"] != DEFAULT_SEGMENT_O_ARROW_WIDTH:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "scale width=%f" % circle["o_arrow"]["width"]
                        if circle["o_arrow"]["side"] != DEFAULT_SEGMENT_O_ARROW_SIDE:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += circle["o_arrow"]["side"]
                        if circle["o_arrow"]["reversed"]:
                            if o_arrow_options != "":
                                o_arrow_options += ", "
                            o_arrow_options += "reversed"
                    if circle["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                        d_arrow_name, d_arrow_options = arrow_tip_to_tkz_option(circle["d_arrow"]["tip"])
                        if circle["d_arrow"]["length"] != DEFAULT_SEGMENT_D_ARROW_LENGTH:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "scale length=%f" % circle["d_arrow"]["length"]
                        if circle["d_arrow"]["width"] != DEFAULT_SEGMENT_D_ARROW_WIDTH:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "scale width=%f" % circle["d_arrow"]["width"]
                        if circle["d_arrow"]["side"] != DEFAULT_SEGMENT_D_ARROW_SIDE:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += circle["d_arrow"]["side"]
                        if circle["d_arrow"]["reversed"]:
                            if d_arrow_options != "":
                                d_arrow_options += ", "
                            d_arrow_options += "reversed"

                    if circle["o_arrow"]["tip"] != DEFAULT_SEGMENT_O_ARROW_TIP and\
                       circle["d_arrow"]["tip"] == DEFAULT_SEGMENT_D_ARROW_TIP:
                        options += "arrows={%s[%s]-}" % (o_arrow_name, o_arrow_options)
                    elif circle["o_arrow"]["tip"] == DEFAULT_SEGMENT_O_ARROW_TIP and\
                       circle["d_arrow"]["tip"] != DEFAULT_SEGMENT_D_ARROW_TIP:
                        options += "arrows={-%s[%s]}" % (d_arrow_name, d_arrow_options)
                    else:
                        options += "arrows={%s[%s]-%s[%s]}" % (o_arrow_name, o_arrow_options, d_arrow_name, d_arrow_options)


            if not circle["pattern"]["type"] in ['none', 'solid']:
                if circle["fill_colour_name"] != DEFAULT_POINT_FILL_COLOUR_NAME or\
                   circle["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                    if options != "":
                        options += ", "
                    options += "pattern color=%s" % circle["fill_colour_name"]
                    if circle["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                        options += "!%s" % circle["fill_strength"]
                if options != '':
                    options += ', '
                if not circle["pattern"]["type"] in\
                   ['Lines', 'Hatch', 'Dots', 'Fivepointed stars', 'Sixpointed stars']:
                    options += 'pattern=%s' % circle["pattern"]["type"]
                else:
                    pattern_options = ''
                    if circle["pattern"]["rotation"] != DEFAULT_PATTERN_ROTATION:
                        pattern_options += 'angle=%s' % circle["pattern"]["rotation"]
                    if circle["pattern"]["distance"] != DEFAULT_PATTERN_DISTANCE:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'distance=%s' % circle["pattern"]["distance"]
                        if circle["pattern"]["type"] in ['Fivepointed stars', 'Sixpointed stars']:
                            pattern_options += ' mm'
                    if circle["pattern"]["xshift"] != DEFAULT_PATTERN_XSHIFT:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'xshift=%s' % circle["pattern"]["xshift"]
                    if circle["pattern"]["yshift"] != DEFAULT_PATTERN_YSHIFT:
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'yshift=%s' % circle["pattern"]["yshift"]
                    if circle["pattern"]["type"] in ['Dots', 'Fivepointed stars', 'Sixpointed stars']:
                        if circle["pattern"]["size"] != DEFAULT_PATTERN_SIZE:
                            if pattern_options != '':
                                pattern_options += ', '
                            pattern_options += 'radius=%s mm' % circle["pattern"]["size"]
                    else:
                        if circle["pattern"]["size"] != DEFAULT_PATTERN_SIZE:
                            if pattern_options != '':
                                pattern_options += ', '
                            pattern_options += 'line width=%s' % circle["pattern"]["size"]
                    if circle["pattern"]["type"] == 'Fivepointed stars':
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'points=5'
                    if circle["pattern"]["type"] == 'Sixpointed stars':
                        if pattern_options != '':
                            pattern_options += ', '
                        pattern_options += 'points=6'
                    if circle["pattern"]["type"] in ['Sixpointed stars', 'Fivepointed stars']:
                        options += 'pattern={Stars[%s]}' % pattern_options
                    else:
                        options += 'pattern={%s[%s]}' % (circle["pattern"]["type"], pattern_options)


            if circle["type"] == "circum_circle" and circle["id"] != 'crc_default':
                if options == '':
                    return_string += "\\tkzDrawCircle[circum](%s,%s,%s)\n" % (circle["points"]["A"], circle["points"]["B"],circle["points"]["C"])
                else:
                    return_string += "\\tkzDrawCircle[circum, %s](%s,%s,%s)\n" % (options, circle["points"]["A"], circle["points"]["B"],circle["points"]["C"])

            if circle["type"] == "two_point_circle" and circle["id"] != 'crc_default':
                if options == '':
                    return_string += "\\tkzDrawCircle(%s,%s)\n" % (circle["points"]["O"], circle["points"]["A"])
                else:
                    return_string += "\\tkzDrawCircle[%s](%s,%s)\n" % (options, circle["points"]["O"], circle["points"]["A"])

            if circle["type"] == "inscribed_circle" and circle["id"] != 'crc_default':
                if options == '':
                    return_string += "\\tkzDrawCircle[in](%s,%s,%s)\n" % (circle["points"]["A"], circle["points"]["B"],circle["points"]["C"])
                else:
                    return_string += "\\tkzDrawCircle[in, %s](%s,%s,%s)\n" % (options, circle["points"]["A"], circle["points"]["B"],circle["points"]["C"])
            if circle["type"] == "arc" and circle["id"] != 'crc_default':
                if options == '':
                    return_string += "\\tkzDrawArc(%s,%s)(%s)\n" % (circle["points"]["O"], circle["points"]["A"],circle["points"]["B"])
                else:
                    return_string += "\\tkzDrawArc[%s](%s,%s)(%s)\n" % (options, circle["points"]["O"], circle["points"]["A"],circle["points"]["B"])
            if circle["type"] == "sector" and circle["id"] != 'crc_default':
                if options == '':
                    return_string += "\\tkzDrawSector(%s,%s)(%s)\n" % (circle["points"]["O"], circle["points"]["A"],circle["points"]["B"])
                else:
                    return_string += "\\tkzDrawSector[%s](%s,%s)(%s)\n" % (options, circle["points"]["O"], circle["points"]["A"],circle["points"]["B"])

            if circle["line_width"] != DEFAULT_SEGMENT_LINE_WIDTH:
                return_string += '\\end{scope}'
    if return_string != '':
        return_string = '%CIRCLES\n' + return_string
    return return_string


def tikzify_circle_labels(eucl):
    return_string = ''
    for circle in eucl["circles"]:
        if circle["label"]["show"] and circle["id"] != 'crc_default':
            options = ''
            if circle["label"]["anchor"] != DEFAULT_POINT_LABEL_ANCHOR:
                options += circle["label"]["anchor"]
            if options != '':
                options = 'R, ' + options
            else:
                options = 'R'

            if circle["type"] in ['two_point_circle', 'sector', 'arc']:
                return_string += '\\tkzCalcLength[cm](%s,%s)\n' % (circle["points"]["O"], circle["points"]["A"])
                return_string += "\\tkzLabelCircle[%s](%s,\\tkzLengthResult cm * %s)(%s){%s}\n" % (options, circle["points"]["O"], circle["label"]["distance"], circle["label"]["angle"], circle["label"]["text"])
            if circle["type"] in ['circum_circle', 'inscribed_circle']:
                option = ''
                if circle["type"] == 'circum_circle':
                    option = 'circum'
                if circle["type"] == 'inscribed_circle':
                    option = 'in'

                return_string += '\\tkzDefCircle[%s](%s,%s,%s)\\tkzGetPoint{eucl@temp}\n' % (option, circle["points"]["A"], circle["points"]["B"], circle["points"]["C"])
                return_string += '\\tkzLabelCircle[%s](eucl@temp, \\tkzLengthResult pt * %s)(%s){%s}\n' % (options, circle["label"]["distance"], circle["label"]["angle"], circle["label"]["text"])
    if return_string != '':
        return_string = '%CIRCLE LABELS\n' + return_string
    return return_string


def tikzify_points(eucl):
    return_string = ''
    for point in eucl["points"]:
        if point["show"] == True and point["id"] != 'pt_default':
            if point["line_width"] != DEFAULT_POINT_LINE_WIDTH or\
               point["fill_opacity"] != DEFAULT_POINT_FILL_OPACITY or\
               point["line_opacity"] != DEFAULT_POINT_LINE_OPACITY or\
               point["line_stroke"] != DEFAULT_POINT_LINE_STROKE:
                options = ""
                if point["line_width"] != DEFAULT_POINT_LINE_WIDTH:
                    options += "line width=%s pt" % point["line_width"]
                if point["fill_opacity"] != DEFAULT_POINT_FILL_OPACITY:
                    if options != "":
                        options += ", "
                    options += "fill opacity=%s" % point["fill_opacity"]
                if point["line_opacity"] != DEFAULT_POINT_LINE_OPACITY:
                    if options != "":
                        options += ", "
                    options += "draw opacity=%s" % point["line_opacity"]
                if point["line_stroke"] != DEFAULT_POINT_LINE_STROKE:
                    if options != "":
                        options += ", "
                    if point["line_stroke"] == "custom":
                        options += "dash pattern=%s" % line_stroke_custom_to_tkz(point["line_stroke_custom"])
                    else:
                        options += str(point["line_stroke"])
                return_string += "\\begin{scope}[%s]" % options

            options = ""
            if point["fill_colour_name"] != DEFAULT_POINT_FILL_COLOUR_NAME or\
               point["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                options += "fill=%s" % point["fill_colour_name"]
                if point["fill_strength"] != DEFAULT_POINT_FILL_STRENGTH:
                    options += "!%s" % point["fill_strength"]
            if point["line_colour_name"] != DEFAULT_POINT_LINE_COLOUR_NAME or\
               point["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
                if options != "":
                    options += ", "
                options += "draw=%s" % point["line_colour_name"]
                if point["line_strength"] != DEFAULT_POINT_LINE_STRENGTH:
                    options += "!%s" % point["line_strength"]
            if point["size"] != DEFAULT_POINT_SIZE:
                if options != "":
                    options += ", "
                options += "size=%s" % point["size"]
            if options == '':
                return_string += "\\tkzDrawPoint(%s)\n" % (point["id"])
            else:
                return_string += "\\tkzDrawPoint[%s](%s)\n" % (options, point["id"])

            if point["line_width"] != DEFAULT_POINT_LINE_WIDTH or\
               point["fill_opacity"] != DEFAULT_POINT_FILL_OPACITY or\
               point["line_opacity"] != DEFAULT_POINT_LINE_OPACITY or\
               point["line_stroke"] != DEFAULT_POINT_LINE_STROKE:
                return_string += "\\end{scope}\n"
    if return_string != '':
        return_string = '%POINTS\n' + return_string
    return return_string


def tikzify_point_labels(eucl):
    return_string = ''
    for point in eucl["points"]:
        if point["label"]["show"] == True and point["id"] != 'pt_default':
            options = ""
            if point["duck"]["show"]:
                options += 'centered'
            elif point["label"]["anchor"] != DEFAULT_POINT_LABEL_ANCHOR:
                options += "%s" % point["label"]["anchor"]
            if point["label"]["angle"] != DEFAULT_POINT_LABEL_ANGLE or\
               point["label"]["distance"] != DEFAULT_POINT_LABEL_DISTANCE:
                if options != "":
                    options += ", "
                options += "shift={(%s:%s)}" % (point["label"]["angle"], point["label"]["distance"])

            if point["duck"]["show"]:
                text = tikzify_duck_commands(point)
            else:
                text = point["label"]["text"]
            if options == "":
                return_string += "\\tkzLabelPoint(%s){%s}\n" % (point["id"], text)
            else:
                return_string += "\\tkzLabelPoint[%s](%s){%s}\n" % (options, point["id"], text)
    if return_string != '':
        return_string = '%POINT LABELS\n' + return_string
    return return_string


def tikzify_finalise(eucl):
    return "\\end{tikzpicture}\n"


def tikzify_duck_commands(point):
    duck = point["duck"]
    if duck["type"] == 'random':
        return "\\begin{tikzpicture}[scale=%s]\\randuck\\end{tikzpicture}" % duck["size"]

    if duck["type"] == 'special':
        return "\\%s{%s}" % (duck["special"], duck["size"])

    if duck["type"] == 'chess':
        if duck["chess"][0] == 'w':
            return "\\%s{%s}{%s}" % (duck["chess"][1:], duck["size"], 'light')
        else:
            return "\\%s{%s}{%s}" % (duck["chess"][1:], duck["size"], 'dark')

    if duck["type"] == 'custom':
        options = ''

        if duck["bill"] != 'sweet':
            if duck["bill"] == 'vampire':
                options += 'vampire=white, laughing'
            else:
                options += duck["bill"]
        if duck["body_colour"] != 'default':
            if options != '':
                options += ', '
            options += 'body=%s' % duck["body_colour"]
        if duck["bill_colour"] != 'default':
            if options != '':
                options += ', '
            options += 'bill=%s' % duck["bill_colour"]
        if duck["hair"] != 'none':
            if options != '':
                options += ', '
            options += duck["hair"]
            if duck["hair_colour"] != 'default':
                options += '=%s' % duck["hair_colour"]
        if duck["glasses"] != 'none':
            if options != '':
                options += ', '
            options += duck["glasses"]
            if duck["glasses_colour"] != 'default':
                options += '=%s' % duck["glasses_colour"]
        if duck["hat"] != 'none':
            if options != '':
                options += ', '
            options += duck["hat"]
            if duck["hat_colour"] != 'default':
                options += '=%s' % duck["hat_colour"]
            if duck["hat"] in DUCK_EXTRA:
                if duck["hat_extra_colour"] != 'default':
                    options += ', %s=%s' % (DUCK_EXTRA[duck["hat"]], duck["hat_extra_colour"])

        if duck["necklace"] != 'none':
            if options != '':
                options += ', '
            options += duck["necklace"]
            if duck["necklace_colour"] != 'default':
                options += '=%s' % duck["necklace_colour"]
        if duck["accessories"] != 'none':
            if options != '':
                options += ', '
            options += duck["accessories"]
            if duck["accessories"] == 'signpost':
                if duck["accessories_text"] != '':
                    options += '=\\scalebox{%s}{%s}' % (duck["size"]*0.3, duck["accessories_text"])
                if duck["accessories_colour"] != 'default':
                    options += ', signback=%s' % duck["accessories_colour"]
            elif duck["accessories"] == 'book':
                if duck["accessories_text"] != '':
                    options += '=\\scalebox{%s}{%s}' % (duck["size"]*0.3, duck["accessories_text"])
                if duck["accessories_colour"] != 'default':
                    options += ', bookcolour=%s' % duck["accessories_colour"]
            else:
                if duck["accessories_colour"] != 'default':
                    options += '=%s' % duck["accessories_colour"]

            if duck["accessories"] in DUCK_EXTRA:
                if duck["accessories_extra_colour"] != 'default':
                    options += ', %s=%s' % (DUCK_EXTRA[duck["accessories"]], duck["accessories_extra_colour"])

        if duck["water"][0] == 'T':
            if options != '':
                options += ', '
            options += "water"
            if duck["water"][2:] != 'default':
                options += '=%s' % duck["water"][2:]
        if duck["eyebrows"][0] == 'T':
            if options != '':
                options += ', '
            options += "eyebrow"
            if duck["eyebrows"][2:] != 'default':
                options += '=%s' % duck["eyebrows"][2:]
        if duck["beard"][0] == 'T':
            if options != '':
                options += ', '
            options += "beard"
            if duck["beard"][2:] != 'default':
                options += '=%s' % duck["beard"][2:]
        if duck["buttons"][0] == 'T':
            if options != '':
                options += ', '
            options += "buttons"
            if duck["buttons"][2:] != 'default':
                options += '=%s' % duck["buttons"][2:]
        if duck["lapel"][0] == 'T':
            if options != '':
                options += ', '
            options += "lapel"
            if duck["lapel"][2:] != 'default':
                options += '=%s' % duck["lapel"][2:]
        if duck["horsetail"][0] == 'T':
            if options != '':
                options += ', '
            options += "horsetail"
            if duck["horsetail"][2:] != 'default':
                options += '=%s' % duck["horsetail"][2:]

        if duck["clothing"]["tshirt"][0] == 'T':
            if options != '':
                options += ', '
            options += "tshirt"
            if duck["clothing"]["tshirt"][2:] != 'default':
                options += '=%s' % duck["clothing"]["tshirt"][2:]
        if duck["clothing"]["jacket"][0] == 'T':
            if options != '':
                options += ', '
            options += "jacket"
            if duck["clothing"]["jacket"][2:] != 'default':
                options += '=%s' % duck["clothing"]["jacket"][2:]
        if duck["clothing"]["tie"][0] == 'T':
            if options != '':
                options += ', '
            options += "tie"
            if duck["clothing"]["tie"][2:] != 'default':
                options += '=%s' % duck["clothing"]["tie"][2:]
        if duck["clothing"]["bowtie"][0] == 'T':
            if options != '':
                options += ', '
            options += "bowtie"
            if duck["clothing"]["bowtie"][2:] != 'default':
                options += '=%s' % duck["clothing"]["bowtie"][2:]
        if duck["clothing"]["aodai"][0] == 'T':
            if options != '':
                options += ', '
            options += "aodai"
            if duck["clothing"]["aodai"][2:] != 'default':
                options += '=%s' % duck["clothing"]["aodai"][2:]
        if duck["clothing"]["cape"][0] == 'T':
            if options != '':
                options += ', '
            options += "cape"
            if duck["clothing"]["cape"][2:] != 'default':
                options += '=%s' % duck["clothing"]["cape"][2:]

        if duck["thought"] != 'none':
            if options != '':
                options += ', '
            options += duck["thought"]
            if duck["thought_text"] != '':
                options += '=\\scalebox{%s}{%s}' % (duck["size"]*0.3, duck["thought_text"])
            if duck["thought_colour"] != 'default':
                options += ', bubblecolour=%s' % duck["thought_colour"]


        return "\\begin{tikzpicture}[scale=%s]\\duck[%s]\\end{tikzpicture}" % (duck["size"],options)


#lbs stands for left/bottom/scale while tblr is for top/bottom/left/right
def eucl2tkz(eucl, lbs, tblr=None):
    left, bottom, scale = lbs
    right, top, margin = (left + 10 * scale, bottom + 10 * scale, scale * 1.3)
    if tblr is not None:
        top, bottom, left, right = tblr

    return_string = tikzify_duck_new_commands(eucl)
    if return_string != '':
        return_string = '%TIKZDUCKS NEWCOMMANDS\n' + return_string + '\n'

    if eucl["code_before"] != '':
        return_string += '%CUSTOM PRECEEDING CODE\n' + eucl["code_before"] + '\n'
    return_string += tikzify_init(eucl, margin, top, bottom, left, right)
    grid = tikzify_grid(eucl)
    if eucl["axis_x"]["show"] or eucl["axis_y"]["show"]:
        return_string += tikzify_grid_with_any_axis(eucl, grid)
        return_string += tikzify_x_axis(eucl)
        return_string += tikzify_y_axis(eucl)
        return_string += tikzify_axis_clip(eucl)
    else:
        return_string += tikzify_grid_without_axis(eucl, grid)
    return_string += tikzify_all_point_declarations(eucl)
    return_string += tikzify_polygons_and_linestrings(eucl)
    return_string += tikzify_functions(eucl)
    return_string += tikzify_segments(eucl)
    return_string += tikzify_segment_marks(eucl)
    return_string += tikzify_filled_angles(eucl)
    return_string += tikzify_angles(eucl)
    return_string += tikzify_circles(eucl)
    return_string += tikzify_angle_labels(eucl)
    return_string += tikzify_segment_labels(eucl)
    return_string += tikzify_circle_labels(eucl)
    return_string += tikzify_points(eucl)
    return_string += tikzify_point_labels(eucl)
    if eucl["code_after"] != '':
        return_string += '%CUSTOM FOLLOWING CODE\n' + eucl["code_after"] + '\n'
    return_string += tikzify_finalise(eucl)
    return return_string


def tkz2tex(eucl, tkz_string):
    return_string  = "\\documentclass[tikz]{standalone}\n"
    return_string += '\n'.join(eucl["packages"]) + '\n'
    # return_string += "\\usetkzobj{all}\n"
    return_string += "\\begin{document}\n"
    return_string += tkz_string
    return_string += "\\end{document}\n"
    return return_string
