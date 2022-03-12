import re
import Constant as c

def phi(window, x, y, width, height):
    return window.left + x / width * window.scale*10.0,\
        window.top - y / height * window.scale*10.0


class Item(object):
    def __init__(self, item=None):
        self.item = item

    def get_id(self):
        return self.item["id"]

    def depends_on(self):
        return list(self.item["definition"].values())

    def being_depended_on(self, items):
        dependent_set = set()
        for item in items.values():
            if self.get_id() in item.depends_on():
                dependent_set.add(item.get_id())
        return dependent_set

    def deep_depends_on(self, items):
        accumulator_set = set()
        depends = self.depends_on()
        if depends:
            accumulator_set |= set(depends)
            for id in depends:
                accumulator_set |= items[id].deep_depends_on(items)
        return accumulator_set

    def delete(self, items):
        dependents = self.being_depended_on(items)
        for item in dependents:
            if item in items:
                items[item].delete(items)
        if self.get_id() in items:
            del items[self.get_id()]

    def recompute_canvas(self, items, window, width, height):
        return NotImplementedError

    def change_id(self, from_id, to_id):
        if self.get_id() == from_id:
            self.item["id"] = to_id
            return # return because there is no self reference
        if from_id in self.depends_on():
            for key, value in self.item["definition"].items():
                if value == from_id and value in self.depends_on():
                    self.item["definition"][key] = to_id

    def tikzify(self):
        raise NotImplementedError

    def parse_into_definition(self, arguments, items):
        raise NotImplementedError

    def name_pattern(self, argument):
        pattern = r"""^([a-zA-Z0-9]+'*[_-]?)+$"""
        return re.search(pattern, argument)

    @staticmethod
    def name_pattern_static(argument):
        pattern = r"""^([a-zA-Z0-9]+'*[_-]?)+$"""
        return re.search(pattern, argument)

    def definition_builder(self, data, items=None):
        return NotImplementedError

    def definition_string(self):
        type, sub_type = self.item["type"], self.item["sub_type"]
        parse_name = list(c.PARSE_TO_TYPE_MAP.keys())[list(c.PARSE_TO_TYPE_MAP.values()).index((type, sub_type))]
        def_str = [('{0:.6g}'.format(i) if isinstance(i, float) else i) for i in self.item["definition"].values()]
        return '%s(%s)' % (parse_name, ', '.join(def_str))

    def dictionary_builder(self, definition, id, sub_type=None):
        return NotImplementedError

    def __str__(self):
        raise NotImplementedError
