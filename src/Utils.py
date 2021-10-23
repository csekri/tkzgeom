from PyQt5 import QtCore, QtWidgets, QtGui, uic
import json
from collections import namedtuple

save_state = namedtuple('save_state', 'opened_file unsaved_progress')


def read_eucl_file(fname):
    with open(fname) as f:
        eucl = json.load(f)
    return eucl


def save_eucl_file(fname, eucl):
    with open(fname, 'w') as outfile:
        json.dump(eucl, outfile, indent=4)


def save_as(self):
    """
    SUMMARY
        equivalent to "Save As", brings up save popup window in any case

    PARAMETERS
        nothing

    RETURNS
        None
    """
    fname = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption="Save file", filter="JavaScript Object Notation / .json (*.json *.JSON)")
    if fname[0] != '':
        self.scene.save_state = save_state(fname[0], False)
        save_eucl_file(fname[0], self.scene.eucl)
        self.scene.save_state = save_state(fname[0], 0)

def save(self):
    """
    SUMMARY
        when CTRL+S save option is chosen creates new file if no file is open,
        save into opened file otherwise

    PARAMETERS
        nothing

    RETURNS
        None
    """
    if self.scene.save_state.opened_file != '' and self.scene.save_state.unsaved_progress != 0:
        save_eucl_file(self.scene.save_state.opened_file, self.scene.eucl)
        self.scene.save_state = save_state(self.scene.save_state.opened_file, 0)
        self.scene.actionSave.setEnabled(False)
    else:
        save_as(self)


def point_change_id(eucl, from_id, to_id, mapped_points):
    point_id_set = []
    for point in eucl["points"]:
        point_id_set.append(point["id"])

    if to_id in point_id_set:
        return
    else:
        mapped_points[to_id] = mapped_points[from_id]
        del mapped_points[from_id]
        for point in eucl["points"]:
            if point["id"] == from_id:
                point["id"] = to_id
                if point["label"]["text"] == ('$%s$' % from_id):
                    point["label"]["text"] = '$%s$' % to_id
            if point["from"]["type"] == "point_on_line":
                if point["from"]["A"] == from_id:
                    point["from"]["A"] = to_id
                if point["from"]["B"] == from_id:
                    point["from"]["B"] = to_id

            if point["from"]["type"] == "intersection_ll":
                if point["from"]["A"] == from_id:
                    point["from"]["A"] = to_id
                if point["from"]["B"] == from_id:
                    point["from"]["B"] = to_id
                if point["from"]["C"] == from_id:
                    point["from"]["C"] = to_id
                if point["from"]["D"] == from_id:
                    point["from"]["D"] = to_id
            if point["from"]["type"] == "intersection_lc":
                if point["from"]["A"] == from_id:
                    point["from"]["A"] = to_id
                if point["from"]["B"] == from_id:
                    point["from"]["B"] = to_id
            if point["from"]["type"] == "segment_midpoint":
                    if point["from"]["A"] == from_id:
                        point["from"]["A"] = to_id
                    if point["from"]["B"] == from_id:
                        point["from"]["B"] = to_id
            if point["from"]["type"] == "projection_point":
                    if point["from"]["A"] == from_id:
                        point["from"]["A"] = to_id
                    if point["from"]["B"] == from_id:
                        point["from"]["B"] = to_id
                    if point["from"]["P"] == from_id:
                        point["from"]["P"] = to_id
            if point["from"]["type"] == "bisector_point":
                    if point["from"]["A"] == from_id:
                        point["from"]["A"] = to_id
                    if point["from"]["B"] == from_id:
                        point["from"]["B"] = to_id
                    if point["from"]["C"] == from_id:
                        point["from"]["C"] = to_id
            if point["from"]["type"] == "translation_point":
                    if point["from"]["A"] == from_id:
                        point["from"]["A"] = to_id
                    if point["from"]["B"] == from_id:
                        point["from"]["B"] = to_id
                    if point["from"]["P"] == from_id:
                        point["from"]["P"] = to_id
            if point["from"]["type"] == "orthogonal_point":
                    if point["from"]["A"] == from_id:
                        point["from"]["A"] = to_id
                    if point["from"]["B"] == from_id:
                        point["from"]["B"] = to_id
            if point["from"]["type"] == "rotation":
                    if point["from"]["A"] == from_id:
                        point["from"]["A"] = to_id
                    if point["from"]["B"] == from_id:
                        point["from"]["B"] = to_id

        for segment in eucl["segments"]:
            if segment["id"] == 'sg_default':
                continue
            if segment["points"]["from"] == from_id:
                segment["points"]["from"] = to_id
            if segment["points"]["to"] == from_id:
                segment["points"]["to"] = to_id

        for circle in eucl["circles"]:
            if circle["type"] == "two_point_circle":
                if circle["points"]["O"] == from_id:
                    circle["points"]["O"] = to_id
                if circle["points"]["A"] == from_id:
                    circle["points"]["A"] = to_id
            if circle["type"] in ["circum_circle", "inscribed_circle"]:
                if circle["points"]["A"] == from_id:
                    circle["points"]["A"] = to_id
                if circle["points"]["B"] == from_id:
                    circle["points"]["B"] = to_id
                if circle["points"]["C"] == from_id:
                    circle["points"]["C"] = to_id
            if circle["type"] == "arc":
                if circle["points"]["O"] == from_id:
                    circle["points"]["O"] = to_id
                if circle["points"]["A"] == from_id:
                    circle["points"]["A"] = to_id
                if circle["points"]["B"] == from_id:
                    circle["points"]["B"] = to_id
            if circle["type"] == "sector":
                if circle["points"]["O"] == from_id:
                    circle["points"]["O"] = to_id
                if circle["points"]["A"] == from_id:
                    circle["points"]["A"] = to_id
                if circle["points"]["B"] == from_id:
                    circle["points"]["B"] = to_id
        for angle in eucl["angles"]:
            if angle["id"] == "ang_default":
                continue
            if angle["points"]["A"] == from_id:
                angle["points"]["A"] = to_id
            if angle["points"]["B"] == from_id:
                angle["points"]["B"] = to_id
            if angle["points"]["C"] == from_id:
                angle["points"]["C"] = to_id

        for polygon in eucl["polygons"]:
            if polygon["id"] == 'pol_default':
                continue
            for i in range(len(polygon["points"])):
                if polygon["points"][i] == from_id:
                    polygon["points"][i] = to_id

def delete_point(eucl, index, mapped_points):
    del_points = [eucl["points"][index]]
    del_points_copy = [eucl["points"][index]]

    while len(del_points) > 0:
        del_point = del_points.pop()
        del_point_id = del_point["id"]
        for i, point in enumerate(eucl["points"]):
            if point["id"] == 'pt_default':
                continue
            if point["from"]["type"] == "point_on_line":
                if del_point_id in [point["from"]["A"], point["from"]["B"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "intersection_ll":
                if del_point_id in [point["from"]["A"], point["from"]["B"],
                                    point["from"]["C"], point["from"]["D"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "intersection_lc":
                if del_point_id in [point["from"]["A"], point["from"]["B"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "segment_midpoint":
                if del_point_id in [point["from"]["A"], point["from"]["B"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "projection_point":
                if del_point_id in [point["from"]["A"], point["from"]["B"], point["from"]["P"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "bisector_point":
                if del_point_id in [point["from"]["A"], point["from"]["B"], point["from"]["C"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "translation_point":
                if del_point_id in [point["from"]["A"], point["from"]["B"], point["from"]["P"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "orthogonal_point":
                if del_point_id in [point["from"]["A"], point["from"]["B"]]:
                    del_points.append(point)
                    del_points_copy.append(point)
            if point["from"]["type"] == "rotation":
                if del_point_id in [point["from"]["A"], point["from"]["B"]]:
                    del_points.append(point)
                    del_points_copy.append(point)

    for point in del_points_copy:
        for i in range(len(eucl["points"])):
            if eucl["points"][i]["id"] == point["id"]:
                del eucl["points"][i]
                break

    point_ids = list(map(lambda x: x["id"], eucl["points"]))

    del_segments = []
    for segment in eucl["segments"]:
        if segment["id"] == 'sg_default':
            continue
        if (segment["points"]["from"] not in point_ids) or (segment["points"]["to"] not in point_ids):
            del_segments.append(segment)

    for segment in del_segments:
        for i in range(len(eucl["segments"])):
            if eucl["segments"][i]["id"] == segment["id"]:
                del eucl["segments"][i]
                break

    del_circles = []
    for circle in eucl["circles"]:
        if circle["type"] == "two_point_circle":
            if (circle["points"]["O"] not in point_ids) or (circle["points"]["A"] not in point_ids):
                del_circles.append(circle)
        if circle["type"] in ["circum_circle", "inscribed_circle"]:
            if (circle["points"]["A"] not in point_ids) or (circle["points"]["B"] not in point_ids) or \
               (circle["points"]["C"] not in point_ids):
                del_circles.append(circle)
        if circle["type"] in ["arc", "sector"]:
            if (circle["points"]["O"] not in point_ids) or (circle["points"]["A"] not in point_ids) or \
               (circle["points"]["B"] not in point_ids):
                del_circles.append(circle)

    for circle in del_circles:
        for i in range(len(eucl["circles"])):
            if eucl["circles"][i]["id"] == circle["id"]:
                del eucl["circles"][i]
                break

    del_angles = []
    for angle in eucl["angles"]:
        if angle["id"] == "ang_default":
            continue
        if (angle["points"]["A"] not in point_ids) or (angle["points"]["B"] not in point_ids) or \
           (angle["points"]["C"] not in point_ids):
            del_angles.append(angle)

    for angle in del_angles:
        for i in range(len(eucl["angles"])):
            if eucl["angles"][i]["id"] == angle["id"]:
                del eucl["angles"][i]
                break

    del_polygons = []
    for polygon in eucl["polygons"]:
        if polygon["id"] == 'pol_default':
            continue
        for i in range(len(polygon["points"])):
            if polygon["points"][i] not in point_ids:
                del_polygons.append(polygon)

    for polygon in del_polygons:
        for i in range(len(eucl["polygons"])):
            if eucl["polygons"][i]["id"] == polygon["id"]:
                del eucl["polygons"][i]
                break
