import Constant as c
from Colour import Colour

def fill_segment_fields(scene):
    ids = scene.list_focus_ids
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'segment':
        return
    segment = scene.project_data.items[ids[0]].item

    scene.ui.segment_line_width_slider.setValue(10.0 * segment["line"]["line_width"])
    scene.ui.segment_line_width_spin.setValue(segment["line"]["line_width"])

    scene.skip_combobox_changes = True
    scene.ui.segment_line_stroke.setCurrentIndex(c.attribute_values(c.Line_Stroke).index(segment["line"]["dash"]["stroke"]))
    scene.skip_combobox_changes = False

    scene.ui.segment_custom_dash.setText(' '.join(map(str, segment["line"]["dash"]["custom_pattern"])))

    scene.ui.segment_double_distance_slider.setValue(10.0 * segment["line"]["double"]["distance"])
    scene.ui.segment_double_distance_spin.setValue(segment["line"]["double"]["distance"])
