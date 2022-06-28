import Constant as c

def point_radio_func(main_window):
    """Connect point radio button."""
    main_window.scene.select_mode.set_mode(0, main_window.point_combo.currentIndex(), True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def segment_radio_func(main_window):
    """Connect segment radio button."""
    main_window.scene.select_mode.set_mode(1, 0, True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def circle_radio_func(main_window):
    """Connect circle radio button."""
    main_window.scene.select_mode.set_mode(2, main_window.circle_combo.currentIndex(), True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type(), True)


def polygon_radio_func(main_window):
    """Connect polygon radio button."""
    main_window.scene.select_mode.set_mode(1, 1, True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def linestring_radio_func(main_window):
    """Connect linestring radio button."""
    main_window.scene.select_mode.set_mode(1, 2, True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def angle_radio_func(main_window):
    """Connect angle radio button."""
    main_window.scene.select_mode.set_mode(4, 0, True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def right_angle_radio_func(main_window):
    """Connect right angle radio button."""
    main_window.scene.select_mode.set_mode(4, 1, True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def cloud_radio_func(main_window):
    """Connect point cloud radio button."""
    main_window.scene.select_mode.set_mode(6, main_window.cloud_combo.currentIndex(), True)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type(), True)


def point_combo_func(value, main_window):
    """Connect point comboBox."""
    main_window.scene.select_mode.set_mode(0, value, False)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def circle_combo_func(value, main_window):
    """Connect circle comboBox."""
    main_window.scene.select_mode.set_mode(2, value, False)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())


def cloud_combo_func(value, main_window):
    """Connect point cloud comboBox."""
    main_window.scene.select_mode.set_mode(6, value, False)
    main_window.ui.statusBar().showMessage(c.TOOL_TO_STATUSBAR_MESSAGE[main_window.scene.select_mode.get_type()])
    print(main_window.scene.select_mode.get_type())
