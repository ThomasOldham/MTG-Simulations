import numpy as N
from PIL import Image

DEBUG = False

RED_VALUE = 0.0
YELLOW_VALUE = 0.5
GREEN_VALUE = 1.0
BLUE_VALUE = 2.0
PURPLE_VALUE = 3.0
BLACK_VALUE = 5.0

NO_DATA = (0xFF, 0xFF, 0xFF)
RED = (0xFF, 0x00, 0x00)
YELLOW = (0xFF, 0xFF, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
PURPLE = (0xFF, 0x00, 0xFF)
BLACK = (0x00, 0x00, 0x00)

SCALE = 100
AVG_SCALE = 10

def weighted_mixed_color(value, low, high, low_color, high_color):
    """ Given a value, low and high values that it falls in between,
        and colors representing each of the low and high values, generates
        a color between those colors representing where the value is
        between the low and high values.
    """
    low_weight = high - value
    high_weight = value - low
    scale = 1 / (low_weight + high_weight)
    low_weight *= scale
    high_weight *= scale
    color = [None] * 3
    for i in range(3):
        color[i] = int(low_color[i] * low_weight + high_color[i] * high_weight)
    return tuple(color)

def mulligan_perf_visual(results, expected, path, debug_value_color_pairs = None):
    """ Given the results of a performance-by-hand-size-and-mana simulation,
        generates an image representing the results, with the number of
        mulligans 0-7 on the y-axis and the number of lands 0-7 on the x-axis.
        Average results for each hand size are represented as a bar at the
        bottom of the row. There will also be a black bar at the top. This
        is a bug; please ignore it.
        Red represents the lowest performance value of 0, followed by yellow
        for 0.5x expected, green for 1x expected, blue for 2x expected, purple
        for 3x expected, and black for 5x expected or higher. Therefore,
        values higher than 5x expected cannot be properly represented and will
        all appear black.
        The generated picture can be used to determine when it is best to
        mulligan by comparing the color of the cell corresponding to a given
        hand to the bar above. If the bar above is a better color, than the
        expected performance of a hand mulliganed one more time is better
        than the expected performance of the current hand.
        Results should be in the form of a 2D numpy array with the first
        index representing hand size, the second index representing lands
        in opening hand, and the highest value of the land count index
        instead representing the average across all hands of that size,
        regardless of land count.
        Expected performance is arbitrary, and the results of each cell have
        little meaning outside of comparisons to other cells anyway. Mess with
        expected performance until you get a color spread you like.
        Path is the full file path where the image should be stored, except
        for the extension. The file will be stored as a .png.
        If DEBUG is turned on in the source code, debug_value_color_pairs
        can optionally be used to store all pairs of values from the input
        and generated colors in a list.
    """
    dimensions = tuple((N.array(N.shape(N.transpose(results))) - [1,0]) * SCALE)
    visual = Image.new("RGB",dimensions)
    for i in range(N.shape(results)[0]):
        for j in range(N.shape(results)[1]):
            color = None
            perf = results[i][j] / expected
            if results.mask[i][j]:
                color = NO_DATA
            elif perf < YELLOW_VALUE:
                color = weighted_mixed_color(perf, RED_VALUE, YELLOW_VALUE, RED, YELLOW)
            elif perf < GREEN_VALUE:
                color = weighted_mixed_color(perf, YELLOW_VALUE, GREEN_VALUE, YELLOW, GREEN)
            elif perf < BLUE_VALUE:
                color = weighted_mixed_color(perf, GREEN_VALUE, BLUE_VALUE, GREEN, BLUE)
            elif perf < PURPLE_VALUE:
                color = weighted_mixed_color(perf, BLUE_VALUE, PURPLE_VALUE, BLUE, PURPLE)
            elif perf < BLACK_VALUE:
                color = weighted_mixed_color(perf, PURPLE_VALUE, BLACK_VALUE, PURPLE, BLACK)
            else:
                color = BLACK
            if DEBUG and debug_value_color_pairs != None:
                debug_value_color_pairs.append([perf, color])
            h = i
            if j == N.shape(results)[1]-1:
                visual.paste(color, (0, h*SCALE + SCALE - AVG_SCALE, dimensions[1], (h+2)*SCALE))
            else:
                box = (j*SCALE, h*SCALE + AVG_SCALE, (j+1)*SCALE, (h+1)*SCALE)
                if DEBUG:
                    print(color, box)
                visual.paste(color, box)
            if DEBUG:
                print(debug_value_color_pairs)
    visual.save(path+".png", "PNG")