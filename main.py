import pygame
import sys
import os
from scripts.entities import PhysicsEntity
from scripts.utils import loadImage


IDLE_STATE = [0, 0]
MAGNITUDE_NORMALIZER = 1 / (2 ** 0.5)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game!")

        self.screen = pygame.display.set_mode((640, 480))  # creates window
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movementX = [0, 0]
        self.movementY = [0, 0]

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))
        self.playerSpeedMultiplier = 6
        self.assets = {
            "player": loadImage(os.path.join("entities", "player.png"))
        }

    def run(self):
        while True:
            diagonalSpeedMultipler = 1 if (self.movementX != IDLE_STATE and self.movementY != IDLE_STATE) else 1

            speedX = (self.movementX[1] - self.movementX[0]) * self.playerSpeedMultiplier * diagonalSpeedMultipler
            speedY = (self.movementY[1] - self.movementY[0]) * self.playerSpeedMultiplier * diagonalSpeedMultipler
            
            self.player.update((speedX, speedY))

            self.display.fill((14, 140, 160))
            self.player.render(self.display)

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movementY[0] = 1
                    if event.key == pygame.K_DOWN:
                        self.movementY[1] = 1
                    if event.key == pygame.K_LEFT:
                        self.movementX[0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.movementX[1] = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movementY[0] = 0
                    if event.key == pygame.K_DOWN:
                        self.movementY[1] = 0
                    if event.key == pygame.K_LEFT:
                        self.movementX[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movementX[1] = 0

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()) , (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()