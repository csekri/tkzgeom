"""
Contains all a large stack of constants required in different files.
"""

#TOOLS
NEW_POINT, POINT_ON_LINE, POINT_ON_CIRCLE, INTERSECT_POINT, MIDPOINT_SEGMENT = (0,1,2,3,4)
MIDPOINT_CIRCLE, ORTHOGONAL_PROJECTION, BISECTOR, TRANSLATION, ORTHOGONAL, ROTATION, MAKEGRID = (5,6,7,8,9,10,11)
SEGMENT_THROUGH, POLYGON, LINESTRING = (100, 101, 102)
CIRCUM_CIRCLE, TWO_POINT_CIRCLE, ARC, SECTOR, INSCRIBED_CIRCLE = (200,201,202,203,204)
MOVE_POINT, MOVE_AND_SCALE_CANVAS = (300,301)
MARK_ANGLE, MARK_RIGHT_ANGLE, COMPASS = (400, 401, 402)
YFX_FUNCTION, POLAR_FUNCTION, PARAMETRIC_FUNCTION = (500, 501, 502)

#MODES
POINT, SEGMENT, CIRCLE, MOVE, DECORATOR = (0,1,2,3,4)

# DEFAULT CANVAS VALUES
CANVAS_LINE_THICKNESS = 3
CANVAS_POINT_RADIUS = 7
MAX_DISTANCE_TO_HIGHLIGHT = 8

# DEFAULT TIKZ VALUES
DEFAULT_POINT_SIZE = 3.0
DEFAULT_POINT_LINE_WIDTH = 0.4
DEFAULT_POINT_LABEL_ANGLE = 315
DEFAULT_POINT_LABEL_DISTANCE = 0.0
DEFAULT_POINT_LABEL_ANCHOR = "below right"
DEFAULT_POINT_FILL_COLOUR_NAME = "black"
DEFAULT_POINT_FILL_STRENGTH = 100
DEFAULT_POINT_FILL_OPACITY = 1.0
DEFAULT_POINT_LINE_COLOUR_NAME = "black"
DEFAULT_POINT_LINE_STRENGTH = 100
DEFAULT_POINT_LINE_OPACITY = 1.0
DEFAULT_POINT_LINE_STROKE = "solid"
DEFAULT_POINT_LINE_STROKE_CUSTOM = [5, 2]

DEFAULT_SEGMENT_LINE_WIDTH = 0.4
DEFAULT_SEGMENT_LINE_STROKE = 'solid'
DEFAULT_SEGMENT_LINE_STROKE_CUSTOM = [5, 2]
DEFAULT_SEGMENT_LABEL_ANCHOR = 'below right'
DEFAULT_SEGMENT_LABEL_ANGLE = 315
DEFAULT_SEGMENT_LABEL_DISTANCE = 0.0
DEFAULT_SEGMENT_LABEL_POSITION = 0.5
DEFAULT_SEGMENT_LINE_COLOUR_NAME = 'black'
DEFAULT_SEGMENT_LINE_STRENGTH = 100
DEFAULT_SEGMENT_LINE_OPACITY = 1.0
DEFAULT_SEGMENT_O_ARROW_TIP = 'None'
DEFAULT_SEGMENT_O_ARROW_LENGTH = 1.0
DEFAULT_SEGMENT_O_ARROW_WIDTH = 1.0
DEFAULT_SEGMENT_O_ARROW_SIDE = 'both'
DEFAULT_SEGMENT_D_ARROW_TIP = 'None'
DEFAULT_SEGMENT_D_ARROW_LENGTH = 1.0
DEFAULT_SEGMENT_D_ARROW_WIDTH = 1.0
DEFAULT_SEGMENT_D_ARROW_SIDE = 'both'
DEFAULT_SEGMENT_MARK_WIDTH = 0.4
DEFAULT_SEGMENT_MARK_SIZE = 4.0
DEFAULT_SEGMENT_MARK_POSITION = 0.5
DEFAULT_SEGMENT_MARK_SYMBOL = 'none'
DEFAULT_SEGMENT_MARK_COLOUR = 'same'
DEFAULT_SEGMENT_O_EXTENSION = 0.0
DEFAULT_SEGMENT_D_EXTENSION = 0.0

DEFAULT_RIGHT_ANGLE_TYPE = 'Anglo-French'

DEFAULT_ANGLE_ARC = 1
DEFAULT_ANGLE_SIZE = 0.5
DEFAULT_ANGLE_MARK_SIZE = 4
DEFAULT_ANGLE_MARK_COLOUR = 'same'
DEFAULT_ANGLE_MARK_POSITION = 0.5
DEFAULT_ANGLE_MARK_SYMBOL = 'none'
DEFAULT_ANGLE_LINE_COLOUR_NAME = 'black'
DEFAULT_ANGLE_LINE_STRENGTH = 100
DEFAULT_ANGLE_LINE_OPACITY = 1.0
DEFAULT_ANGLE_FILL_COLOUR_NAME = 'same'
DEFAULT_ANGLE_FILL_STRENGTH = 100
DEFAULT_ANGLE_FILL_OPACITY = 1.0
DEFAULT_ANGLE_LABEL_DISTANCE = 1.0
DEFAULT_ANGLE_LABEL_ANCHOR = 'centered'
DEFAULT_ANGLE_LINE_WIDTH = 0.4
DEFAULT_ANGLE_LINE_STROKE = 'solid'
DEFAULT_ANGLE_LINE_STROKE_CUSTOM = [5, 2]

DEFAULT_CURVE_STRATEGY = 'nothing'
DEFAULT_CURVE_IN_ANGLE = 0
DEFAULT_CURVE_OUT_ANGLE = 180
DEFAULT_CURVE_BEND_ANGLE = 0
DEFAULT_CURVE_CORNER_RADIUS = 0.0
DEFAULT_PATTERN_TYPE = 'none'
DEFAULT_PATTERN_DISTANCE = 3.0
DEFAULT_PATTERN_ROTATION = 0
DEFAULT_PATTERN_XSHIFT = 0.0
DEFAULT_PATTERN_YSHIFT = 0.0
DEFAULT_DECORATOR_TYPE = 'none'
DEFAULT_DECORATOR_AMPLITUDE = 2.5
DEFAULT_DECORATOR_WAVE_LENGTH = 10.0
DEFAULT_LOOP_SIZE = 40
DEFAULT_PATTERN_DISTANCE = 3
DEFAULT_PATTERN_SIZE = 0

DEFAULT_CIRCLE_LABEL_DISTANCE = 1.0
DEFAULT_CIRCLE_LABEL_ANCHOR = 'centered'

DEFAULT_FUNCTION_SAMPLES = 50
DEFAULT_FUNCTION_TYPE = 'none'
DEFAULT_FUNCTION_NUMBER = 10
DEFAULT_FUNCTION_FILL_OPACITY = 0.5

DEFAULT_ANCHOR_DISTANCE = 0.1
DEFAULT_AXIS_ARROW_TIP = 'Latex'

POINT_TEXT_DICT = {
"free" : "Free point.",
"intersection_ll" : "Intersection point of line #1 and line #2.",
"intersection_lc" : "Intersection point of line #1 and the #2.",
"circle_midpoint" : "The middle point of the #1.",
"segment_midpoint" : "The midpoint of segment #1.",
"point_on_line" : "The point defined as dilation of #1, by factor #2 across centre #3.",
"point_on_circle" : "The point on the #1 at angle #2.",
"projection_point" : "The orthogonal projection of #1 on #2.",
"bisector_point" : "A point on the bisector of angle #1.",
"translation_point" : "The point given by translating point #1 with vector #2.",
"orthogonal_point" : "A point on the perpendicular to segment #1 at #2.",
"rotation" : "The point defined as the rotation of #1, by angle #2 around centre #3."
}



# SELECTION VALUES

COLOURS = ['black', 'blue', 'brown', 'cyan', 'darkgray', 'gray', 'green',\
           'lightgray', 'lime', 'magenta', 'olive', 'orange', 'pink',\
           'purple', 'red', 'teal', 'violet', 'white', 'yellow']
MARKER_COLOURS = ['same'] + COLOURS
DIRECTIONS = ['center','north','north west','west','south west',\
              'south','south east','east','north east']

DIRECTIONS = ['centered','above','above left','left','below left',\
              'below','below right','right','above right']

LINE_STROKES = ['solid', 'loosely dashed', 'dashed', 'densely dashed',\
                'loosely dotted', 'dotted', 'densely dotted', 'loosely dash dot',\
                'dash dot', 'densely dash dot', 'loosely dash dot dot',\
                'dash dot dot', 'densely dash dot dot', 'custom']

SEGMENT_MARKERS = ['none', '|', '||', '|||', 's|', 's||', 'z', '*', 'x',\
                  '+', '-', 'o', 'oo', 'asterisk', 'star', '10-pointed star',\
                  'oplus', 'oplus*', 'otimes', 'otimes*', 'square',\
                  'square*', 'triangle', 'triangle*', 'diamond', 'diamond*',\
                  'halfdiamond*', 'halfsquare*',\
                  'halfsquare right*', 'halfsquare left*', 'pentagon',\
                  'pentagon*', 'Mercedes star', 'Mercedes star flipped',\
                  'halfcircle', 'halfcircle*', 'heart']

ARROW_TIPS = ['None', 'Stealth', 'Stealth^r', 'Stealth^o', 'Stealth^or', '<', '>',\
              'Latex', 'Latex^r', 'Latex^o', 'Latex^or', 'To', 'Computer Modern Rightarrow',\
              'Implies', 'Butt Cap', 'Fast Round', 'Fast Triangle', 'Round Cap',\
              'Triangle Cap', 'Circle', 'Circle^o', 'Diamond', 'Diamond^o',\
              'Ellipse', 'Ellipse^o', 'Kite', 'Kite^o', 'Rectangle',\
              'Rectangle^o', 'Square', 'Square^o', 'Triangle', 'Triangle^o',\
              'Turned Square', 'Turned Square^o', 'Arc Barb', 'Bar', 'Bracket',\
              'Hooks', 'Parenthesis', 'Straight Barb', 'Tee Barb']

ARROW_SIDES = ['both', 'left', 'right']
ANGLE_ARC = [1,2,3]
PATTERN_TYPES = ['none', 'solid', 'horizontal lines', 'vertical lines',\
                 'north east lines', 'north west lines', 'grid', 'crosshatch',\
                 'dots', 'crosshatch dots', 'bricks', 'checkerboard', 'Lines',\
                 'Hatch', 'Dots', 'Fivepointed stars', 'Sixpointed stars']
DECORATIONS = ['none', 'text along path', 'zigzag', 'saw', 'random steps',\
              'bumps', 'coil', 'snake']
STRATEGIES = ['nothing', 'segment_in_out', 'segment_bend_left', 'segment_bend_right', 'smooth']

FUNCTION_TYPES = ['none', 'sup', 'inf', 'mid']

FONT_SIZES = ['', '\\tiny', '\\scriptsize', '\\footnotesize', '\\small',\
              '\\large', '\\Large', '\\LARGE', '\\huge', '\\Huge']

TRUE_FALSE = [True, False]

FRACTIONS = list(range(11))

DUCK_EXTRA = {'strawhat':'ribbon', 'graduate':'tassel',\
              'harlequin':'niuqelrah', 'bunny':'inear',\
              'magichat':'magicstars', 'signpost':'signcolour',\
              'neckerchief':'woggle'}
DUCK_TYPES = ['custom', 'special', 'chess', 'random']
DUCK_SPECIAL = ['horse', 'unicorn', 'bunny', 'sheep', 'girlwithpearlearring',\
                'queenuk', 'snowman', 'overleaf', 'ceasar', 'ghost', 'yoda', 'vader', 'leila']
DUCK_CHESS = ['wbauer', 'wturm', 'wspringer','wlaeufer', 'wdame', 'wkoenig',\
              'bbauer',  'bturm', 'bspringer', 'blaeufer', 'bdame', 'bkoenig']
DUCK_BILLS = ['sweet', 'grumpy', 'laughing', 'parrot', 'vampire']
DUCK_HAIRS = ['none', 'longhair', 'shorthair', 'parting',\
              'crazyhair', 'recedinghair', 'mohican', 'mullet']
DUCK_GLASSESS = ['none', 'glasses', 'squareglasses', 'sunglasses', 'mask',]
DUCK_HATS = ['none', 'alien', 'hat', 'tophat', 'strawhat', 'cap',\
             'conicalhat', 'santa', 'graduate', 'beret', 'peakedcap',\
             'harlequin', 'sailor', 'crown', 'queencrown',\
             'kingcrown', 'helmet', 'viking', 'devil', 'unicorn',\
             'bunny', 'witch', 'magichat', 'darthvader', 'chef']
DUCK_NECKLACES = ['none', 'necklace', 'stethoscope', 'neckerchief']
DUCK_ACCESSORIES = ['none', 'magicwand', 'signpost', 'book', 'cricket',\
                    'hockey', 'football', 'lightsaber', 'torch', 'prison',\
                    'crozier', 'icecream', 'rollingpin', 'cake', 'pizza',\
                    'baguette', 'cheese', 'milkshake', 'wine', 'cocktail',\
                    'wing', 'basket', 'easter', 'crystalball', 'umbrella',\
                    'umbrellaclosed', 'handbag']
DUCK_SPEECH = ['none', 'speech', 'think']

DUCK_EXTRA = {'strawhat':'ribbon', 'graduate':'tassel',\
              'harlequin':'niuqelrah', 'bunny':'inear',\
              'magichat':'magicstars', 'signpost':'signcolour',\
              'neckerchief':'woggle'}

PRINCIPAL_COLOURS = ['default', 'black', 'blue', 'brown', 'cyan', 'darkgray', 'gray', 'green',\
           'lightgray', 'lime', 'magenta', 'olive', 'orange', 'pink',\
           'purple', 'red', 'teal', 'violet', 'white', 'yellow']

MIX_COLOURS = ['none', 'black', 'blue', 'brown', 'cyan', 'darkgray', 'gray', 'green',\
           'lightgray', 'lime', 'magenta', 'olive', 'orange', 'pink',\
           'purple', 'red', 'teal', 'violet', 'white', 'yellow']
