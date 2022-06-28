"""Collection of constants"""


def attribute_values(class_input):
    """Turn class attribute values into a list."""
    return [m for v, m in vars(class_input).items() if not (v.startswith('_') or callable(m))]


class MouseState:  # TODO check if this is actually used anywhere, if so delete
    UP = 0
    DOWN = 1


class MouseButton:  # TODO check if this is actually used anywhere, if so delete
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


class StrategyType:
    SEGMENTS = 'segments'
    VERTHOZ = 'vert-hoz'
    HOZVERT = 'hoz-vert'
    IO_ANGLE = 'io_angle'
    BENDED_LEFT = 'bended_left'
    BENDED_RIGHT = 'bended_right'
    SMOOTH = 'smooth'


class StrategyDefault:
    def __init__(self, type_=StrategyType.SEGMENTS, rounded_corners=0.0, bend_angle=30, in_angle=90, out_angle=0,
                 smooth_tension=0.55, loop_size=1.0):
        self.TYPE = type_
        self.ROUNDED_CORNERS = rounded_corners
        self.BEND_ANGLE = bend_angle
        self.IN_ANGLE = in_angle
        self.OUT_ANGLE = out_angle
        self.SMOOTH_TENSION = smooth_tension
        self.LOOP_SIZE = loop_size


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
    def __init__(self, tip=ArrowTip.NONE, side=ArrowSide.BOTH, width=1.0, length=1.0, reversed_=False, bending=False):
        self.TIP = tip
        self.WIDTH = width
        self.LENGTH = length
        self.BENDING = bending
        self.SIDE = side
        self.REVERSED = reversed_


# Parameters that define a pattern.
class FillPatternDefault:
    def __init__(self, type_=PatternType.SOLID, distance=5.0, size=0.5, rotation=0.0, xshift=0.0,
                 yshift=0.0):
        self.TYPE = type_
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
class MarkerShape:
    CIRCLE = 'circle'
    RECTANGE = 'rectangle'
    REGULAR_POLYGON = 'regular polygon'
    STAR = 'star'
    DIAMOND = 'diamond'


# Parameters that define a node/marker.
class MarkerDefault:
    def __init__(self, size=3, shape=MarkerShape.CIRCLE, shape_number=5, ratio=2.25, inner_sep=0.0,
                 rounded_corners=0.0, text='', text_width=0.0):
        self.SIZE = size
        self.SHAPE = shape
        self.SHAPE_NUMBER = shape_number
        self.RATIO = ratio
        self.INNER_SEP = inner_sep
        self.ROUNDED_CORNERS = rounded_corners
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
    COIL = 'coil'
    SNAKE = 'snake'


# Parameters that make up a decoration.
class DecorationDefault:
    def __init__(self, type_=DecorationType.NONE, amplitude=3.0, wavelength=3.0, text=''):
        self.TYPE = type_
        self.AMPLITUDE = amplitude
        self.WAVELENGTH = wavelength
        self.TEXT = text


class SegmentMarkerType:
    NONE = 'none'
    VERT = '|'
    VVERT = '||'
    VVVERT = '|||'
    SVERT = 's|'
    SVVERT = 's||'
    ZED = 'z'
    MULTIPLICATION = '*'
    EX = 'x'
    PLUS = '+'
    MINUS = '-'
    OH = 'o'
    OHOH = 'oo'
    ASTERISK = 'asterisk'
    STAR = 'star'
    TEN_POINTED_STAR = '10-pointed star'
    OPLUS = 'oplus'
    OPLUS_STAR = 'oplus*'
    OTIMES = 'otimes'
    OTIMES_STAR = 'otimes*'
    SQUARE = 'square'
    SQUARE_STAR = 'square*'
    TRIANGLE = 'triangle'
    TRIANGLE_STAR = 'triangle*'
    DIAMOND = 'diamond'
    DIAMOND_STAR = 'diamond*'
    HALF_DIAMOND_STAR = 'halfdiamond*'
    HALF_SQUARE_STAR = 'halfsquare*'
    HALF_SQUARE_RIGHT_STAR = 'halfsquare right*'
    HALF_SQUARE_left_STAR = 'halfsquare left*'
    PENTAGON = 'pentagon'
    PENTAGON_STAR = 'pentagon*'
    MERCEDES_STAR = 'Mercedes star'
    MERCEDES_STAR_FLIPPED = 'Mercedes star flipped'
    HALF_CIRCLE = 'halfcircle'
    HALF_CIRCLE_STAR = 'halfcircle*'
    HEART = 'heart'


class SegmentMarkerDefault:
    def __init__(self, symbol=SegmentMarkerType.NONE, width=0.4, size=4.0, position=0.5):
        self.SYMBOL = symbol
        self.WIDTH = width
        self.SIZE = size
        self.POSITION = position


# Parameters that define a label.
class LabelDefault:
    def __init__(self, show=True, text='', anchor=Direction.SOUTH_EAST, offset=0.0):
        self.SHOW = show
        self.TEXT = text
        self.ANCHOR = anchor
        self.OFFSET = offset


# Line strokes supported by tikz.
class LineStroke:
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


class Mode:  # TODO good idea but not sure if actually used.
    POINT = 0
    SEGMENT = 1
    CIRCLE = 2
    MOVE = 3
    DECORATOR = 4


class Canvas:  # TODO not entirely used now.
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
        LINE_DASH_STROKE = LineStroke.SOLID
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
    class Default:  # TODO change this
        LINE_WIDTH = 0.4
        Fill_Colour = ColourDefault(strength=10)
        Fill_Pattern = FillPatternDefault()
        Line_Colour = ColourDefault()
        O_Arrow = ArrowDefault()
        D_Arrow = ArrowDefault()
        Double_Line = DoubleDefault()
        LINE_DASH_STROKE = LineStroke.SOLID
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
        LINE_WIDTH = 0.4
        Fill_Colour = ColourDefault()
        Line_Colour = ColourDefault()
        Marker = MarkerDefault()
        Double_Line = DoubleDefault()
        O_Arrow = ArrowDefault()
        D_Arrow = ArrowDefault()
        LINE_DASH_STROKE = LineStroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]
        LINE_CONNECT_TO = LineConnectTo.NODE_BOUNDARY
        Segment_Marker = SegmentMarkerDefault()


# Contains the default values for a polygon.
class Polygon:
    class Default:
        LINE_WIDTH = 0.4
        Fill_Colour = ColourDefault(strength=10)
        Line_Colour = ColourDefault()
        # Double_Line = DoubleDefault()
        Fill_Pattern = FillPatternDefault()
        Decoration = DecorationDefault()
        Strategy = StrategyDefault()
        LINE_DASH_STROKE = LineStroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]


# Contains the default values for a linestring.
class Linestring:  # TODO don't forget arrow bending, it is important
    class Default:
        LINE_WIDTH = 0.4
        Line_Colour = ColourDefault()
        Double_Line = DoubleDefault()
        Decoration = DecorationDefault()
        Strategy = StrategyDefault()
        O_Arrow = ArrowDefault()
        D_Arrow = ArrowDefault()
        O_ARROW_BENDING = False
        D_ARROW_BENDING = False
        Line_Junction = LineJunctionType.MITER
        LINE_DASH_STROKE = LineStroke.SOLID
        LINE_DASH_CUSTOM = [5, 2]
        LINE_CONNECT_TO = LineConnectTo.NODE_CENTRE


# List of the default packages.
PackagesDefault = [
    "\\usepackage{amsmath,amssymb}",
    "\\usepackage[utf8]{inputenc}",
    "\\usepackage[T1]{fontenc}",
    "\\usepackage[rgb]{xcolor} % xcolor must be loaded before everything tikz",
    "\\usepackage{tikz, tkz-euclide, etoolbox}",
    "\\usetikzlibrary{arrows.meta, bending, patterns.meta, ducks}",
    "\\usetikzlibrary{shapes, backgrounds, decorations.pathmorphing, calc}"
]

BackGroundColourDefault = {  # TODO investigate and delete.
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
    # 0 - 99
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

    # 100-199
    SEGMENT_THROUGH = 100
    POLYGON = 101
    LINESTRING = 102

    # 200-299
    CIRCLE_WITH_CENTRE = 200
    CIRCUM_CIRCLE = 201
    INSCRIBED_CIRCLE = 202
    ARC = 203
    SECTOR = 204

    # 300-399
    # MOVE_POINT = 300
    # MOVE_AND_SCALE_CANVAS = 301

    # 400-499
    MARK_ANGLE = 400
    MARK_RIGHT_ANGLE = 401
    # COMPASS = 402

    # 500-599
    YFX_FUNCTION = 500
    POLAR_FUNCTION = 501
    PARAMETRIC_FUNCTION = 502

    # 600-699
    MAKEGRID = 600
    REGULAR_POLYGON = 601
    COMPLETE_GRAPH = 602
    STAR_GRAPH = 603
    FROM_FILE = 604
    TURTLE = 605


TOOL_TO_PARSE_MAP = {
    Tool.FREE: 'FreePoint',
    Tool.MIDPOINT_SEGMENT: 'MidPoint',
    Tool.INTERSECT_POINT: 'Intersection',
    Tool.CIRCLE_CENTRE: 'Centre',
    Tool.TRANSLATION: 'Translation',
    Tool.POINT_ON_LINE: 'OnLine',
    Tool.POINT_ON_CIRCLE: 'OnCircle',
    Tool.ORTHOGONAL_PROJECTION: 'Projection',
    Tool.PERPENDICULAR: 'Perpendicular',
    Tool.BISECTOR: 'Bisector',
    Tool.ROTATION: 'Rotation',

    Tool.SEGMENT_THROUGH: 'Segment',
    Tool.POLYGON: 'Polygon',
    Tool.LINESTRING: 'Linestring',

    Tool.CIRCLE_WITH_CENTRE: 'WithCentre',
    Tool.CIRCUM_CIRCLE: 'Circum',
    Tool.INSCRIBED_CIRCLE: 'InCircle',
    Tool.ARC: 'Arc',

    Tool.MAKEGRID: 'MakeGrid',
    Tool.REGULAR_POLYGON: 'RegularPolygon'
}

PARSE_TO_TYPE_MAP = {
    TOOL_TO_PARSE_MAP[Tool.FREE]: ('point', Point.Definition.FREE),
    TOOL_TO_PARSE_MAP[Tool.MIDPOINT_SEGMENT]: ('point', Point.Definition.SEGMENT_MIDPOINT),
    TOOL_TO_PARSE_MAP[Tool.INTERSECT_POINT]: ('point', Point.Definition.INTERSECTION),
    TOOL_TO_PARSE_MAP[Tool.CIRCLE_CENTRE]: ('point', Point.Definition.CIRCLE_CENTRE),
    TOOL_TO_PARSE_MAP[Tool.TRANSLATION]: ('point', Point.Definition.TRANSLATION),
    TOOL_TO_PARSE_MAP[Tool.POINT_ON_LINE]: ('point', Point.Definition.ON_LINE),
    TOOL_TO_PARSE_MAP[Tool.POINT_ON_CIRCLE]: ('point', Point.Definition.ON_CIRCLE),
    TOOL_TO_PARSE_MAP[Tool.ORTHOGONAL_PROJECTION]: ('point', Point.Definition.PROJECTION),
    TOOL_TO_PARSE_MAP[Tool.PERPENDICULAR]: ('point', Point.Definition.PERPENDICULAR),
    TOOL_TO_PARSE_MAP[Tool.BISECTOR]: ('point', Point.Definition.BISECTOR),
    TOOL_TO_PARSE_MAP[Tool.ROTATION]: ('point', Point.Definition.ROTATION),

    TOOL_TO_PARSE_MAP[Tool.SEGMENT_THROUGH]: ('segment', None),
    TOOL_TO_PARSE_MAP[Tool.POLYGON]: ('polygon', None),
    TOOL_TO_PARSE_MAP[Tool.LINESTRING]: ('linestring', None),

    TOOL_TO_PARSE_MAP[Tool.CIRCLE_WITH_CENTRE]: ('circle', 'with_centre'),
    TOOL_TO_PARSE_MAP[Tool.CIRCUM_CIRCLE]: ('circle', 'circum'),
    TOOL_TO_PARSE_MAP[Tool.INSCRIBED_CIRCLE]: ('circle', 'inscribed'),
    TOOL_TO_PARSE_MAP[Tool.ARC]: ('circle', 'arc'),

    TOOL_TO_PARSE_MAP[Tool.MAKEGRID]: ('cloud', None),
    TOOL_TO_PARSE_MAP[Tool.REGULAR_POLYGON]: ('cloud', None)
}

# The patterns that has extra tuning possibilities.
PATTERN_EXTRAS = {PatternType.LINES, PatternType.HATCH, PatternType.DOTS_EXTRA, PatternType.FIVEPOINTED_STARS,
                  PatternType.SIXPOINTED_STARS}

CIRCLE_PATTERN_LENGTH = {Tool.CIRCLE_WITH_CENTRE: 2,
                         Tool.CIRCUM_CIRCLE: 3,
                         Tool.INSCRIBED_CIRCLE: 3,
                         Tool.ARC: 3}

# List of types in items as it appears in the tabWidget.
TYPES = ['point', 'segment', 'circle', 'polygon', 'linestring', 'function', 'colour', 'code']

Default_Settings_Dict = {
    'PDF_LATEX_COMMAND': r'pdflatex -synctex=1 -interaction=batchmode --shell-escape -halt-on-error tmp.tex',
    'PDF2PNG': 'pdftocairo -png -scale-to-x #1 -scale-to-y #2 tmp.pdf',
    'SYNTAX': '$default',
    'ASPECT_RATIO': [16, 9],
}
