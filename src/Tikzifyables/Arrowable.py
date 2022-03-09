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
    def arrow_tip_splitter(tip_str):
        splitted = tip_str.split('^')
        if len(splitted) == 2:
            if splitted[1] == 'o':
                return splitted[0], 'open'
            if splitted[1] == 'r':
                return splitted[0], 'round'
            if splitted[1] == 'or':
                return splitted[0], 'open, round'
        else:
            return splitted[0] ,''

    @staticmethod
    def tikzify_arrow(arrow):
        if arrow["tip"] == 'None':
            return ''
        options = []
        if arrow["length"] == arrow["width"] == 1.0:
            options = []
        elif arrow["length"] == arrow["width"]:
            options.append(f'scale={arrow["length"]}')
        else:
            options.append(f'scale length={arrow["length"]}, scale width={arrow["width"]}')
        arrow_tip, arrow_extra = Arrowable.arrow_tip_splitter(arrow["tip"])
        options.append(arrow_extra)
        options.append(arrow["side"])
        if arrow["reversed"]:
            options.append('reversed')
        if 'bending' in arrow and arrow["bending"]:
            options.append('bend')
        options = list(filter(bool, options))
        if not options:
            return arrow_tip
        return '{%s[%s]}' % (arrow_tip, ', '.join(options))
