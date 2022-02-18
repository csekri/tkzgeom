from enum import Enum, auto, unique

def attribute_values(class_input):
    return [m for v, m in vars(class_input).items() if not (v.startswith('_')  or callable(m))]

class MouseState:
    UP = 0
    DOWN = 1

class MouseButton:
    LEFT = 0
    RIGHT = 1

class Colour:
    BLACK = 'black'
    BLUE = 'blue'
    BROWN = 'brown'
    CYAN = 'cyan'
    DARKGRAY = 'darkgray'
    GRAY = 'gray'
    GREEN = 'green'
    LIGHTGRAY = 'lightgray'
    LIME = 'lime'
    MAGENTA = 'magenta'
    OLIVE = 'olive'
    ORANGE = 'orange'
    PINK = 'pink'
    PURPLE = 'purple'
    RED = 'red'
    TEAL = 'teal'
    VIOLET = 'violet'
    WHITE = 'white'
    YELLOW = 'yellow'

class ArrowTips:
    NONE = 'None'
    STEALTH = 'Stealth'
    STEALTH_R = 'Stealth^r'
    STEALTH_O = 'Stealth^o'
    STEALTH_OR = 'Stealth^or'
    LESS = '<'
    GREATER = '>'
    LATEX = 'Latex'
    LATEX_R = 'Latex^r'
    LATEX_O = 'Latex^o'
    LATEX_OR = 'Latex^ro'
    TO = 'To'
    COMPUTER_MODERN_RIGHTARROW = 'Computer Modern Rightarrow'
    IMPLES = 'Implies'
    BUTT_CAP = 'Butt Cap'
    FAST_ROUND = 'Fast Round'
    FAST_TRIANGLE = 'Fast Triangle'
    ROUND_CAP = 'Round Cap'
    TRIANGLE_CAP = 'Triangle Cap'
    CIRCLE = 'Circle'
    CIRCLE_O = 'Circle^o'
    DIAMOND = 'Diamond'
    DIAMOND_O = 'Diamond^o'
    ELLIPSE = 'Ellipse'
    ELLIPSE_O = 'Ellipse^o'
    KITE = 'Kite'
    KITE_O = 'Kite^o'
    RECTANGLE = 'Rectangle'
    RECTANGLE_O = 'Rectangle^o'
    SQUARE = 'Square'
    SQUARE_O = 'Square^o'
    TRIANGLE = 'Triangle'
    TRIANGLE_O = 'Triangle^o'
    TURNED_SQUARE = 'Turned Square'
    TURNED_SQUARE_O = 'Turned Square^o'
    ARC_BARB = 'Arc Barb'
    BAR = 'Bar'
    BRACKET = 'Bracket'
    HOOKS = 'Hooks'
    PARENTHESIS = 'Parenthesis'
    STRAIGHT_BARB = 'Straight Barb'
    TEE_BARB = 'Tee Barb'


class ColourDefault:
    def __init__(self, name=Colour.BLACK, mix_with=Colour.BLACK, mix_ratio=0, strength=100, opacity=1.0):
        self.NAME = name
        self.MIX_WITH = mix_with
        self.MIX_RATIO = mix_ratio
        self.STRENGTH = strength
        self.OPACITY = opacity

class DoubleDefault:
    def __init__(self, distance=0.0, colour=ColourDefault()):
        self.DISTANCE = distance
        self.Colour = colour

class ArrowDefault:
    def __init__(self, tip=ArrowTips.NONE, width=1.0, length=1.0):
        self.TIP = tip
        self.WIDTH = width
        self.LENGTH = length

class FillPatternDefault:
    def __init__(self, type='none', distance=3.0, size=0.0, rotatio=0.0, xshift=0.0, yshift=0.0):
        self.TYPE = type
        self.DISTANCE = distance
        self.SIZE = size
        self.ROTATION = rotation
        self.XSHIFT = 0.0
        self.YSHIFT = 0.0


class Marker_Shape:
    CIRCLE = 'circle'
    RECTANGE = 'rectangle'
    REGULAR_POLYGON = 'regular polygon'
    STAR = 'star'
    DIAMOND = 'diamond'


class MarkerDefault:
    def __init__(self, size=3, shape=Marker_Shape.CIRCLE, shape_number=5, ratio=2.25, inner_sep=0.0, rounded_corners=0.0, text='', text_width=0.0):
        self.SIZE = 3
        self.SHAPE = shape
        self.SHAPE_NUMBER = shape_number
        self.RATIO = ratio
        self.INNER_SEP = inner_sep
        self.ROUNDED_CORNERS = 0.0
        self.TEXT = text
        self.TEXT_WIDTH = text_width


class Direction:
    NORTH = 'above'
    NORTH_EAST = 'above right'
    EAST = 'right'
    SOUTH_EAST = 'below right'
    SOUTH = 'below'
    SOUTH_WEST = 'below left'
    WEST = 'left'
    NORTH_WEST = 'above left'


class LabelDefault:
    def __init__(self, show=True, text='', anchor=Direction.SOUTH_EAST, offset=0.0):
        self.SHOW = show
        self.TEXT = text
        self.ANCHOR = anchor
        self.OFFSET = offset


class Line_Stroke:
    SOLID = 'solid'
    LOOSELY_DASHED = 'loosely dashed'
    DASHED = 'dashed'
    DENSELY_DASHED = 'densely dashed'
    LOOSELY_DOTTED = 'loosely dotted'
    DOTTED = 'dotted'
    DENSELY_DOTTED = 'densely dotted'
    LOOSELY_DASH_DOT = 'loosely dash dot'
    DASH_DOT = 'dash dot'
    DENSELY_DASH_DOT = 'densely dash dot'
    LOOSELY_DASH_DOT_DOT = 'loosely dash dot dot'
    DASH_DOT_DOT = 'dash dot dot'
    DENSELY_DASH_DOT_DOT = 'densely dash dot dot'
    CUSTOM = 'custom'


class Tool:
    FREE = 0
    MIDPOINT_SEGMENT = 1
    INTERSECT_POINT = 2
    CIRCLE_CENTRE = 3
    TRANSLATION = 4
    POINT_ON_LINE = 5
    POINT_ON_CIRCLE = 6
    ORTHOGONAL_PROJECTION = 7
    ORTHOGONAL = 8
    BISECTOR = 7
    ROTATION = 10
    MAKEGRID = 11

    SEGMENT_THROUGH = 100
    POLYGON = 101
    LINESTRING = 102

    CIRCUM_CIRCLE = 200
    TWO_POINT_CIRCLE = 201
    ARC = 202
    SECTOR = 203
    INSCRIBED_CIRCLE = 204

    MOVE_POINT = 300
    MOVE_AND_SCALE_CANVAS = 301

    MARK_ANGLE = 400
    MARK_RIGHT_ANGLE = 401
    # COMPASS = 402

    YFX_FUNCTION = 500
    POLAR_FUNCTION = 501
    PARAMETRIC_FUNCTION = 502

class Mode():
    POINT = 0
    SEGMENT = 1
    CIRCLE = 2
    MOVE = 3
    DECORATOR = 4


class Canvas:
    POINT_RADIUS = 7
    LINE_THICKNESS = 3
    CIRCLE_THICKNESS = 3
    MAX_DISTANCE_TO_HIGHLIGHT = 8

class Point:
    class Default:
        SIZE = 3.0
        LINE_WIDTH = 0.4
        NODE_INSIDE_TEXT = ''
        Fill_Colour = ColourDefault()
        Line_Colour = ColourDefault()
        Marker = MarkerDefault()
        Label = LabelDefault()
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]

    class Definition():
        FREE = 'free'
        INTERSECTION_LL = 'intersection_ll'
        INTERSECTION_LC = 'intersection_lc'
        CIRCLE_CENTRE = 'circle_centre'
        SEGMENT_MIDPOINT = 'segment_midpoint'
        ON_LINE = 'on_line'
        ON_CIRCLE = 'on_circle'
        PROJECTION = 'projection'
        BISECTOR = 'bisector'
        TRANSLATION = 'translation'
        PERPENDICULAR = 'perpendicular'
        ROTATION = 'rotation'

    TEXT_DICT = {
        Definition.FREE : "Free point.",
        Definition.INTERSECTION_LL : "Intersection point of line #1 and line #2.",
        Definition.INTERSECTION_LC : "Intersection point of line #1 and the #2.",
        Definition.CIRCLE_CENTRE : "The middle point of the #1.",
        Definition.SEGMENT_MIDPOINT : "The midpoint of segment #1.",
        Definition.ON_LINE : "The point defined as dilation of #1, by factor #2 across centre #3.",
        Definition.ON_CIRCLE : "The point on the #1 at angle #2.",
        Definition.PROJECTION : "The orthogonal projection of #1 on #2.",
        Definition.BISECTOR : "A point on the bisector of angle #1.",
        Definition.TRANSLATION : "The point given by translating point #1 with vector #2.",
        Definition.PERPENDICULAR : "A point on the perpendicular to segment #1 at #2.",
        Definition.ROTATION : "The point defined as the rotation of #1, by angle #2 around centre #3."
    }

# print(Point.TEXT_DICT[Point.Definition.FREE])
# print(attribute_values(Direction))

class Segment:
    class Default:
        LINE_WIDTH = 0.4
        Fill_Colour = ColourDefault()
        Line_Colour = ColourDefault()
        Marker = MarkerDefault()
        Label = LabelDefault()
        Double_Line = DoubleDefault()
        O_Arrow = ArrowDefault()
        D_Arrow = ArrowDefault()
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]

class Polygon:
    class Default:
        LINE_WIDTH = 0.4
        Fill_Colour = ColourDefault()
        Line_Colour = ColourDefault()
        Double_Line = DoubleDefault()
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]

PackagesDefault = [
    "\\usepackage{amsmath,amssymb}",
    "\\usepackage[utf8]{inputenc}",
    "\\usepackage[T1]{fontenc}",
    "\\usepackage{xcolor}",
    "\\usepackage{tkz-euclide,tkz-fct}",
    "\\usetikzlibrary{arrows.meta, patterns.meta, hobby, ducks}",
    "\\usetikzlibrary{backgrounds, decorations.pathmorphing, calc}"
]

BackGroundColourDefault = {
    "name": "black",
    "mix_with": "black",
    "mix_percent": 0,
    "strength": 0
}

WindowDefault = {
    "left": -5.0,
    "top": 5.0,
    "scale": 1.0,
}