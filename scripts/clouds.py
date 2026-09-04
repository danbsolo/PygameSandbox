from scripts.defs import *
import random

class Cloud:
    def __init__(self, position, image, speed, depth):
        self.position = list(position)
        self.image = image
        self.speed = speed
        self.depth = depth

    def update(self):
        self.position[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        renderPosition = (self.position[0] - offset[0] * self.depth, self.position[1] - offset[1] * self.depth)
        surface.blit(self.image, (renderPosition[0] % (DISPLAY_WIDTH + self.image.get_width()) - self.image.get_width(),
                                  renderPosition[1] % (DISPLAY_HEIGHT + self.image.get_height()) - self.image.get_height()))

class Clouds:
    def __init__(self, cloudImages, count=16):
        self.clouds = []

        for _ in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999),
                                     random.choice(cloudImages),
                                     random.uniform(0.01, 2),   #random.random() * 0.05 + 0.05,
                                     random.uniform(0.1, 0.8)   #random.random() * 0.6 + 0.2
                               ))

        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset)
