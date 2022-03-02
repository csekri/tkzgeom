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

    def delete(self, items):
        dependents = self.being_depended_on(items)
        for item in dependents:
            items[item].delete(items)
        if self.get_id() in items:
            del items[self.get_id()]

    def recompute_canvas(self, items, window, width, height):
        return NotImplementedError
        # if isinstance(self, Point):
        #     if isinstance(self, FreePoint):
        #         self.set_canvas_coordinates(*phi(window, self.item["definition"]["x"], self.item["definition"]["y"], width, height))
        #     if isinstance(self, Midpoint):
        #         x1, y1 = items[self.depends_on()[0]].get_canvas_coordinates()
        #         x2, y2 = items[self.depends_on()[0]].get_canvas_coordinates()
        #         self.set_canvas_coordinates(x1/2 + x2/2, y1/2 + y2/2)

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

    def definition_builder(self, data, items=None):
        return NotImplementedError

    def dictionary_builder(self, definition, id, sub_type=None):
        return NotImplementedError

    def __str__(self):
        raise NotImplementedError
