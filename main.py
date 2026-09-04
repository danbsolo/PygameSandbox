import pygame
import sys
import os
from scripts.entities import PhysicsEntity
from scripts.utils import loadImage, loadImages
from scripts.maps import Tilemap
from scripts.defs import *
from collections import deque


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game!")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # creates window
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        self.clock = pygame.time.Clock()

        self.movementX = [0, 0]
        self.movementY = [0, 0]

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))
        self.playerSpeedMultiplier = 6
        self.assets = {
            "player": loadImage(os.path.join("entities", "player.png")),
            #"randomVerticalImage": loadImage(os.path.join("other", "randomVerticalImage.jpg")),
            "darkVerticalImage": pygame.transform.scale(loadImage(os.path.join("other", "darkVerticalImage.jpg")), (BORDER_WIDTH, SCREEN_HEIGHT)),
            "lightVerticalImage": pygame.transform.flip(pygame.transform.scale(loadImage(os.path.join("other", "lightVerticalImage.jpg")), (BORDER_WIDTH, SCREEN_HEIGHT)), True, False),
            "decor": loadImages(os.path.join("tiles", "decor")),
            "grass": loadImages(os.path.join("tiles", "grass")),
            "large_decor": loadImages(os.path.join("tiles", "large_decor")),
            "stone": loadImages(os.path.join("tiles", "stone"))
        }

        self.tilemap = Tilemap(self, 16)

        self.bufferInputQueue = deque(maxlen=10)
        self.coyoteTimeQueue = deque(maxlen=10)

        self.scroll = [0, 0]


    def run(self):
        floatHeld = False

        while True:
            self.scroll[0] += 0.5

            diagonalSpeedMultipler = 1 if (self.movementX != IDLE_STATE and self.movementY != IDLE_STATE) else 1
            speedX = (self.movementX[1] - self.movementX[0]) * self.playerSpeedMultiplier * diagonalSpeedMultipler
            speedY = (self.movementY[1] - self.movementY[0]) * self.playerSpeedMultiplier * diagonalSpeedMultipler
            self.player.update(self.tilemap, (speedX, speedY))

            self.display.fill((14, 140, 160))
            self.tilemap.render(self.display, offset=self.scroll)
            self.player.render(self.display, offset=self.scroll)

            self.screen.blit(self.assets["darkVerticalImage"], (0, 0))
            self.screen.blit(self.assets["lightVerticalImage"], (SCREEN_WIDTH - BORDER_WIDTH, 0))

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    # movement (not included in buffer)
                    if event.key == pygame.K_LEFT:
                        self.movementX[0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.movementX[1] = 1


                    # other buttons (included in buffer)
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.bufferInputQueue.append(event.key)
                    elif event.key == pygame.K_x:
                        floatHeld = True
                    else:
                        self.bufferInputQueue.append(None)
                else:
                    self.bufferInputQueue.append(None)
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movementX[0] = 0
                    elif event.key == pygame.K_RIGHT:
                        self.movementX[1] = 0
                    elif event.key == pygame.K_x:
                        floatHeld = False 
            else:
                self.bufferInputQueue.append(None)

            self.coyoteTimeQueue.append(self.player.isGrounded)

            if pygame.K_UP in self.bufferInputQueue and True in self.coyoteTimeQueue:
                self.player.velocity[1] = -4
                self.bufferInputQueue.clear()
                self.coyoteTimeQueue.clear()
            elif pygame.K_DOWN in self.bufferInputQueue and not self.player.isGrounded:
                self.player.velocity[1] = 5
                self.bufferInputQueue.clear()

            if floatHeld and not self.player.isGrounded:
                self.player.velocity[1] = 0.5

            self.screen.blit(pygame.transform.scale(self.display, (DISPLAY_SCALED_WIDTH, DISPLAY_SCALED_HEIGHT)), (BORDER_WIDTH, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
