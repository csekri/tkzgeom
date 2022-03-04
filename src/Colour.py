from Item import Item


class Colour(Item):
    def __init__(self, item):
        Item.__init__(self, item)
        if item is None:
            self.dictionary_builder(None, "")

    def depends_on(self):
        return []

    def tikzify(self):
        return '\\definecolor{%s}{HTML}{%s}' % (self.item["id"], self.item["definition"][1:])

    def next_id_func(self, definition, iter_counter):
        return 'Colour_' + chr(ord('A') + iter_counter % 26) + (iter_counter // 26) * '\''
