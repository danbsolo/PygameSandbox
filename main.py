import pygame as pg
import sys


pg.init()
pg.display.set_caption("My Game!")
screen = pg.display.set_mode((640, 480))  # creates window

clock = pg.time.Clock()


while True:
    for event in pg.event.get():
       if event.type == pg.QUIT:  # clicking x on the window
           pg.quit()
           sys.exit()


    pg.display.update()  # update the display to changes made to the screen
    clock.tick(60)  # force run at 60 fps
