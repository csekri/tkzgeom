from Tikzifyables.Colourable.Colourable import Colourable

class LineColourable(Colourable):
    def __init__(self, item):
        self.item = item

    def tikzify_line_colour(self):
        return self.tikzify_colour(self.item["line"]["colour"])
