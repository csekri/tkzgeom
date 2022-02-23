class Arrowable:
    def __init__(self, item):
        self.item = item

    def tikzify_arrows(self):
        o_str = Arrowable.tikzify_arrow(self.item["o_arrow"])
        d_str = Arrowable.tikzify_arrow(self.item["d_arrow"])
        if not (o_str or d_str):
            return ''
        return o_str + '-' + d_str

    @staticmethod
    def tikzify_arrow(arrow):
        if arrow["tip"] == 'None':
            return ''
        options = ''
        if arrow["length"] == arrow["width"] == 1.0:
            options = ''
        elif arrow["length"] == arrow["width"]:
            options = f'scale={arrow["length"]}'
        else:
            options = 'scale length=%s, width=%s' % (arrow["length"], arrow["width"])
        if options == '':
            return arrow["tip"]
        return '{%s[%s]}' % (arrow["tip"], options)
