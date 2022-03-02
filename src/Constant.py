"""Collection of constants"""

def attribute_values(class_input):
    """Turn class attribute values into a list."""
    return [m for v, m in vars(class_input).items() if not (v.startswith('_')  or callable(m))]


class MouseState: # TODO check if this is actually used anywhere, if so delete
    UP = 0
    DOWN = 1


class MouseButton: # TODO check if this is actually used anywhere, if so delete
    LEFT = 0
    RIGHT = 1


# The base colours in tikz, 19 colours altogether.
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


# The side visible of a tikz arrow (from arrows.meta).
class ArrowSide:
    BOTH = ''
    LEFT = 'left'
    RIGHT = 'right'


# The arrowtip types in tikz (from arrows.meta).
# The "^" character indicates that extra options are appended.
# "r" means rounded, "o" means open, "or" means both of the two.
class ArrowTip:
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
    LATEX_OR = 'Latex^or'
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


# Fill patterns supported by tikz (patterns).
class PatternType:
    NONE = 'none'
    SOLID = 'solid'
    HORIZONTAL_LINES = 'horizontal lines'
    VERTICAL_LINES = 'vertical lines'
    NORTH_EAST_LINES = 'north east lines'
    NORTH_WEST_LINES = 'north west lines'
    GRID = 'grid'
    CROSSHATCH = 'crosshatch'
    DOTS = 'dots'
    CROSSHATCH_DOTS = 'crosshatch dots'
    BRICKS = 'bricks'
    CHECKERBOARD = 'checkerboard'
    LINES = 'Lines'
    HATCH = 'Hatch'
    DOTS_EXTRA = 'Dots'
    FIVEPOINTED_STARS = 'Fivepointed stars'
    SIXPOINTED_STARS = 'Sixpointed stars'


# Parameters that define a colour.
class ColourDefault:
    def __init__(self, name=Colour.BLACK, mix_with=Colour.BLACK, mix_ratio=0, strength=100, opacity=1.0):
        self.NAME = name
        self.MIX_WITH = mix_with
        self.MIX_RATIO = mix_ratio
        self.STRENGTH = strength
        self.OPACITY = opacity


# Parameters that define the double line.
class DoubleDefault:
    def __init__(self, distance=0.0, colour=ColourDefault(name=Colour.WHITE)):
        self.DISTANCE = distance
        self.Colour = colour


# Parameters that define an arrow.
class ArrowDefault:
    def __init__(self, tip=ArrowTip.NONE, side=ArrowSide.BOTH, width=1.0, length=1.0, reversed=False, bending=False):
        self.TIP = tip
        self.WIDTH = width
        self.LENGTH = length
        self.BENDING = bending
        self.SIDE = side
        self.REVERSED = reversed


# Parameters that define a pattern.
class FillPatternDefault:
    def __init__(self, type=PatternType.SOLID, distance=5.0, size=0.5, rotation=0.0, rotatio=0.0, xshift=0.0, yshift=0.0):
        self.TYPE = type
        self.DISTANCE = distance
        self.SIZE = size
        self.ROTATION = rotation
        self.XSHIFT = xshift
        self.YSHIFT = yshift


class LineJunctionType:
    MITER = 'miter'
    ROUND = 'round'
    BEVEL = 'bevel'


# Node/marker shapes supported by TkzGeom
class Marker_Shape:
    CIRCLE = 'circle'
    RECTANGE = 'rectangle'
    REGULAR_POLYGON = 'regular polygon'
    STAR = 'star'
    DIAMOND = 'diamond'


# Parameters that define a node/marker.
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


# Anchor of a label.
class Direction:
    CENTRE = 'centered'
    NORTH = 'above'
    NORTH_EAST = 'above right'
    EAST = 'right'
    SOUTH_EAST = 'below right'
    SOUTH = 'below'
    SOUTH_WEST = 'below left'
    WEST = 'left'
    NORTH_WEST = 'above left'


# Path decoration modes supported by TkzGeom.
class DecorationType:
    NONE = 'none'
    TEXT_ALONG_CURVE = 'text along path'
    ZIGZAG = 'zigzag'
    SAW = 'saw'
    RANDOM_STEPS = 'random steps'
    BUMPS = 'bumps'
    COIL= 'coil'
    SNAKE = 'snake'


# Parameters that make up a decoration.
class DecorationDefault:
    def __init__(self, type=DecorationType.NONE, amplitude=3.0, wavelength=3.0, text=''):
        self.TYPE = type
        self.AMPLITUDE = amplitude
        self.WAVELENGTH = wavelength
        self.TEXT = text


# Parameters that define a label.
class LabelDefault:
    def __init__(self, show=True, text='', anchor=Direction.SOUTH_EAST, offset=0.0):
        self.SHOW = show
        self.TEXT = text
        self.ANCHOR = anchor
        self.OFFSET = offset


# Line strokes supported by tikz.
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


# The segment is connected either to the boundary or the centre of a node.
class LineConnectTo:
    NODE_BOUNDARY = 'boundary'
    NODE_CENTRE = 'centre'

class Mode(): # TODO good idea but not sure if actually used.
    POINT = 0
    SEGMENT = 1
    CIRCLE = 2
    MOVE = 3
    DECORATOR = 4


class Canvas: # TODO not entirely used now.
    POINT_RADIUS = 7
    LINE_THICKNESS = 3
    CIRCLE_THICKNESS = 3
    MAX_DISTANCE_TO_HIGHLIGHT = 8


# Contains the default values for a point plus the definition subtypes.
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

    class Definition:
        FREE = 'free'
        INTERSECTION = 'intersection'
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
        Definition.FREE: "Free point.",
        Definition.INTERSECTION: "Intersection of #1 and #2.",
        Definition.CIRCLE_CENTRE: "The middle point of the #1.",
        Definition.SEGMENT_MIDPOINT: "The midpoint of segment #1.",
        Definition.ON_LINE: "The point defined as dilation of #1, by factor #2 across centre #3.",
        Definition.ON_CIRCLE: "The point on the #1 at angle #2.",
        Definition.PROJECTION: "The orthogonal projection of #1 on #2.",
        Definition.BISECTOR: "A point on the bisector of angle #1.",
        Definition.TRANSLATION: "The point given by translating point #1 with vector #2.",
        Definition.PERPENDICULAR: "A point on the perpendicular to segment #1 at #2.",
        Definition.ROTATION: "The point defined as the rotation of #1, by angle #2 around centre #3."
    }

# Contains the default values for a point plus the definition subtypes.
class Circle:
    class Default: # TODO change this
        SIZE = 3.0
        LINE_WIDTH = 0.4
        NODE_INSIDE_TEXT = ''
        Fill_Colour = ColourDefault()
        Line_Colour = ColourDefault()
        Marker = MarkerDefault()
        Label = LabelDefault()
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]

    class Definition:
        WITH_CENTRE = 'with_centre'
        CIRCUM = 'circum'
        INSCRIBED = 'inscribed'
        ARC = 'arc'
        SECTOR = 'sector'

    # TEXT_DICT = {
    #     Definition.WITH_CENTRE: "Free point.",
    #     Definition.CIRCUM: "Intersection of #1 and #2.",
    #     Definition.INSCRIBED: "The middle point of the #1.",
    #     Definition.ARC: "The midpoint of segment #1.",
    #     Definition.SECTOR: "The point defined as dilation of #1, by factor #2 across centre #3.",
    # }


# Contains the default values for a segment.
class Segment:
    class Default:
        LINE_WIDTH = 3.0
        Fill_Colour = ColourDefault()
        Line_Colour = ColourDefault()
        Marker = MarkerDefault()
        Label = LabelDefault()
        Double_Line = DoubleDefault()
        O_Arrow = ArrowDefault()
        D_Arrow = ArrowDefault()
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]
        LINE_CONNECT_TO = LineConnectTo.NODE_BOUNDARY


# Contains the default values for a polygon.
class Polygon:
    class Default:
        LINE_WIDTH = 0.4
        Fill_Colour = ColourDefault(strength=10)
        Line_Colour = ColourDefault()
        # Double_Line = DoubleDefault()
        Fill_Pattern = FillPatternDefault()
        Decoration = DecorationDefault()
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]


# Contains the default values for a linestring.
class Linestring: # TODO don't forget arrow bending, it is important
    class Default:
        LINE_WIDTH = 0.4
        Line_Colour = ColourDefault()
        Double_Line = DoubleDefault()
        Decoration = DecorationDefault()
        O_Arrow = ArrowDefault()
        D_Arrow = ArrowDefault()
        Line_Junction = LineJunctionType.MITER
        LINE_DASH_STROKE = Line_Stroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]
        LINE_CONNECT_TO = LineConnectTo.NODE_BOUNDARY


# List of the default packages.
PackagesDefault = [
    "\\usepackage{amsmath,amssymb}",
    "\\usepackage[utf8]{inputenc}",
    "\\usepackage[T1]{fontenc}",
    "\\usepackage{xcolor}",
    "\\usepackage{tkz-euclide,tkz-fct}",
    "\\usetikzlibrary{arrows.meta, bending, patterns.meta, hobby, ducks}",
    "\\usetikzlibrary{shapes, backgrounds, decorations.pathmorphing, calc}"
]


BackGroundColourDefault = { # TODO investigate and delete.
    "name": "black",
    "mix_with": "black",
    "mix_percent": 0,
    "strength": 0
}


# The default dimensions of the window
WindowDefault = {
    "left": -5.0,
    "top": 5.0,
    "scale": 1.0,
}


# The creator tools.
class Tool:
    FREE = 0
    MIDPOINT_SEGMENT = 1
    INTERSECT_POINT = 2
    CIRCLE_CENTRE = 3
    TRANSLATION = 4
    POINT_ON_LINE = 5
    POINT_ON_CIRCLE = 6
    ORTHOGONAL_PROJECTION = 7
    PERPENDICULAR = 8
    BISECTOR = 9
    ROTATION = 10
    MAKEGRID = 11

    SEGMENT_THROUGH = 100
    POLYGON = 101
    LINESTRING = 102

    CIRCLE_WITH_CENTRE = 200
    CIRCUM_CIRCLE = 201
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

    TYPE_MAP = {
        FREE: ('point', Point.Definition.FREE),
        MIDPOINT_SEGMENT: ('point', Point.Definition.SEGMENT_MIDPOINT),
        INTERSECT_POINT: ('point', Point.Definition.INTERSECTION),
        CIRCLE_CENTRE: ('point', Point.Definition.CIRCLE_CENTRE),
        TRANSLATION: ('point', Point.Definition.TRANSLATION),
        POINT_ON_LINE: ('point', Point.Definition.ON_LINE),
        POINT_ON_CIRCLE: ('point', Point.Definition.ON_CIRCLE),
        ORTHOGONAL_PROJECTION: ('point', Point.Definition.PROJECTION),
        PERPENDICULAR: ('point', Point.Definition.PERPENDICULAR),
        BISECTOR: ('point', Point.Definition.BISECTOR),
        ROTATION: ('point', Point.Definition.ROTATION),
        MAKEGRID: ('point', Point.Definition.ON_LINE),

        SEGMENT_THROUGH: ('segment', None),
        POLYGON: ('polygon', None),
        LINESTRING: ('linestring', None),

        CIRCLE_WITH_CENTRE: ('circle', 'with_centre'),
        CIRCUM_CIRCLE: ('circle', 'circum')

    }


# The patterns that has extra tuning possibilities.
PATTERN_EXTRAS = set([PatternType.LINES, PatternType.HATCH, PatternType.DOTS_EXTRA, PatternType.FIVEPOINTED_STARS, PatternType.SIXPOINTED_STARS])


# List of types in items as it appears in the tabWidget.
TYPES = ['point', 'segment', 'circle', 'polygon', 'linestring', 'function', 'colour', 'number']
