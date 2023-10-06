from enum import IntEnum

GROUND_POINTS, MIDDLE_POINTS, BOTTOM_POINTS, BED_POINTS = 200, 300, 400, 500
ROCK_KILL_POINTS = 1000
ENEMY_HEAL = 9


class Speed(IntEnum):
    SLOWEST = (1,)
    SLOW = (2,)
    NORMAL = (3,)
    FAST = 4


class Smart(IntEnum):
    LOW = (1,)
    NORMAL = (2,)
    HIGH = 3


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
