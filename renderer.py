import pygame
from helpers import *
from game_logic import Game


class Renderer:
    cell_size: int = 80

    groundImg = pygame.image.load("assets/ground.png")
    crateImg = pygame.image.load("assets/crate.png")
    playerImg = pygame.image.load("assets/player.png")
    wallImg = pygame.image.load("assets/wall.png")
    targetImg = pygame.image.load("assets/target.png")
    solvedImg = pygame.image.load("assets/solved_crate.png")

    def __init__(self, game: Game):
        pygame.init()
        current_state = game.current_state()
        self.screen_y = Renderer.cell_size * current_state.length
        self.screen_x = Renderer.cell_size * current_state.width
        self.display = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption("Sokoban Game")

    def update_game(self, game: Game):
        self.display.fill((50, 50, 50))
        current_state = game.current_state()

        for p in current_state.positions():
            py, px = Renderer.cell_size * p.x, Renderer.cell_size * p.y

            if p.access(current_state.tiles) == Tile.WALL:
                self.display.blit(Renderer.wallImg, (px, py))

            elif p.access(current_state.tiles) == Tile.EMPTY:
                self.display.blit(Renderer.groundImg, (px, py))
                if p.access(current_state.background) == BackgroundTile.GOAL:
                    self.display.blit(Renderer.targetImg, (px, py))

            elif p.access(current_state.tiles) == Tile.BOX:
                if p.access(current_state.background) == BackgroundTile.EMPTY:
                    self.display.blit(Renderer.crateImg, (px, py))
                if p.access(current_state.background) == BackgroundTile.GOAL:
                    self.display.blit(Renderer.solvedImg, (px, py))

            elif p.access(current_state.tiles) == Tile.PLAYER:
                self.display.blit(Renderer.playerImg, (px, py))

        pygame.display.update()

    def close(self):
        pygame.quit()
