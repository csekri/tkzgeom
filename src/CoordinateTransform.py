from Constants import WIDTH, HEIGHT

def canvascoord2tkzcoord(x_canvas, y_canvas, lbs):
    """
    SUMMARY
        converts canvas pixel coordinates into TikZ coordinates

    PARAMETERS
        x_canvas: x coordinate on the canvas
        y_canvas: y coordinate on the canvas
        lbs: the parameters of the TikZ bounding box
            (lbs stands for tuple of (left,bottom,scale))

    RETURNS
        (str, str): x and y coordinate on the TikZ plane both converted to str
            (converted to string because it is used in the TikZ code straight)
    """
    left, bottom, scale = lbs
    # 10 had to be assigned here to have 10 by 10 unit wide and high TikZ canvas
    # in the beginning
    x_tkz = left + x_canvas/WIDTH * scale*10
    y_tkz = bottom + (HEIGHT-y_canvas) / HEIGHT * scale*10
    return str(x_tkz), str(y_tkz)


def tkzcoord2canvascoord(x_tkz, y_tkz, lbs):
    """
    SUMMARY
        converts TikZ coordinates into canvas pixel coordinates

    PARAMETERS
        x_tkz: x coordinate on the canvas
        y_tkz: y coordinate on the canvas
        lbs: the parameters of the TikZ bounding box
            (lbs stands for tuple of (left,bottom,scale))

    RETURNS
        (str, str): x and y coordinate on the canvas plane
    """
    left, bottom, scale = lbs
    x_canvas = (eval(x_tkz) - left) * WIDTH / (scale * 10)
    y_canvas = -(eval(y_tkz) - bottom) * HEIGHT / (scale * 10) + HEIGHT
    return [x_canvas, y_canvas]
