

def point_radio_func(main_window):
    main_window.scene.select_mode.set_mode(0, main_window.point_combo.currentIndex())
    print(main_window.scene.select_mode.get_type())

def segment_radio_func(main_window):
    main_window.scene.select_mode.set_mode(1, 0)
    print(main_window.scene.select_mode.get_type())

def circle_radio_func(main_window):
    main_window.scene.select_mode.set_mode(2, main_window.circle_combo.currentIndex())
    print(main_window.scene.select_mode.get_type())

def polygon_radio_func(main_window):
    main_window.scene.select_mode.set_mode(1, 1)
    print(main_window.scene.select_mode.get_type())

def linestring_radio_func(main_window):
    main_window.scene.select_mode.set_mode(1, 2)
    print(main_window.scene.select_mode.get_type())

def angle_radio_func(main_window):
    main_window.scene.select_mode.set_mode(4, 0)
    print(main_window.scene.select_mode.get_type())

def right_angle_radio_func(main_window):
    main_window.scene.select_mode.set_mode(4, 1)
    print(main_window.scene.select_mode.get_type())



'''
More radio definitions go here.
'''

def point_combo_func(value, main_window):
    main_window.scene.select_mode.set_mode(None, value)
    print(main_window.scene.select_mode.get_type())

def circle_combo_func(value, main_window):
    main_window.scene.select_mode.set_mode(None, value)
    print(main_window.scene.select_mode.get_type())
