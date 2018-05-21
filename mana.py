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
    ret = str(pool[GENERIC])
    for i in range(MANA_TYPES):
        if i != GENERIC:
            for j in range(pool[i]):
                ret += SYMBOLS[i]
    if len(ret) > 1 and pool[GENERIC] == 0:
        ret = ret[1:]
    return ret

def converted(pool):
    return sum(pool)

def contains(pool, cost):
    for i in range(MANA_TYPES):
        if (i != GENERIC and pool[i] < cost[i]):
            return False
    return converted(pool) >= converted(cost)

def plus(p1, p2):
    ret = [0] * MANA_TYPES
    for i in range(MANA_TYPES):
        ret[i] = p1[i] + p2[i]

def minus(p1, p2):
    ret = [0] * MANA_TYPES
    for i in range(MANA_TYPES):
        ret[i] = max(p1[i] - p2[i], 0)
