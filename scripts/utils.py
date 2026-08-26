import pygame
import os

BASE_IMG_PATH = os.path.join("data", "images")

def loadImage(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert()
    
    img.set_colorkey((0, 0, 0))
    
    return img