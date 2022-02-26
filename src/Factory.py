from PointClasses.FreePoint import FreePoint
from PointClasses.Midpoint import Midpoint
from PointClasses.OnLine import OnLine
from PointClasses.Intersection import Intersection
from Point import Point
from Segment import Segment
from Polygon import Polygon
from Colour import Colour
import Constant as c

class Factory:
    @staticmethod
    def create_item(item):
        if item['type'] == 'segment':
            return Segment(item)
        if item['type'] == 'point':
            if item["sub_type"] == c.Point.Definition.FREE:
                return FreePoint(item)
            if item["sub_type"] == c.Point.Definition.SEGMENT_MIDPOINT:
                return Midpoint(item)
            if item["sub_type"] == c.Point.Definition.ON_LINE:
                return OnLine(item)
            if item["sub_type"] == c.Point.Definition.INTERSECTION:
                return Intersection(item)
        if item['type'] == 'polygon':
            return Polygon(item)
        if item['type'] == 'colour':
            return Colour(item)

    @staticmethod
    def create_empty_item(type, sub_type):
        if type == 'segment':
            return Segment(None)
        if type == 'point':
            if sub_type == c.Point.Definition.FREE:
                return FreePoint(None)
            if sub_type == c.Point.Definition.SEGMENT_MIDPOINT:
                return Midpoint(None)
            if sub_type == c.Point.Definition.ON_LINE:
                return OnLine(None)
            if sub_type == c.Point.Definition.INTERSECTION:
                return Intersection(None)
        if type == 'polygon':
            return Polygon(None)
        if type == 'colour':
            return Colour(None)


    # The following method, strickly speaking, are not part of the factory
    # but only auxiliary methods helping the use of the factory.

    @staticmethod
    def create_dictionary(type, sub_type, definition, items):
        dictionary = {}
        id = Factory.next_id(items, type, definition)
        if type == 'point':
            dictionary = Point.dictionary_builder(definition, id, sub_type)
        if type == 'segment':
            dictionary = Segment.dictionary_builder(definition, id)
        dictionary["type"] = type
        if sub_type:
            dictionary["sub_type"] = sub_type

        return dictionary


    @staticmethod
    def next_id(item, definition, items):
        class Alphabet(object):
            def __init__(self, start, stop, type, definition):
               self.start = start
               self.stop = stop
               self.type = type
               self.definition = definition

            def __iter__(self): return self
            def __next__(self):
                if self.start >= self.stop:
                    raise StopIteration
                current = item.next_id_func(definition, self.start)
                self.start += 1
                return current

        iterator = Alphabet(0, 10000, type, definition) # 10000 is a big enough number

        for alpha in iterator:
            if alpha not in items:
                return alpha
