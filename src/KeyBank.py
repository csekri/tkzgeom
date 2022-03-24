from PyQt5 import QtCore
from sys import platform


class KeyState:
    UP = 0
    DOWN = 1


class Key:
    def __init__(self, key, state):
        """Construct Key."""
        self.key = key
        self.state = state


class KeyBank:
    def __init__(self):
        """Construct KeyBank."""
        if platform.startswith('win'):  # Windows system is detected
            self.move_point = Key(QtCore.Qt.Key.Key_Alt, KeyState.UP)
        else:  # anything other than Windows
            self.move_point = Key(QtCore.Qt.Key.Key_AltGr, KeyState.UP)
        self.move_canvas = Key(QtCore.Qt.Key.Key_Control, KeyState.UP)

    def set_move_point_down(self):
        """Set move point key down."""
        self.move_point.state = KeyState.DOWN

    def set_move_point_up(self):
        """Set move point key up."""
        self.move_point.state = KeyState.UP

    def set_move_canvas_down(self):
        """Set move canvas key down."""
        self.move_canvas.state = KeyState.DOWN

    def set_move_canvas_up(self):
        """Set move canvas key up."""
        self.move_canvas.state = KeyState.UP
