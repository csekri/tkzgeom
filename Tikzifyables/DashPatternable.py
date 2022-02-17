class DashPatternable:
    def __init__(self, item):
        self.dash = item["line"]["dash"]["stroke"]
        self.dash_custom = item["line"]["dash"]["custom_pattern"]

    def tikzify_dash(self):
        if self.dash == 'solid':
            return ''
        if self.dash == 'custom':
            string = 'dash pattern='
            for i, length in enumerate(self.dash_custom):
                if i % 2 == 0:
                    string += "on %s pt" % str(length)
                else:
                    string += "off %s pt" % str(length)
                if i < len(self.dash_custom)-1:
                    string += ' '
            return string
        return self.dash
