# Module3 (FRA262) Simulation

import pygame as pg
import math

pg.init()
pg.display.set_caption('Module3 Group10 Simulation')
pg.display.set_icon(pg.image.load('data/fibo_icon.jpg'))

CLOCK = pg.time.Clock()
FPS = 60 # 60 frames/second

# Image
IMAGE = {
    'BACKGROUND': pg.image.load('data/simulation_background.png')
}

# Font
def FONT(size):
    return pg.font.SysFont('ocraextended', size)

winx, winy = 1024, 768
screen = pg.display.set_mode((winx, winy))

class InputBox:
    def __init__(self, x, y, w=200, h=50):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = ''
        self.able = False

    def draw(self):
        # Box
        if self.able:
            pg.draw.rect(screen, (195,195,195), (self.x, self.y, self.w, self.h))
        elif self.isMouseOn():
            pg.draw.rect(screen, (220,220,220), (self.x, self.y, self.w, self.h))
        else:
            pg.draw.rect(screen, (255,255,255), (self.x, self.y, self.w, self.h))
        # Font
        screen.blit(FONT(20).render(self.value, True, (0,0,0)), (self.x+5, self.y+5))

    def handleEvent(self, event):
        # Click
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isMouseOn():
                self.able = True
            else:
                self.able = False
        # Write
        if event.type == pg.KEYDOWN and self.able:
            if event.unicode in '.0123456789' and len(self.value) <= 5:
                self.value += str(event.unicode)
            elif event.key == pg.K_BACKSPACE:
                self.value = self.value[:-1]

    def isMouseOn(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return True if self.x < mouse_x < self.x+self.w and self.y < mouse_y < self.y+self.h else False

class Simulation:
    def __init__(self, input_box):
        self.input_box = input_box
        self.timer = 0
        self.total_distance = 0

    def init(self):
        screen.blit(IMAGE['BACKGROUND'], (0, 0))
# Run
    def run(self):
        self.init()
        self.run = True

        while self.run:
            screen.blit(IMAGE['BACKGROUND'], (0, 0))

            self.input_box.draw()

            pg.display.update()
        # Event
            for event in pg.event.get():
                self.input_box.handleEvent(event)
                
                if event.type == pg.QUIT or not self.run:
                    self.run = False
                    pg.quit()

            CLOCK.tick(FPS)

    def waitForInput(self):
        self.total_distance = input("Input the distance : ")

input_distance = InputBox(230, 680)

Simulation = Simulation(input_distance)
Simulation.run()
