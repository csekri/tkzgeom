from Items import Items
from Item import Item
from Point import Point
from Segment import Segment
from Factory import Factory
import os

import json

# d = {
#         "points" : [ { "id" : "A", "x" : 3.11, "y": 1.2, "from": ["B"], "label": { "text": "$A$" } },
#                      { "id" : "B", "x" : 3.11, "y": 1.2, "from": [], "label": { "text": "$B$" } } ],
#         "segments" : [ { "id" : "AB", "from" : "A", "to": "B", "o_arrow": {"length": 1.0, "width": 1.25, "tip": "latex"}, "d_arrow": {"length": 1.0, "width": 1.35, "tip": "stealth"}, "line_stroke": "custom", "line_stroke_custom": [5, 2] } ]
# }

with open('../../oop.json') as f:
    d = json.load(f)

items = Items()

for item in (d["items"]):
    items.add(Factory.create_item(item))


string ="""
\\documentclass{standalone}
\\usepackage{tikz, tkz-euclide}
\\usetikzlibrary{positioning, backgrounds, shapes}

\\begin{document}
\\begin{tikzpicture}
%s
\\end{tikzpicture}
\\end{document}
""" % items.tikzify()
with open('try.tex', 'w') as f:
    f.write(string)
os.system('pdflatex try.tex')
# for item in items.items:
#     if item.get_id() == "C":
#         item.delete(items)
#         break
# print(items)
print(string)
