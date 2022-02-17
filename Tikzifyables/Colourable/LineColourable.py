from Tikzifyables.Colourable.Colourable import Colourable

class LineColourable(Colourable):
    def __init__(self, item):
        self.line_colour = item["line"]["colour"]

    def tikzify_line_colour(self):
        return self.tikzify_colour(self.line_colour)
