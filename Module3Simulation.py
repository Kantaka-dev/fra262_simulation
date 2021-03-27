# Module3 (FRA262) Simulation

import math
def RtoD(radian): return radian*180/math.pi
def DtoR(degree): return degree/180*math.pi

import pygame as pg
pg.init()
pg.display.set_caption('Module3 Group10 Simulation')
pg.display.set_icon(pg.image.load('data/fibo_icon.jpg'))

CLOCK = pg.time.Clock()
FPS = 30 # frames/second

# Image
IMAGE = {
    'BACKGROUND'    : pg.image.load('data/simulation_background.png'),
    'BACKGROUND_L'  : pg.image.load('data/simulation_background_halfLeft.png')
}
# Color
COLOR = {
    'WHITE'     : (255, 255, 255),
    'ORANGE'    : (255, 167, 76),
    'RED'       : (255, 108, 70),
    'BLUE'      : (70,  205, 255),
    'YELLOW'    : (255, 208, 54),
    'YELLOW1'   : (223, 182, 49),
    'BLACK'     : (32,  34,  41)
}
# Font
# for font in pg.font.get_fonts():
#     print(font)
def FONT(size): return pg.font.SysFont('couriernew', size, bold=True)

winx, winy = 1024, 768
screen = pg.display.set_mode((winx, winy))

class InputBox:
    def __init__(self, x, y, w=200, h=50, length=6):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = ''
        self.value_len = length
        self.able = True

    def draw(self, mode=1):
        # Mode:0
        if mode == 0:
            pg.draw.rect(screen, COLOR['BLACK'], (self.x, self.y, self.w, self.h))
            screen.blit(FONT(28).render(self.value, True, COLOR['WHITE']), (
                self.x+100- int(50*len(self.value)/self.value_len), self.y+10)
            )
            return
        # Box
        elif self.able:
            pg.draw.rect(screen, (195,195,195), (self.x, self.y, self.w, self.h))
        elif self.isMouseOn():
            pg.draw.rect(screen, (220,220,220), (self.x, self.y, self.w, self.h))
        else:
            pg.draw.rect(screen, (255,255,255), (self.x, self.y, self.w, self.h))
        # Font
        screen.blit(FONT(28).render(self.value, True, COLOR['BLACK']), (
            self.x+100- int(50*len(self.value)/self.value_len), self.y+10)
        )

    def handleEvent(self, event):
        # Click
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isMouseOn():
                self.able = True
            else:
                self.able = False
        # Write
        if event.type == pg.KEYDOWN and self.able:
            if event.unicode in '.0123456789' and len(self.value) < self.value_len:
                self.value += str(event.unicode)
            elif event.key == pg.K_BACKSPACE:
                self.value = self.value[:-1]
    
    def getValue(self):
        return float(self.value)
    
    def check(self):
        return True if 0 < float(self.value) < 360 and self.value.count('.') <= 1 else False

    def isMouseOn(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return True if self.x < mouse_x < self.x+self.w and self.y < mouse_y < self.y+self.h else False

class Simulation:
    def __init__(self, input_box, max_rpm=10, max_acc=0.5):
        self.input_box = input_box
        # Plotting variable
        self.alpha = max_acc    # rad/s^2
        self.omega = 0.0        # rad/s
        self.theta = [0.0, 0.0] # [current,initial] deg ***
        self.theta_plot = []
        # Requirement
        self.omega_limit = max_rpm /30 *math.pi # rad/s
        self.alpha_limit = max_acc              # rad/s^2

    def init(self):
        # Simulation variable
        self.end_effector = [580.0, 384.0] # Initial position
        self.center = (330, 384)    # pixels
        self.radius = 250           # pixels
        self.total_distance = 0.0   # deg
        self.total_time = 0         # frames
        self.timer = 0              # frames
        self.link_length = [self.radius*math.cos(DtoR(self.theta[0])), self.radius*math.sin(DtoR(self.theta[0]))]
        screen.blit(IMAGE['BACKGROUND'], (0, 0))
# Run
    def run(self):
        print("\n====== Setting  ======")
        self.init()
        self.run = True

        while self.run:
            screen.blit(IMAGE['BACKGROUND_L'], (0, 0))
            screen.blit(FONT(22).render("Running process", True, COLOR['ORANGE']), (20, 20))

            self.input_box.draw(1)
            self.drawEndEffector()
            screen.blit(FONT(18).render("current position: {:6.2f} deg".format(self.theta[0]), True, COLOR['WHITE']), (20, 50))

            pg.display.update()
        # Event
            for event in pg.event.get():
                self.input_box.handleEvent(event)

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.input_box.check():
                    print("input distance: {} deg".format(self.input_box.getValue()))
                    self.total_distance += self.input_box.getValue()
                    self.input_box.able = False
                    
                    self.runSimulation()
                    self.run_simu = False
                    print("\n====== Setting  ======")
                    self.input_box.able = True
                
                if event.type == pg.QUIT or not self.run:
                    self.run = False
                    pg.quit()

            # CLOCK.tick(FPS)

    def init_simu(self):
        # set initial value
        self.alpha = self.alpha_limit   # rad/s^2
        self.omega = 0.0                # rad/s
        self.timer = 0                  # frame
        # circular rotational overflow
        self.theta[0] %= 360            # deg
        self.total_distance %= 360      # deg
        
        self.theta[1] = self.theta[0]
        self.theta_plot = []
        # calculate for total time ues and maximum velocity
        #  omega_max = sqrt(2*alpha*theta)
        self.omega_max = math.sqrt(self.alpha*DtoR(self.input_box.getValue()))
        #  time = sqrt(2*theta/alpha)
        self.total_time = FPS *math.sqrt(DtoR(self.input_box.getValue())/self.alpha)
        # set points of time for change acceleration
        self.critical_time = (int(self.total_time), int(self.total_time))
        self.total_time *= 2 # increase + decrease period

        # # Requirement
        if self.omega_max > self.omega_limit:
            # set maximum velocity limit
            self.omega_max = self.omega_limit
            # calculate critical points
            critical_pos = RtoD((self.omega_max**2)/self.alpha/2) # (this is 62.8 deg)
            stable_dis = self.input_box.getValue() - 2*critical_pos # deg
            middle_time = DtoR(stable_dis) / self.omega_max * FPS # frame
            # set new critical time
            self.critical_time = (int(self.omega_max/self.alpha*FPS), int(self.omega_max/self.alpha*FPS + middle_time))
            # set new total time
            self.total_time = int(2*self.omega_max/self.alpha*FPS + middle_time)

        screen.blit(IMAGE['BACKGROUND'], (0, 0))

    def runSimulation(self):
        self.init_simu()
        print("\n===== Simulation =====")
        print("initial position: {:.2f} deg".format(self.theta[1]))
        self.run_simu = True
        
        while self.run_simu:
            screen.blit(IMAGE['BACKGROUND_L'], (0, 0))
            screen.blit(FONT(22).render("Simulation process", True, COLOR['ORANGE']), (20, 20))

            self.input_box.draw(0)
            self.drive(1)
            self.drawEndEffector()
            screen.blit(FONT(18).render("current position: {:6.2f} deg".format(self.theta[0]), True, COLOR['WHITE']), (20, 50))
            if self.theta[0] > 360: 
                screen.blit(FONT(18).render("({:6.2f} deg)".format(self.theta[0]-360), True, COLOR['WHITE']), (350, 50))
            self.timer += 1
            # plotting graph
            self.plotTheta(1)
            self.plotOmega()
            self.plotAlpha()

            screen.blit(FONT(18).render("{:4} frames/ {:4.2f} second".format(self.timer, self.timer/FPS), True, COLOR['WHITE']), (20, 70))
            pg.display.update()
        # Event
            if self.timer >= self.total_time:
                print("final position  : {:.2f} deg".format(self.theta[0]))
                self.drive(-1)
                self.drawEndEffector()
                print("total time: {:.2f} s".format(self.total_time/FPS))
                self.run_simu = False

            for event in pg.event.get():
                if event.type == pg.QUIT or not self.run_simu:
                    self.run_simu = False
                    self.run = False
                    pg.quit()

            CLOCK.tick(FPS)

    def drive(self, mode=0):
        self.link_length = [self.radius*math.cos(DtoR(self.theta[0])), self.radius*math.sin(DtoR(self.theta[0]))]
        # Mode:1
        if mode == 1:
            # last phase
            if self.timer == max(self.critical_time):
                print("<max velocity idel:{:.3f} / real:{:.3f} / set:{:.3f}>".format(self.omega_max, self.omega, 2*self.omega_max - self.omega))
                self.omega = 2*self.omega_max - self.omega # for reduce sampling time error **
                self.alpha = -self.alpha_limit
            # middle phase
            elif self.timer == min(self.critical_time): # reach middle way for constant velocity
                self.omega = self.omega_max
                self.alpha = 0
            
            self.omega += self.alpha/FPS
            self.theta[0] += RtoD(self.omega)/FPS # deg/s * s/frame
            
            # End-effector currunt position
            self.end_effector = [self.center[0] + self.link_length[0], self.center[1] + self.link_length[1]]
        
        # Mode:-1
        elif mode == -1:
            # End-effector final position
            self.theta[0] = self.total_distance
            self.end_effector = [self.center[0] + self.link_length[0], self.center[1] + self.link_length[1]]
    
    def drawEndEffector(self, linkstyle=7):
        # draw link
        # (version1)
        # pg.draw.line(screen, COLOR['YELLOW'], self.center, (int(self.end_effector[0]), int(self.end_effector[1])), 30)
        # (version2)
        for i in range(1, linkstyle+1):
            pg.draw.circle(screen, COLOR['BLACK'], (
                int(self.end_effector[0] -(i/linkstyle)* self.link_length[0]),
                int(self.end_effector[1] -(i/linkstyle)* self.link_length[1])
            ), 20)
        # draw center
        pg.draw.circle(screen, COLOR['BLACK'], self.center, 37)
        # draw end-effector
        pg.draw.circle(screen, COLOR['ORANGE'], (int(self.end_effector[0]), int(self.end_effector[1])), 30)
    
    def plotTheta(self, mode=0, begin=(656,640), scale=(240,110)): # begin: origin(x,y), scale: (width,height)
        # (vertion2)
        pg.draw.circle(screen, COLOR['ORANGE'], (begin[0] + int(self.timer/self.total_time*scale[0]), 
        begin[1] - int((self.theta[0]-self.theta[1])/self.input_box.getValue()*scale[1])), 3)
        
        # (vertion1)
        # Mode:1
        # if mode == 1:
        #     self.theta_plot.append((0,0))
        #     self.theta_plot.append((int(self.timer/self.total_time * scale[0]), int((self.theta[0]-self.theta[1])/self.input_box.getValue() * scale[1])))
        # for xy in self.theta_plot:
        #     pg.draw.circle(screen, COLOR['ORANGE'], (xy[0]+begin[0], -xy[1]+begin[1]), 3)
    
    def plotOmega(self, mode=0, begin=(656,440), scale=(240,110)): # begin: origin(x,y), scale: (width,height)
        # (vertion2)
        pg.draw.circle(screen, COLOR['BLUE'], (begin[0] + int(self.timer/self.total_time*scale[0]), 
        begin[1] - int(self.omega/self.omega_max*scale[1])), 3)
        
        # (vertion1)
        # if self.timer < self.total_time//2:
        #     pg.draw.line(screen, COLOR['BLUE'], begin, 
        #     (begin[0]+int(self.timer/self.total_time*scale[0]), begin[1]-int(self.omega/self.omega_max*scale[1])), 6)

        # elif self.timer >= self.total_time//2:
        #     pg.draw.line(screen, COLOR['BLUE'], (begin[0]+scale[0]//2, begin[1]-scale[1]), 
        #     (begin[0]+int(self.timer/self.total_time*scale[0]), begin[1]-int(self.omega/self.omega_max*scale[1])), 6)
    
    def plotAlpha(self, mode=0, begin=(656,180), scale=(240,110)): # begin: origin(x,y), scale: (width,height)
        # (vertion2)
        pg.draw.circle(screen, COLOR['RED'], (begin[0] + int(self.timer/self.total_time*scale[0]), 
        begin[1] - int(self.alpha*scale[1])), 3)
        
        # (vertion1)
        # if self.timer < self.total_time//2:
        #     pg.draw.line(screen, COLOR['RED'], (begin[0], begin[1]-scale[1]//2), 
        #     (begin[0]+int(self.timer/self.total_time*scale[0]), begin[1]-scale[1]//2), 6)
        
        # elif self.timer >= self.total_time//2:
        #     # pg.draw.line(screen, COLOR['RED'], (begin[0], begin[1]-scale[1]//2), (begin[0]+scale[0]//2, begin[1]-scale[1]//2), 6)
        #     # pg.draw.line(screen, COLOR['RED'], (begin[0]+scale[0]//2, begin[1]-scale[1]//2), (begin[0]+scale[0]//2, begin[1]+scale[1]//2), 6)
        #     pg.draw.line(screen, COLOR['RED'], (begin[0]+scale[0]//2, begin[1]+scale[1]//2), 
        #     (begin[0]+int(self.timer/self.total_time*scale[0]), begin[1]+scale[1]//2), 6)

input_distance = InputBox(x=230, y=680)

Simulation = Simulation(input_distance, max_rpm=10)
Simulation.run()