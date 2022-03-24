from PointClasses.FreePoint import FreePoint
from PointClasses.Midpoint import Midpoint
from Segment import Segment
import Constant as c
from copy import copy


class SelectMode:
    def __init__(self):
        """Construct SelectMode."""
        self.type_index = 0
        self.sub_type_index = dict(zip(list(range(10)), 10*[0]))

    def get_type(self):
        """Return selection tool type."""
        return 100 * self.type_index + self.sub_type_index[self.type_index]

    def set_mode(self, type_index, sub_type_index, set_type):
        """Set selection mode."""
        if set_type:
            self.type_index = type_index
        if sub_type_index is not None:
            self.sub_type_index[type_index] = sub_type_index


class ItemAccumulator:
    def __init__(self):
        """Construct ItemAccumulator."""
        self.id_history = []
        self.type_history = ''
        self.type_map = { 'point': 'p', 'segment': 's', 'circle': 'c', 'polygon': 'o' }

    @staticmethod
    def is_prefix(pref: str, word: str):
        """Check if pref is prefix of word."""
        if word.find(pref) == 0:
            return True
        else:
            return False

    def add_to_history(self, item_id, item_type):
        """Update selection history."""
        self.id_history.append(item_id)
        self.type_history += self.type_map[item_type]

    def reset_history(self):
        """Reset history."""
        self.type_history = ''
        self.id_history.clear()

    def match_pattern(self, patterns):
        """Check if selection can be completed."""
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
