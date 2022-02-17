class Labelable:
    def __init__(self, item):
        self.label = item["label"]
        self.id = item["id"]

    def tikzify_label(self):
        option = ''
        if self.label["offset"] != 0.0:
            option = self.label["anchor"] + '=' + str(self.label["offset"])
        elif self.label["anchor"] != 'below right':
            option = self.label["anchor"]

        if option:
            print(self.id)
            return "\\tkzLabelPoint[%s](%s){%s}" % (option, self.id, self.label["text"])
        else:
            return "\\tkzLabelPoint(%s){%s}" % (self.id, self.label["text"])
