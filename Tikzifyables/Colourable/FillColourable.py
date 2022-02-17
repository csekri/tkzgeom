from Tikzifyables.Colourable.Colourable import Colourable

class FillColourable(Colourable):
    def __init__(self, item):
        self.fill_colour = item["fill"]["colour"]

    def tikzify_fill_colour(self):
        return self.tikzify_colour(self.fill_colour)
