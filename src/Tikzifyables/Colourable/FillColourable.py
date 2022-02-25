from Tikzifyables.Colourable.Colourable import Colourable

class FillColourable(Colourable):
    def __init__(self, item):
        self.item = item

    def tikzify_fill_colour(self):
        return self.tikzify_colour(self.item["fill"]["colour"])
