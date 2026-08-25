import pygame
import sys
import os


IDLE_STATE = [0, 0]
MAGNITUDE_NORMALIZER = 1 / (2 ** 0.5)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game!")

        self.fontMain = pygame.font.SysFont("Consolas", 24, bold=True)

        self.screen = pygame.display.set_mode((640, 480))  # creates window
        self.clock = pygame.time.Clock()

        self.cloudImg = pygame.image.load(os.path.join("data", "images", "clouds", "cloud_1.png"))
        self.cloudImg.set_colorkey((0, 0, 0))  # enables transparency
        self.cloudImgPos = [160, 260]
        self.cloudMovementX = [0, 0]
        self.cloudMovementY = [0, 0]
        self.cloudSpeedMultiplier = 5

        self.collisionArea = pygame.Rect(300, 200, 200, 75)

    def run(self):
        while True:
            # UPDATE/CREATION
            imgCollisionRect = pygame.Rect(self.cloudImgPos[0], self.cloudImgPos[1], self.cloudImg.get_width(), self.cloudImg.get_height())

            # cloud position
            if (self.cloudMovementX != IDLE_STATE and self.cloudMovementY != IDLE_STATE):
                diagonalSpeedMultipler = MAGNITUDE_NORMALIZER
            else:
                diagonalSpeedMultipler = 1

            cloudVelocityX = (self.cloudMovementX[1] - self.cloudMovementX[0]) * self.cloudSpeedMultiplier * diagonalSpeedMultipler
            cloudVelocityY = (self.cloudMovementY[1] - self.cloudMovementY[0]) * self.cloudSpeedMultiplier * diagonalSpeedMultipler
            self.cloudImgPos[0] += cloudVelocityX
            self.cloudImgPos[1] += cloudVelocityY
            
            # text/other
            colliding = imgCollisionRect.colliderect(self.collisionArea)
            #textSurface = self.fontMain.render(f"X = {cloudVelocityX}\nY = {cloudVelocityY}", True, (0, 0, 0))
            textSurface = self.fontMain.render(f"Collision detected!" if (colliding) else "All quiet on the western front.", True, (0, 0, 0))

            # rendering
            self.screen.fill((14, 219, 248))
            
            if colliding:
                pygame.draw.rect(self.screen, (0, 100, 255), self.collisionArea)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collisionArea)

            self.screen.blit(self.cloudImg, self.cloudImgPos)
            self.screen.blit(textSurface, (50, 50))

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # clicking x on the window
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.cloudMovementY[0] = 1
                    if event.key == pygame.K_DOWN:
                        self.cloudMovementY[1] = 1
                    if event.key == pygame.K_LEFT:
                        self.cloudMovementX[0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.cloudMovementX[1] = 1
                if event.type == pygame.KEYUP:
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