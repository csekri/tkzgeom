from Tikzifyables.Colourable.Colourable import Colourable


class FillColourable(Colourable):
    def __init__(self, item):
        """Construct FillColourable."""
        self.item = item

    def tikzify_fill_colour(self):
        """Convert fill colour into tikz code."""
        return self.tikzify_colour(self.item["fill"]["colour"])
