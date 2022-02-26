from Fill.FillPoint import fill_point_fields
from Fill.FillSegment import fill_segment_fields
from Fill.FillColour import fill_colour_fields

def fill_all_fields(scene):
    fill_point_fields(scene)
    fill_segment_fields(scene)
    fill_colour_fields(scene)
