import pygame
import sys
import os

IDLE_STATE = [0, 0]
MAGNITUDE_NORMALIZER = 2 ** 0.5

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game!")

        self.fontMain = pygame.font.SysFont("Segoe UI", 24, bold=True)

        self.screen = pygame.display.set_mode((640, 480))  # creates window
        self.clock = pygame.time.Clock()

        self.cloudImg = pygame.image.load(os.path.join("data", "images", "clouds", "cloud_1.png"))
        self.cloudImgPos = [160, 260]
        self.cloudMovementX = [0, 0]
        self.cloudMovementY = [0, 0]
        self.cloudSpeedMultiplier = 5

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            if (self.cloudMovementX != IDLE_STATE and self.cloudMovementY != IDLE_STATE):
                diagonalSpeedMultipler = MAGNITUDE_NORMALIZER
            else:
                diagonalSpeedMultipler = 1

            cloudSpeedX = (self.cloudMovementX[1] - self.cloudMovementX[0]) * self.cloudSpeedMultiplier / diagonalSpeedMultipler
            cloudSpeedY = (self.cloudMovementY[1] - self.cloudMovementY[0]) * self.cloudSpeedMultiplier / diagonalSpeedMultipler
            self.cloudImgPos[0] += cloudSpeedX
            self.cloudImgPos[1] += cloudSpeedY
            
            self.screen.blit(self.cloudImg, self.cloudImgPos)

            text_surface = self.fontMain.render(f"X = {cloudSpeedX}\nY = {cloudSpeedY}", True, (0, 0, 0))
            self.screen.blit(text_surface, (50, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # clicking x on the window
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.cloudMovementY[0] = 1
                    if event.key == pygame.K_DOWN:
                        self.cloudMovementY[1] = 1
                    if event.key == pygame.K_LEFT:
                        self.cloudMovementX[0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.cloudMovementX[1] = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.cloudMovementY[0] = 0
                    if event.key == pygame.K_DOWN:
                        self.cloudMovementY[1] = 0
                    if event.key == pygame.K_LEFT:
                        self.cloudMovementX[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.cloudMovementX[1] = 0



            pygame.display.update()  # update the display to changes made to the screen
            self.clock.tick(60)  # force run at 60 fps


if __name__ == "__main__":
    Game().run()