class DashPatternable:
    def __init__(self, item):
        """Construct DashPatternable."""
        self.item = item

    def tikzify_dash(self):
        """Turn dash pattern into tikz code."""
        if self.item["line"]["dash"]["stroke"] == 'solid':
            return ''
        if self.item["line"]["dash"]["stroke"] == 'custom':
            string = 'dash pattern='
            for i, length in enumerate(self.item["line"]["dash"]["custom_pattern"]):
                if i % 2 == 0:
                    string += "on %s pt" % str(length)
                else:
                    string += "off %s pt" % str(length)
                if i < len(self.item["line"]["dash"]["custom_pattern"])-1:
                    string += ' '
            return string
        return self.item["line"]["dash"]["stroke"]
