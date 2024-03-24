from enum import Enum


class Tile(Enum):
    EMPTY = 0
    PLAYER = 1
    WALL = 2
    BOX = 3

    def name(self) -> str:
        match self:
            case Tile.EMPTY:
                return "."
            case Tile.PLAYER:
                return "p"
            case Tile.WALL:
                return "#"
            case Tile.BOX:
                return "x"
            case _:
                raise Exception("Invalid tile")


def parse_tile(c):
    match c:
        case ".":
            return Tile.EMPTY
        case "p":
            return Tile.PLAYER
        case "#":
            return Tile.WALL
        case "x":
            return Tile.BOX
        case _:
            raise Exception("Invalid tile character: " + c)


class BackgroundTile(Enum):
    EMPTY = 0
    GOAL = 1

    def name(self) -> str:
        match self:
            case BackgroundTile.EMPTY:
                return "."
            case BackgroundTile.GOAL:
                return "o"
            case _:
                raise Exception("Invalid background tile")


def parse_background_tile(c):
    match c:
        case ".":
            return BackgroundTile.EMPTY
        case "o":
            return BackgroundTile.GOAL
        case _:
            raise Exception("Invalid background tile character: " + c)


class Vector2:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def access(self, arr):
        return arr[self.x][self.y]

    def set(self, arr, val):
        arr[self.x][self.y] = val

    def __add__(self, other):
        assert type(other) == Vector2, "Tried to add a Vector2 to another type"
        return Vector2(self.x + other.x, self.y + other.y)


def zip2(xs, ys):
    return map(zip, xs, ys)
