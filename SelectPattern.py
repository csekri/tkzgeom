from PointClasses.FreePoint import FreePoint
from PointClasses.Midpoint import Midpoint
from Segment import Segment
import Constant as c
from copy import copy


class SelectMode:
    def __init__(self, type_index, sub_type_index):
        self.type_index = type_index
        self.sub_type_index = sub_type_index

    def get_type(self):
        return 100 * self.type_index  + self.sub_type_index

    def set_mode(self, type_index, sub_type_index):
        if type_index is not None:
            self.type_index = type_index
        if sub_type_index is not None:
            self.sub_type_index = sub_type_index


class ItemAccumulator:
    def __init__(self):
        self.id_history = []
        self.type_history = ''
        self.type_map = { 'point': 'p', 'segment': 's', 'circle': 'c', 'polygon': 'o' }

    @staticmethod
    def is_prefix(pref: str, word: str):
        if word.find(pref) == 0:
            return True
        else:
            return False

    def add_to_history(self, item_id, item_type):
        self.id_history.append(item_id)
        self.type_history += self.type_map[item_type]

    def reset_history(self):
        self.type_history = ''
        self.id_history.clear()


    def match_pattern(self, patterns):
        print('type', self.type_history)
        if any(map(lambda x: ItemAccumulator.is_prefix(self.type_history, x), patterns)):
            if self.type_history in patterns:
                ids_copy = copy(self.id_history)
                self.reset_history()
                return ids_copy
        else:
            self.reset_history()
        return None






#
