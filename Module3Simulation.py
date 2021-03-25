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

# Color
COLOR = {
    'WHITE' : (255, 255, 255),
    'ORANGE': (255, 167, 76)
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

    def draw(self, mode=1):
        # Mode:0
        if mode == 0:
            pg.draw.rect(screen, (255,255,255), (self.x, self.y, self.w, self.h))
            screen.blit(FONT(20).render(self.value, True, (0,0,0)), (self.x+5, self.y+5))
            return
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
    
    def check(self):
        return True if 0 < float(self.value) < 360 and self.value.count('.') <= 1 else False

    def isMouseOn(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return True if self.x < mouse_x < self.x+self.w and self.y < mouse_y < self.y+self.h else False

class Simulation:
    def __init__(self, input_box):
        self.input_box = input_box
        # Plotting variable
        self.alpha = 0.0 # rad/s^2
        self.omega = 1.0 # rad/s
        self.theta = 0.0 # rad
        # Simulation variable
        self.end_effector = [580.0, 384.0] # Initial position
        self.center = (330, 384)    # pixels
        self.radius = 250           # pixels
        self.timer = 0              # frames
        self.total_distance = 0.0   # deg

    def init(self):
        screen.blit(IMAGE['BACKGROUND'], (0, 0))
# Run
    def run(self):
        print("\n===== Setting =====")
        self.init()
        self.run = True

        while self.run:
            screen.blit(IMAGE['BACKGROUND'], (0, 0))
            screen.blit(FONT(20).render("Running process", True, COLOR['ORANGE']), (20, 20))

            self.input_box.draw(1)
            self.drawEndEffector(0)

            pg.display.update()
        # Event
            for event in pg.event.get():
                self.input_box.handleEvent(event)

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.input_box.check():
                    print("input distance: {} deg.".format(self.input_box.value))
                    self.total_distance += float(self.input_box.value)
                    self.input_box.able = False
                    
                    self.runSimulation()
                    self.run_simu = False
                    print("\n====== Setting  ======")
                
                if event.type == pg.QUIT or not self.run:
                    self.run = False
                    pg.quit()

            CLOCK.tick(FPS)

    def runSimulation(self):
        print("\n===== Simulation =====")
        self.run_simu = True
        
        while self.run_simu:
            screen.blit(IMAGE['BACKGROUND'], (0, 0))
            screen.blit(FONT(20).render("Simulation process", True, COLOR['ORANGE']), (20, 20))

            self.input_box.draw(0)
            self.drawEndEffector(1)
            screen.blit(FONT(20).render("{:.2f} deg".format(self.theta*180.0/math.pi), True, COLOR['WHITE']), (20, 50))

            pg.display.update()
        # Event
            # For testing
            if self.theta >= self.total_distance/180.0*math.pi:
                self.run_simu = False

            for event in pg.event.get():

                if event.type == pg.QUIT or not self.run_simu:
                    self.run_simu = False
                    self.run = False
                    pg.quit()

            CLOCK.tick(FPS)

    def drawEndEffector(self, mode=0):
        # Mode:1
        if mode == 1:
            self.theta += self.omega/FPS # rad/s * s/frame

            self.end_effector = [self.center[0]+self.radius*math.cos(self.theta), self.center[1]+self.radius*math.sin(self.theta)]
        
        pg.draw.circle(screen, COLOR['ORANGE'], (int(self.end_effector[0]), int(self.end_effector[1])), 30)

input_distance = InputBox(230, 680)

Simulation = Simulation(input_distance)
Simulation.run()
