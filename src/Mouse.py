import Constant as c

class Mouse:
    def __init__(self):
        """Construct Mouse."""

        self.__left_button_state = c.MouseState.UP
        self.__right_button_state = c.MouseState.UP
        self.__x = 0
        self.__y = 0
        self.__pressed_at_x = 0
        self.__pressed_at_y = 0

    def get_x(self):
        """Return the x coordinate of the mouse pointer."""

        return self.__x

    def get_y(self):
        """return the y coordinate of the mouse pointer."""

        return self.__y

    def get_pressed_at_x(self):
        """Return the pressed x coordinate of the mouse.

        Returns the x coordinate of the position where the mouse
        was when the left button was pressed.
        """

        return self.__pressed_at_x

    def get_pressed_at_y(self):
        """Return the pressed y coordinate of the mouse.

        Returns the y coordinate of the position where the mouse
        was when the left button was pressed.
        """

        return self.__y

    def set_pressed_xy(self, x, y):
        """return the x and y coordinate of the mouse pointer."""

        return self.__pressed_at_x, self.__pressed_at_y

    def get_xy(self):
        """return the x and y coordinate of the mouse pointer."""

        return self.__x, self.__y

    def set_xy(self, x, y):
        """set the x and y coordinate of the mouse pointer."""

        self.__x, self.__y = x, y

    def get_left_button_state(self):
        """return the state of the left mouse button."""

        return self.__left_button_state

    def set_left_button_state(self, state):
        """set the state of the left mouse button."""

        self.__left_button_state = state

    def get_right_button_state(self):
        """return the state of the right mouse button."""

        return self.__right_button_state

    def set_right_button_state(self, state):
        """set the state of the right mouse button."""

        self.__right_button_state = state
