from enum import IntEnum


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
