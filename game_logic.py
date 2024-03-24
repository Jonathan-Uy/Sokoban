from copy import deepcopy
from helpers import *
from typing import List, Iterable

UP = Vector2(-1, 0)
DOWN = Vector2(1, 0)
LEFT = Vector2(0, -1)
RIGHT = Vector2(0, 1)

CAN_MULTIPUSH = False


class State:
    length: int
    width: int
    tiles: List[List[Tile]]
    background: List[List[BackgroundTile]]

    def __init__(self, tiles: List[List[Tile]], background: List[List[BackgroundTile]]):
        self.tiles = tiles
        self.background = background
        self.length = len(tiles)
        self.width = len(tiles[0])

    def move_player(self, player_pos: Vector2, direction: Vector2) -> bool:
        target = player_pos + direction
        if not self.is_inbounds(target):
            return False
        if target.access(self.tiles) == Tile.WALL:
            return False
        if target.access(self.tiles) == Tile.BOX:
            if not self.move_box(target, direction):
                return False
        player_pos.set(self.tiles, Tile.EMPTY)
        target.set(self.tiles, Tile.PLAYER)
        return True

    def move_box(self, box_pos: Vector2, direction: Vector2) -> bool:
        target = box_pos + direction
        if not self.is_inbounds(target):
            return False
        if target.access(self.tiles) == Tile.WALL:
            return False
        if target.access(self.tiles) == Tile.BOX:
            if not CAN_MULTIPUSH or not self.move_box(target, direction):
                return False
        box_pos.set(self.tiles, Tile.EMPTY)
        target.set(self.tiles, Tile.BOX)
        return True

    def win(self) -> bool:
        for p in self.positions():
            if (
                p.access(self.tiles) == Tile.BOX
                and p.access(self.background) != BackgroundTile.GOAL
            ):
                return False
        return True

    def is_inbounds(self, p: Vector2) -> bool:
        return 0 <= p.x < self.length and 0 <= p.y < self.width

    def positions(self) -> Iterable[Vector2]:
        for i in range(self.length):
            for j in range(self.width):
                yield Vector2(i, j)

    @staticmethod
    def print_tile(tile: Tile, background_tile: BackgroundTile) -> str:
        if tile == Tile.EMPTY:
            return background_tile.name()
        return tile.name()

    def __str__(self) -> str:
        return "\n".join(
            map(
                lambda row: "".join(map(lambda xs: State.print_tile(*xs), row)),
                zip2(self.tiles, self.background),
            )
        )


class Game:
    states: List[State]
    initial_state: State

    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.states = [initial_state]

    def current_state(self) -> State:
        return self.states[-1]

    def move(self, direction: Vector2) -> bool:
        state_copy = deepcopy(self.current_state())
        for p in state_copy.positions():
            if p.access(state_copy.tiles) == Tile.PLAYER:
                if state_copy.move_player(p, direction):
                    self.states.append(state_copy)
                    return True
        return False

    def reset(self) -> None:
        self.states.append(deepcopy(self.initial_state))

    def undo(self) -> bool:
        if len(self.states) > 1:
            self.states.pop()
            return True
        return False

    def win(self) -> bool:
        return self.current_state().win()

    def __str__(self) -> str:
        return str(self.current_state())
