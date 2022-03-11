from PointClasses.FreePoint import FreePoint
import Constant as c
from Factory import Factory


def free_point_checkbox(dialog, state):
    dialog.free_point = bool(state)


def turn_into_free_point(item, scene):
    id_ = item.item["id"]
    item.recompute_canvas(scene.project_data.items,
                          scene.project_data.window,
                          *scene.init_canvas_dims)
    canvas_coords = item.get_canvas_coordinates()
    tikz_coords = FreePoint.phi_inverse(scene.project_data.window,
                                        *item.get_canvas_coordinates(),
                                        *scene.init_canvas_dims)
    item = Factory.create_empty_item('point', c.Point.Definition.FREE)
    definition = dict(zip(['x', 'y'], tikz_coords))
    item.item["id"] = id_
    item.item["definition"] = definition
    item.set_canvas_coordinates(*canvas_coords)
    return item
