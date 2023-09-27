from consts import Speed, Smart, Direction
import uuid
import math
import logging

LOGGER = logging.getLogger("Map")


DIR = "wasd"
DEFAULT_LIVES = 3
MIN_ENEMY_LIFE = DEFAULT_LIVES

def distance(p1, p2):
    LOGGER.warn("please use math.dist")
    return math.dist(p1, p2)


def vector2dir(vx, vy):
    m = max(abs(vx), abs(vy))
    if m == abs(vx):
        if vx < 0:
            d = 1  # a
        else:
            d = 3  # d
    else:
        if vy > 0:
            d = 2  # s
        else:
            d = 0  # w
    return d


class Character:
    def __init__(self, x=1, y=1):
        self._pos = x, y
        self._spawn_pos = self._pos
        self._direction: Direction = Direction.EAST

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if value[0] < self._pos[0]:
            self._direction = Direction.WEST
        elif value[0] > self._pos[0]:
            self._direction = Direction.EAST
        elif value[1] < self._pos[1]:
            self._direction = Direction.NORTH
        elif value[1] > self._pos[1]:
            self._direction = Direction.SOUTH
        self._pos = value

    @property
    def direction(self):
        return self._direction

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    def respawn(self):
        self.pos = self._spawn_pos


class DigDug(Character):
    def __init__(self, pos, lives=DEFAULT_LIVES):
        super().__init__(x=pos[0], y=pos[1])
        self._lives: int = lives

    def to_dict(self):
        return {"pos": self.pos, "lives": self._lives, "dir": self._direction.value}

    @property
    def lives(self):
        return self._lives

    def kill(self):
        self._lives -= 1


class Enemy(Character):
    def __init__(self, pos, name, points, speed, smart, wallpass):
        self._name = name
        self.id = uuid.uuid4()
        self._points = points
        self._speed = speed
        self._smart = smart
        self._wallpass = wallpass
        self.dir = list(Direction)
        self.step = 0
        self.lastdir = Direction.EAST
        self.lastpos = None
        self.wander = 0
        self._alive = MIN_ENEMY_LIFE  # TODO increase according to level
        super().__init__(*pos)

    def __str__(self):
        return f"{self._name}"

    def points(self):
        return self._points

    def kill(self):
        self._alive -= 1
        if self._alive < 0:
            self._alive = 0

    @property
    def alive(self):
        return self._alive > 0

    def move(self, mapa, digdug, enemies):
        if not self.ready():
            return

        if self._smart == Smart.LOW:
            new_pos = mapa.calc_pos(
                self.pos, self.dir[self.lastdir], self._wallpass
            )  # don't bump into stones/walls
            if new_pos == self.pos:
                self.lastdir = (self.lastdir + 1) % len(self.dir)

        elif self._smart == Smart.NORMAL:
            enemies_pos = [e.pos for e in enemies if e.id != self.id]
            open_pos = [
                pos
                for pos in [mapa.calc_pos(self.pos, d, self._wallpass) for d in DIR]
                if pos not in [self.lastpos] + enemies_pos
            ]
            if open_pos == []:
                new_pos = self.lastpos
            else:
                next_pos = sorted(
                    open_pos, key=lambda pos: distance(digdug.pos, pos), reverse=True
                )
                new_pos = next_pos[0]

        elif self._smart == Smart.HIGH:
            enemies_pos = [e.pos for e in enemies if e.id != self.id]
            open_pos = [
                pos
                for pos in [mapa.calc_pos(self.pos, d, self._wallpass) for d in DIR]
                if pos not in [self.lastpos] + enemies_pos
            ]
            if open_pos == []:
                new_pos = self.lastpos
            else:
                """
                if len(bombs):
                    next_pos = sorted(open_pos, key=lambda pos: distance(bombs[0].pos, pos), reverse=True)
                else:
                    next_pos = sorted(open_pos, key=lambda pos: distance(digdug.pos, pos), reverse=True)
                """
                new_pos = next_pos[0]

        self.lastpos = self.pos
        self.pos = new_pos

    def ready(self):
        self.step += int(self._speed)
        if self.step >= int(Speed.FAST):
            self.step = 0
            return True
        return False


class Pooka(Enemy):
    def __init__(self, pos):
        super().__init__(
            pos, self.__class__.__name__, 100, Speed.FAST, Smart.LOW, False
        )


class Fygar(Enemy):
    def __init__(self, pos):
        super().__init__(
            pos, self.__class__.__name__, 100, Speed.SLOW, Smart.LOW, False
        )
