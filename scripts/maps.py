import pygame


NEIGHBOUR_OFFSETS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
PHYSICS_TILES = {'grass', 'stone'}


class Tilemap:
    def __init__(self, game, tileSize=16):
        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offgridTiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'position': (3+i, 10)}
            self.tilemap['10;' + str(5+i)] = {'type': 'stone', 'variant': 1, 'position': (10, 5+i)}

    def getSurroundingTiles(self, position):
        surroundingTiles = []
        tileLocation = (int(position[0] // self.tileSize), int(position[1] // self.tileSize))  # convert pixel position into tile position

        for offset in NEIGHBOUR_OFFSETS:
            checkLocation = f"{tileLocation[0] + offset[0]};{tileLocation[1] + offset[1]}"

            if checkLocation in self.tilemap:
                surroundingTiles.append(self.tilemap[checkLocation])

        return surroundingTiles

    def getSurroundingCollisionBoxes(self, position):
        collisionBoxes = []
        for tile in self.getSurroundingTiles(position):
            if tile['type'] in PHYSICS_TILES:
                collisionBoxes.append(pygame.Rect(tile['position'][0]*self.tileSize,tile['position'][1]*self.tileSize, self.tileSize, self.tileSize))
        return collisionBoxes

    def render(self, surface, offset=(0, 0)):
        for tile in self.offgridTiles:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['position'][0] - offset[0], tile['position'][1] - offset[1]))

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['position'][0] * self.tileSize - offset[0], tile['position'][1] * self.tileSize - offset[1]))
            # ^ * self.tileSize in order to convert tile position into pixel position
