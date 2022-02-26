class Labelable:
    def __init__(self, item):
        self.item = item

    def tikzify_label(self):
        if not self.item["label"]["show"]:
            return ''
        option = ''
        if self.item["label"]["offset"] != 0.0:
            option = f'{self.item["label"]["anchor"]}={str(self.item["label"]["offset"])}pt'
        elif self.item["label"]["anchor"] != 'below right':
            option = self.item["label"]["anchor"]

        if option:
            return "\\tkzLabelPoint[%s](%s){%s}" % (option, self.item["id"], self.item["label"]["text"])
        else:
            return "\\tkzLabelPoint(%s){%s}" % (self.item["id"], self.item["label"]["text"])
