import pygame as pg
import sys
from scripts.entities import PlayerEntity
from scripts.header import *
from scripts.utils import *
from scripts.tileMap import TileMap
import asyncio
from collections import deque


class Game:
    def __init__(self):        
        pg.init()
        pg.display.set_caption("UUUUU")
        
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # create the window
        self.container = pg.Surface((SCREEN_WIDTH/CONTAINER_DIVIDER, SCREEN_HEIGHT/CONTAINER_DIVIDER))
        
        self.assets = {
            #"decor": loadImages("tiles/decor", TILE_SIZE, TILE_SIZE),
            "grass": loadImages("tiles/grass", TILE_SIZE, TILE_SIZE),
            #"large_decor": loadImages("tiles/large_decor", TILE_SIZE, TILE_SIZE),
            "stone": loadImages("tiles/stone", TILE_SIZE, TILE_SIZE),
            "spikes": loadImages("tiles/spikes", TILE_SIZE, TILE_SIZE),
            "victory": loadImages("tiles/victory", TILE_SIZE, TILE_SIZE)
        }

        self.victoryAchieved = False
        self.frameCounter = 0
        self.finishTime = None
        self.bestTime = None
        
        self.horizontalMovement = {}
        self.verticalMovement = {}

        self.playerId = 0
        self.playerEntity = PlayerEntity(self, self.playerId, "player", (60/CONTAINER_DIVIDER, 480/CONTAINER_DIVIDER), (8, 15), imgPath='entities/player.png', convert=False, colorKey=False)

        self.tileMap = TileMap(self, 4)

        self.bufferQueue = deque(maxlen=10)
        self.coyoteTimeQueue = deque(maxlen=4)

        self.myFont = pg.font.SysFont(pg.font.get_default_font(), 50, bold=True)


    async def run(self):
        while True:
            self.frameCounter += 1

            self.container.fill((14, 140, 160))  # resets screen

            self.tileMap.render(self.container)

            if self.victoryAchieved:
                victoryText = self.myFont.render(f'{self.finishTime}s\nCongrats!', True, (0, 0, 0))
                self.container.blit(victoryText, (310 / CONTAINER_DIVIDER, 565 / CONTAINER_DIVIDER))

            if self.bestTime:
                bestTimeText = self.myFont.render(f'PB: {self.bestTime}s', True, (0, 0, 0))
                self.container.blit(bestTimeText, (50 / CONTAINER_DIVIDER, 865 / CONTAINER_DIVIDER))

            self.playerEntity.update(self.tileMap)
            self.playerEntity.render(self.container)

            speed = 4

            bufferedInput = None

            for event in pg.event.get():  # get user input
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:  # key pressed
                    if event.key == pg.K_LEFT:
                        self.horizontalMovement[self.playerId][0] = speed
                    elif event.key == pg.K_RIGHT:
                        self.horizontalMovement[self.playerId][1] = speed

                    if event.key == pg.K_UP:
                        bufferedInput = pg.K_UP
                    else:
                        bufferedInput = None

                if event.type == pg.KEYUP:  # key released
                    if event.key == pg.K_LEFT:
                        self.horizontalMovement[self.playerId][0] = 0
                    elif event.key == pg.K_RIGHT:
                        self.horizontalMovement[self.playerId][1] = 0

            self.bufferQueue.append(bufferedInput)
            self.coyoteTimeQueue.append(self.playerEntity.isGrounded)

            if pg.K_UP in self.bufferQueue and True in self.coyoteTimeQueue:
                self.playerEntity.flipGravity()
                self.bufferQueue.clear()
                self.coyoteTimeQueue.clear()

            self.screen.blit(pg.transform.scale(self.container, (SCREEN_WIDTH, SCREEN_HEIGHT)))
            pg.display.update()  # update the display with any changes
            await asyncio.sleep(0)



game = Game()
asyncio.run(game.run())
