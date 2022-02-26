from Tikzifyables.Colourable.Colourable import Colourable

class Doubleable(Colourable):
    def __init__(self, item):
        self.item = item

    def tikzify_double(self):
        if self.item["line"]["double"]["distance"] == 0.0:
            return ''
        colour = self.tikzify_colour(self.item["line"]["double"]["colour"])
        options = [
            'double' if colour else f'double={colour}',
            f'double distance={self.item["line"]["double"]["distance"]}'
        ]
        return ', '.join(options)
