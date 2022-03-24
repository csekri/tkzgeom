from Tikzifyables.Colourable.Colourable import Colourable


class LineColourable(Colourable):
    def __init__(self, item):
        """Construct LineColourable."""
        self.item = item

    def tikzify_line_colour(self):
        """Convert line colour into tikz code."""
        return self.tikzify_colour(self.item["line"]["colour"])
