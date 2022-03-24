import Constant as c
from Colour import Colour
from Fill.FillMacros import fill_colour, fill_dash


def fill_point_fields(scene):
    """Fill all widgets in the point tab."""
    ids = scene.list_focus_ids
    colours = c.attribute_values(c.Colour) \
              + [i.get_id() for i in scene.project_data.items.values() if isinstance(i, Colour)]
    if not ids:
        return
    if c.TYPES[scene.current_tab_idx] != 'point':
        return
    point = scene.project_data.items[ids[0]].item

    scene.ui.point_def_str.setText(scene.project_data.items[ids[0]].definition_string())
    scene.skip_plaintextedit_changes = True
    scene.ui.plainTextEdit.setPlainText(point["marker"]["text"])
    scene.skip_plaintextedit_changes = False
    scene.skip_combobox_changes = True
    scene.ui.point_marker_shape.setCurrentIndex(c.attribute_values(c.MarkerShape).index(point["marker"]["shape"]))
    scene.ui.point_anchor.setCurrentIndex(c.attribute_values(c.Direction).index(point["label"]["anchor"]))
    scene.skip_combobox_changes = False
    scene.skip_checkbox_changes = True
    scene.ui.point_show_label.setChecked(point["label"]["show"])
    scene.skip_checkbox_changes = False

    scene.ui.point_size_slider.setValue(point["marker"]["size"])
    scene.ui.point_size_spin.setValue(point["marker"]["size"])

    scene.ui.point_shape_number_slider.setValue(point["marker"]["shape_number"])
    scene.ui.point_shape_number_spin.setValue(point["marker"]["shape_number"])

    scene.ui.point_inner_sep_slider.setValue(point["marker"]["inner_sep"])
    scene.ui.point_inner_sep_spin.setValue(point["marker"]["inner_sep"])

    scene.ui.point_ratio_slider.setValue(-10 + 20 * point["marker"]["ratio"])
    scene.ui.point_ratio_spin.setValue(point["marker"]["ratio"])

    scene.ui.point_text_width_slider.setValue(point["marker"]["text_width"])
    scene.ui.point_text_width_spin.setValue(point["marker"]["text_width"])

    scene.ui.point_line_width_slider.setValue(10.0 * point["line"]["line_width"])
    scene.ui.point_line_width_spin.setValue(point["line"]["line_width"])

    scene.ui.point_label_text.setText(point["label"]["text"])

    scene.ui.point_offset_slider.setValue(10 + point["label"]["offset"])
    scene.ui.point_offset_spin.setValue(point["label"]["offset"])

    scene.ui.point_rounded_corners_slider.setValue(4 * point["marker"]["rounded_corners"])
    scene.ui.point_rounded_corners_spin.setValue(point["marker"]["rounded_corners"])

    fill_colour(scene, point["fill"]["colour"], colours,
                scene.ui.point_marker_colour_name,
                scene.ui.point_marker_colour_mix_name,
                scene.ui.point_marker_colour_mixratio_spin,
                scene.ui.point_marker_colour_mixratio_slider,
                scene.ui.point_marker_colour_strength_spin,
                scene.ui.point_marker_colour_strength_slider)

    fill_dash(scene, point["line"]["dash"], scene.ui.point_line_stroke, scene.ui.point_custom_dash)

    fill_colour(scene, point["line"]["colour"], colours,
                scene.ui.point_border_colour_name,
                scene.ui.point_border_colour_mix_name,
                scene.ui.point_border_colour_mixratio_spin,
                scene.ui.point_border_colour_mixratio_slider,
                scene.ui.point_border_colour_strength_spin,
                scene.ui.point_border_colour_strength_slider)
