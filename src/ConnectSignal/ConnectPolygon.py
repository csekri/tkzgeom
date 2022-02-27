import Constant as c
from ConnectSignal.Lambda import (
    connect_plain_text_edit_abstract,
    connect_text_edit_pushbutton_apply_abstract,
    connect_combobox_abstract,
    connect_checkbox_abstract,
    connect_slider_moved_abstract,
    connect_slider_released_abstract,
    connect_dash_lineedit_abstract,
    connect_lineedit_abstract
)

from ConnectSignal.ConnectMacros import connect_colour, connect_fill_pattern

def connect_polygon(scene):
    connect_colour(scene, ['fill', 'colour'],
        scene.ui.polygon_marker_colour_name,
        scene.ui.polygon_marker_colour_mix_name,
        scene.ui.polygon_marker_colour_mixratio_spin,
        scene.ui.polygon_marker_colour_mixratio_slider,
        scene.ui.polygon_marker_colour_strength_spin,
        scene.ui.polygon_marker_colour_strength_slider)
    connect_fill_pattern(scene, ['fill', 'pattern'],
        scene.ui.polygon_pattern_type,
        scene.ui.polygon_pattern_distance_spin,
        scene.ui.polygon_pattern_distance_slider,
        scene.ui.polygon_pattern_size_spin,
        scene.ui.polygon_pattern_size_slider,
        scene.ui.polygon_pattern_rotation_spin,
        scene.ui.polygon_pattern_rotation_slider,
        scene.ui.polygon_pattern_xshift_spin,
        scene.ui.polygon_pattern_xshift_slider,
        scene.ui.polygon_pattern_yshift_spin,
        scene.ui.polygon_pattern_yshift_slider)
