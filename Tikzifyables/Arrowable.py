class Arrowable:
    def __init__(self, item):
        self.o_arrow = Arrow(item["o_arrow"])
        self.d_arrow = Arrow(item["d_arrow"])
        
    def tikzify_arrow(self):
        o_str = self.o_arrow.tikzify()
        d_str = self.d_arrow.tikzify()
        if not (o_str and d_str):
            return ''
        return o_str + '-' + d_str



class Arrow:
    def __init__(self, arrow):
        self.length = arrow["length"]
        self.width = arrow["width"]
        self.tip = arrow["tip"]
        
    def tikzify(self):
        if self.tip == 'None':
            return ''
        return '{%s[length=%s, width=%s]}' % (self.tip, self.length, self.width)
