from Point import Point
from Segment import Segment
from Polygon import Polygon
from collections import OrderedDict
from operator import itemgetter

def item_in_focus(project_data, mouse):
    distances = {}
    for item in project_data.items.values():
        if isinstance(item, Point):
            distance = item.distance_sqr(*mouse.get_xy(), project_data.items)
            if distance < 200:
                distances[item.get_id()] = distance
    if distances:
        distance_dict_ord = OrderedDict(sorted(distances.items(), key=itemgetter(1)))
        return next(iter(distance_dict_ord.keys()))

    distances = {}
    for item in project_data.items.values():
        if isinstance(item, Segment):
            distance = item.distance_sqr(*mouse.get_xy(), project_data.items)
            if distance < 200:
                distances[item.get_id()] = distance
    if distances:
        distance_dict_ord = OrderedDict(sorted(distances.items(), key=itemgetter(1)))
        return next(iter(distance_dict_ord.keys()))

    for item in project_data.items.values():
        if isinstance(item, Polygon):
            if item.is_inside(*mouse.get_xy(), project_data.items):
                return item.get_id()
    return None
