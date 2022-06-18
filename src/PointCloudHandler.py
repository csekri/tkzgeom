import Constant as c
from HighlightItem import item_in_focus
from Dialogs.MakeGridDialog import  MakeGridDialog
from Dialogs.RegularPolygonDialog import RegularPolygonDialog
from Dialogs.CompleteGraphDialog import CompleteGraphDialog
from Dialogs.StarGraphDialog import StarGraphDialog


def select_point_cloud(scene):
    """Select point cloud."""
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
    if scene.select_mode.get_type() == c.Tool.COMPLETE_GRAPH:
        if ids := scene.select_history.match_pattern(['pp']):
            dialog = CompleteGraphDialog(scene, ids)
            dialog.exec_()
            return True
    if scene.select_mode.get_type() == c.Tool.STAR_GRAPH:
        if ids := scene.select_history.match_pattern(['pp']):
            dialog = StarGraphDialog(scene, ids)
            dialog.exec_()
            return True

    return False
