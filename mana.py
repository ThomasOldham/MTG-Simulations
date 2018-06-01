""" A set of functions for dealing with mana as arrays. Supports multiple
    colors, although the complexities of multi-color decks are not yet
    reflected anywhere in the project.
"""

MANA_TYPES = 7
NUMBER_BASE = 10

GENERIC = 0
COLORLESS = 1
WHITE = 2
BLUE = 3
BLACK = 4
RED = 5
GREEN = 6

SYMBOLS = [None, 'C', 'W', 'U', 'B', 'R', 'G']

def fromString(string):
    """ Creates an array of mana counts from a string in the common format
        of the number of generic mana followed by a letter indicating each
        individual non-generic mana. To check the symbol used for a mana
        type, use Mana.SYMBOLS[name of mana type in all caps].
    """
    ret = [0] * MANA_TYPES
    for char in string:
        if char in SYMBOLS:
            ret[SYMBOLS.index(char)] += 1
        elif char >= '0' or char <= '0'+NUMBER_BASE:
            ret[GENERIC] *= NUMBER_BASE
            ret[GENERIC] += int(char)
    return ret

def arrayFromString(array):
    ret = []
    for string in array:
        ret.append(fromString(string))
    return ret

def toString(pool):
    """ Converts a mana array back to a string in the common format of the
        number of generic mana followed by a letter indicating each
        individual non-generic mana.
    """
    ret = str(pool[GENERIC])
    for i in range(MANA_TYPES):
        if i != GENERIC:
            for j in range(pool[i]):
                ret += SYMBOLS[i]
    if len(ret) > 1 and pool[GENERIC] == 0:
        ret = ret[1:]
    return ret

def converted(pool):
    """ Gets the total amount of mana in a mana array.
    """
    return sum(pool)

def contains(pool, cost):
    """ Checks whether the first mana array contains enough mana of all types
        necessary to pay for the second mana array as a cost.
    """
    for i in range(MANA_TYPES):
        if (i != GENERIC and pool[i] < cost[i]):
            return False
    return converted(pool) >= converted(cost)

def plus(p1, p2):
    """ Adds two mana pools and returns the result. """
    ret = [0] * MANA_TYPES
    for i in range(MANA_TYPES):
        ret[i] = p1[i] + p2[i]

def minus(p1, p2):
    """ Subtracts the second mana pool from the first and returns the result. """
    ret = [0] * MANA_TYPES
    for i in range(MANA_TYPES):
        ret[i] = max(p1[i] - p2[i], 0)