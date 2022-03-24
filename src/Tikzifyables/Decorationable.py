import Constant as c

class Decorationable:
    def __init__(self, item):
        """Construct Decorationable."""
        self.item = item

    def tikzify_decoration(self):
        """Turn curve decoration into tikz code."""
        if self.item["line"]["decoration"]["type"] == c.DecorationType.NONE:
            return ''
        if self.item["line"]["decoration"]["type"] == c.DecorationType.TEXT_ALONG_CURVE:
            return 'decoration={%s, text={%s}}, decorate'\
            % (c.DecorationType.TEXT_ALONG_CURVE, self.item["line"]["decoration"]["text"])
        else:
            return 'decoration={%s, amplitude=%s, segment length=%s}, decorate'\
            % (self.item["line"]["decoration"]["type"],\
            self.item["line"]["decoration"]["amplitude"],\
            self.item["line"]["decoration"]["wavelength"])
