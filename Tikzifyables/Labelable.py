class Labelable:
    def __init__(self, item):
        self.label = item["label"]
        self.id = item["id"]
        self.item = item

    def tikzify_label(self):
        option = ''
        if self.item["label"]["offset"] != 0.0:
            option = self.item["label"]["anchor"] + '=' + str(self.item["label"]["offset"])
        elif self.item["label"]["anchor"] != 'below right':
            option = self.item["label"]["anchor"]

        if option:
            return "\\tkzLabelPoint[%s](%s){%s}" % (option, self.item["id"], self.item["label"]["text"])
        else:
            return "\\tkzLabelPoint(%s){%s}" % (self.item["id"], self.item["label"]["text"])
