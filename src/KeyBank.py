from PyQt5 import QtCore, QtGui
from sys import platform

class KeyState:
    UP = 0
    DOWN = 1

class Key:
    def __init__(self, key, state):
        self.key = key
        self.state = state

class KeyBank:
    def __init__(self):
        if platform.startswith('win'):
            self.move_point = Key(QtCore.Qt.Key.Key_Alt, KeyState.UP)
        else:
            self.move_point = Key(QtCore.Qt.Key.Key_AltGr, KeyState.UP)
        self.move_canvas = Key(QtCore.Qt.Key.Key_Control, KeyState.UP)

    def set_move_point_down(self):
        self.move_point.state = KeyState.DOWN

    def set_move_point_up(self):
        self.move_point.state = KeyState.UP

    def set_move_canvas_down(self):
        self.move_canvas.state = KeyState.DOWN

    def set_move_canvas_up(self):
        self.move_canvas.state = KeyState.UP
