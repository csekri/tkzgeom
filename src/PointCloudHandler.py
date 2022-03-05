import Constant as c
from HighlightItem import item_in_focus
from Dialogs.MakeGridDialog import  MakeGridDialog
from Dialogs.RegularPolygonDialog import RegularPolygonDialog


def select_point_cloud(scene):
    focus = item_in_focus(scene.project_data, scene.mouse)
    if not bool(focus):
        scene.select_history.reset_history()
        return False
    scene.select_history.add_to_history(focus, scene.project_data.items[focus].item["type"])
    if scene.select_mode.get_type() == c.Tool.MAKEGRID:
        if ids := scene.select_history.match_pattern(['ppp']):
            dialog = MakeGridDialog(scene, ids)
            dialog.exec_()
            return True
    if scene.select_mode.get_type() == c.Tool.REGULAR_POLYGON:
        if ids := scene.select_history.match_pattern(['pp']):
            dialog = RegularPolygonDialog(scene, ids)
            dialog.exec_()
            return True
    return False
