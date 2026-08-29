import pygame as pg
from random import randint, uniform, choice
import time

SCREEN_WIDTH = 1080 #1366 #640 # 1920
SCREEN_HEIGHT = 1080 #768 #480

CONTAINER_DIVIDER = 2

NEIGHBOUR_OFFSETS = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (0, 0), (1, 0),
                    (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass", "stone", "spikes", "victory"}
DEATH_TILES = {"spikes"}
VICTORY_TILES = {"victory"}
TILEMAP_PATH = "data/maps/"

TILE_SIZE = 20