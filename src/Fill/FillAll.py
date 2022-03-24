from Fill.FillPoint import fill_point_fields
from Fill.FillSegment import fill_segment_fields
from Fill.FillPolygon import fill_polygon_fields
from Fill.FillColour import fill_colour_fields
from Fill.FillCircle import fill_circle_fields
from Fill.FillLinestring import fill_linestring_fields
from Fill.FillCode import fill_code_fields


def fill_all_fields(scene):
    """Fill all widgets in the tabWidget."""
    fill_point_fields(scene)
    fill_segment_fields(scene)
    fill_circle_fields(scene)
    fill_polygon_fields(scene)
    fill_linestring_fields(scene)
    fill_colour_fields(scene)
    fill_code_fields(scene)
