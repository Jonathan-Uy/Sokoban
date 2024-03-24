import sys
import pygame
from typing import Optional
from helpers import *
from game_logic import *
from renderer import Renderer


def parse_level(level_str: str) -> Optional[State]:
    try:
        lines = level_str.splitlines()
        length, width = map(int, lines[0].split())
        tiles = map(lambda ln: list(map(parse_tile, ln)), lines[1 : length + 1])
        background_tiles = map(
            lambda ln: list(map(parse_background_tile, ln)),
            lines[length + 1 : (length * 2) + 1],
        )
        return State(list(tiles), list(background_tiles))
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    # Choose a level number from the command line
    args = sys.argv[1:]
    level_no = int(args[0]) if len(args) >= 1 else 0

    # Load an initial state of a level
    # First, read the string from a file
    try:
        with open(f"levels/{level_no}.txt") as f:
            level_str = f.read()
    except:
        print("The requested level doesn't exist!")
        print("Playing level 0 as default")
        with open("levels/0.txt") as f:
            level_str = f.read()

    # Then, parse the string into a State
    level = parse_level(level_str)
    if level is None:
        print("The level was incorrectly formatted")
        exit(1)
    game = Game(level)

    # Renderer
    renderer = Renderer(game)
    renderer.update_game(game)

    # Can be uncommented for debugging
    # print(game)

    # While the game is not over, read events
    while not game.win():
        for event in pygame.event.get():
            # If it is a directional key, process it
            # then update the screen
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        game.move(UP)
                    case pygame.K_s | pygame.K_DOWN:
                        game.move(DOWN)
                    case pygame.K_a | pygame.K_LEFT:
                        game.move(LEFT)
                    case pygame.K_d | pygame.K_RIGHT:
                        game.move(RIGHT)
                    case pygame.K_z | pygame.K_BACKSPACE:
                        game.undo()
                    case pygame.K_r | pygame.K_ESCAPE:
                        game.reset()
                renderer.update_game(game)

                # Can be uncommented for debugging
                # print(game)

            # Also need to read quits so user can exit
            # A quit is when user presses x on the game window
            elif event.type == pygame.QUIT:
                renderer.close()
                quit()

    print("You win! :D")
    renderer.close()
