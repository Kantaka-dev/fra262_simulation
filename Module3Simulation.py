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
    'BACKGROUND_L'  : pg.image.load('data/simulation_background_halfLeft.png'),
    'TARGET'        : (
        pg.image.load('data/target0.PNG'), # size 62*62 / offset x:9 y:9
        pg.image.load('data/target1.PNG'),
        pg.image.load('data/target2.PNG'),
        pg.image.load('data/target3.PNG')
    )
}
# Color
COLOR = {
    'WHITE'     : (255, 255, 255),
    'GRAY'      : (220, 220, 220),
    'GRAY2'     : (195, 195, 195),
    'GRAY3'     : (115, 115, 115),
    'ORANGE'    : (255, 167,  76),
    'RED'       : (255, 108,  70),
    'BLUE'      : ( 70, 205, 255),
    'YELLOW'    : (255, 208,  54),
    'YELLOW1'   : (223, 182,  49),
    'GRAY9'     : ( 37,  39,  47),
    'BLACK'     : ( 32,  34,  41), 
    'BACKGROUND': ( 45,  49,  60)
}
# Font
# for font in pg.font.get_fonts():
#     print(font)
def FONT(size): return pg.font.SysFont('couriernew', size, bold=True)

winx, winy = 1024, 768
screen = pg.display.set_mode((winx, winy))

class InputBox:
    def __init__(self, name, x, y, next_box=None, scale=120, length=6, default=False):
        self.name = name # name must be 'Station [num]' only
        self.x = x
        self.y = y
        self.w = scale
        self.h = scale//4
        self.value = ''
        self.value_len = length
        self.able = default
        self.next = next_box

    def draw(self, mode=1):
        # draw name
        screen.blit(FONT(18).render(self.name, True, COLOR['BLACK'],), (self.x+10, self.y-22))
        # Mode:0
        if mode == 0:
            pg.draw.rect(screen, COLOR['BLACK'], (self.x, self.y, self.w, self.h), border_radius=self.h//4)
        # while typing
        elif self.able:
            pg.draw.rect(screen, COLOR['WHITE'], (self.x, self.y, self.w, self.h), border_radius=self.h//4)
            screen.blit(FONT(int(self.w*0.16)).render(self.value, True, COLOR['BLACK']), (
                self.x+(self.w//2)- int(self.w/4*len(self.value)/self.value_len), self.y+(self.h//6))
            )
            # draw curser
            if pg.time.get_ticks()%1000 < 500:
                if len(self.value)>0:
                    pg.draw.line(screen, COLOR['BLACK'], (
                        self.x+(self.w//2)+ int(self.w/3.5*len(self.value)/self.value_len) +5, self.y+(self.h//2)
                    ), (
                        self.x+(self.w//2)+ int(self.w/3.5*len(self.value)/self.value_len) +10, self.y+(self.h//2)
                    ), self.h//2)
                else:
                    pg.draw.line(screen, COLOR['BLACK'], (
                        self.x+(self.w//2)-2, self.y+(self.h//2)), (self.x+(self.w//2)+3, self.y+(self.h//2)
                    ), self.h//2)
            return
        
        elif self.isMouseOn():
            pg.draw.rect(screen, COLOR['GRAY9'], (self.x, self.y, self.w, self.h), border_radius=self.h//4)
        else:
            pg.draw.rect(screen, COLOR['BLACK'], (self.x, self.y, self.w, self.h), border_radius=self.h//4)
        
        screen.blit(FONT(int(self.w*0.16)).render(self.value, True, COLOR['WHITE']), (
            self.x+(self.w//2)- int(self.w/4*len(self.value)/self.value_len), self.y+(self.h//6))
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
            # insert value
            if event.unicode in '.0123456789' and len(self.value) < self.value_len:
                self.value += str(event.unicode)
            # delete last valse
            elif event.key == pg.K_BACKSPACE:
                self.value = self.value[:-1]
            # go to next box
            elif event.key == pg.K_TAB and self.next != None:
                self.able = False
                self.next.able = True
    
    def getValue(self):
        return float(self.value)
    
    def check(self):
        return True if len(self.value)>0 and self.value.count('.')<= 1 and 0<float(self.value) and (self.value[0].isnumeric() or self.value[-1].isnumeric()) else False
        # and 0<float(self.value)<=360

    def isMouseOn(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return True if self.x < mouse_x < self.x+self.w and self.y < mouse_y < self.y+self.h else False

    def reset(self):
        self.value = ''
        self.able = False

    def warp(self):
        self.value = str(float(self.value) + 360)

class Simulation:
    def __init__(self, input_boxes, max_rpm=10, max_acc=0.5):
        self.input_boxes = input_boxes
        self.input_box = 0
        # Plotting variable
        self.alpha = max_acc    # rad/s^2
        self.omega = 0.0        # rad/s
        self.theta = [0.0, 0.0] # [current,initial] deg ***
        # Requirement
        self.omega_limit = max_rpm /30 *math.pi # rad/s
        self.alpha_limit = max_acc              # rad/s^2
        self.global_time = 0                    # s

    def init(self):
        # Simulation variable
        self.end_effector = [580.0, 384.0] # Initial position
        self.center = (330, 384)    # pixels
        self.radius = 250           # pixels
        self.total_distance = 0.0   # deg
        self.total_time = 0         # frames
        self.timer = 0              # frames
        self.global_time = 0        # s
        self.link_length = [self.radius*math.cos(DtoR(self.theta[0])), self.radius*math.sin(DtoR(self.theta[0]))]
        screen.blit(IMAGE['BACKGROUND'], (0, 0))
    
    def run(self):
        # print("\n====== Setting  ======")
        self.init()
        self.run = True

        while self.run:
            screen.blit(IMAGE['BACKGROUND_L'], (0, 0))
            screen.blit(FONT(22).render("Input process", True, COLOR['ORANGE']), (20, 20))

            for each_input_box in self.input_boxes:
                each_input_box.draw(1)
            self.drawTarget()
            self.drawEndEffector()
            self.drawTime()

            pg.display.update()
        # Event
            for event in pg.event.get():
                for each_input_box in self.input_boxes[::-1]:
                    each_input_box.handleEvent(event)

                if event.type == pg.KEYDOWN:
                    # Run Simulation
                    if event.key == pg.K_RETURN and self.check():
                        for each_input_box in self.input_boxes:
                            each_input_box.able = False
                        
                        # Run each sub-staions
                        for each_input_box in self.input_boxes:
                            if each_input_box.check():
                                self.input_box = each_input_box
                                self.total_distance = self.input_box.getValue() - self.total_distance
                                print("\n>> INPUT: {} deg".format(self.total_distance))

                                self.runSimulation()
                        # ***For now fire***
                        self.end()
                        # ******************
                        self.run_simu = False
                        self.input_boxes[0].able = True
                    # Reset
                    if event.key == pg.K_r:
                        self.reset()
                # Exit Program
                if event.type == pg.QUIT or not self.run:
                    self.run = False
                    pg.quit()

            # CLOCK.tick(FPS)

    def check(self):
        check = [0, False] # [Are all values sorted?, Are all value is None?]
        for each_input_box in self.input_boxes:
            if each_input_box.check():
                # warping the radial position
                while each_input_box.getValue() <= check[0]: # case [30,60,90,75]
                    each_input_box.warp()
                check[0] = each_input_box.getValue()
                check[1] = each_input_box.check()
        return check[1]
    
    def init_simu(self):
        # set initial value
        self.alpha = self.alpha_limit       # rad/s^2
        self.omega = 0.0                    # rad/s
        self.timer = 0                      # frame
        # circular rotational overflow
        # self.theta[0] %= 360            # deg
        # self.total_distance %= 360      # deg
        
        self.theta[1] = self.theta[0]
        # calculate for total time ues and maximum velocity
        #  omega_max = sqrt(2*alpha*theta)
        self.omega_max = math.sqrt(self.alpha*DtoR(self.total_distance))
        #  time = sqrt(2*theta/alpha)
        self.total_time = FPS *math.sqrt(DtoR(self.total_distance)/self.alpha)
        # set points of time for change acceleration
        self.critical_time = (int(self.total_time), int(self.total_time))
        self.total_time *= 2 # increase + decrease period

        # # Requirement
        if self.omega_max > self.omega_limit:
            # set maximum velocity limit
            self.omega_max = self.omega_limit
            # calculate critical points
            critical_pos = RtoD((self.omega_max**2)/self.alpha/2) # (this is 62.8 deg)
            stable_dis = self.total_distance - 2*critical_pos # deg
            middle_time = DtoR(stable_dis) / self.omega_max * FPS # frame
            # set new critical time
            self.critical_time = (int(self.omega_max/self.alpha*FPS), int(self.omega_max/self.alpha*FPS + middle_time))
            # set new total time
            self.total_time = int(2*self.omega_max/self.alpha*FPS + middle_time)

        screen.blit(IMAGE['BACKGROUND'], (0, 0))

    def runSimulation(self):
        self.init_simu()
        # print("\n===== Simulation =====")
        # print("initial position: {:.2f} deg".format(self.theta[1]))
        self.run_simu = True
        
        while self.run_simu:
            # draw simulation
            screen.blit(IMAGE['BACKGROUND_L'], (0, 0))
            screen.blit(FONT(22).render("Simulation process", True, COLOR['ORANGE']), (20, 20))

            for each_input_box in self.input_boxes:
                each_input_box.draw(0)
            self.drawTarget()
            self.drive(1)
            self.drawEndEffector()
            # if self.theta[0] > 360: 
            #     screen.blit(FONT(18).render("({:6.2f} deg)".format(self.theta[0]-360), True, COLOR['WHITE']), (350, 50))
            self.timer += 1
            # plotting graph
            self.plotTheta(1)
            self.plotOmega()
            self.plotAlpha()

            self.drawTime(1)
            pg.display.update()
        # Event
            # End Simulation
            if self.timer >= self.total_time:
                # print("final position  : {:.2f} deg".format(self.theta[0]))
                self.drive(-1)
                self.drawEndEffector()
                self.plotTheta(-1)
                self.total_distance = self.input_box.getValue()

                print(".\n.\n{} took {:.2f} s\n.\n.".format(self.input_box.name, self.total_time/FPS))
                self.global_time += self.timer/FPS  # s
                
                self.wait()
                self.run_simu = False

            for event in pg.event.get():
                # Exit Program
                if event.type == pg.QUIT:
                    self.run_simu = False
                    self.run = False
                    pg.quit()
                # Reset
                if event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self.reset()

            CLOCK.tick(FPS)

    def drive(self, mode=0):
        self.link_length = [self.radius*math.cos(DtoR(self.theta[0])), self.radius*math.sin(DtoR(self.theta[0]))]
        # Mode:1
        if mode == 1:
            # last phase
            if self.timer == max(self.critical_time):
                # print("<max velocity idel:{:.3f} / real:{:.3f} / set:{:.3f}>".format(self.omega_max, self.omega, 2*self.omega_max - self.omega))
                self.omega = 2*self.omega_max - self.omega # for reduce sampling time error **
                self.alpha = -self.alpha_limit
            # middle phase
            elif self.timer == min(self.critical_time): # reach middle way for constant velocity
                self.omega = self.omega_max
                self.alpha = 0
            
            self.omega += self.alpha/FPS
            self.theta[0] += RtoD(self.omega)/FPS # deg/s * s/frame
                    
        # Mode:-1
        elif mode == -1:
            self.theta[0] = self.input_box.getValue()
        
        # End-effector current/final position
        self.end_effector = [self.center[0] + self.link_length[0], self.center[1] + self.link_length[1]]
    
    def drawTarget(self):
        for i, each_input_box in enumerate(self.input_boxes):
            if each_input_box.check():
                link_length_target = [self.radius*math.cos(DtoR(each_input_box.getValue())), self.radius*math.sin(DtoR(each_input_box.getValue()))]
                screen.blit(IMAGE['TARGET'][i], (self.center[0] + link_length_target[0] -40, self.center[1] + link_length_target[1] -40))
    
    def drawEndEffector(self, linkstyle=8):
        # screen.blit(FONT(18).render("current position: {:6.2f} deg".format(self.theta[0]), True, COLOR['WHITE']), (20, 50))
        
        # draw end-effector
        pg.draw.circle(screen, COLOR['ORANGE'], (int(self.end_effector[0]), int(self.end_effector[1])), 30)
        # draw center
        pg.draw.circle(screen, COLOR['GRAY9'], self.center, 37)
        # draw link
        # (version1)
        # pg.draw.line(screen, COLOR['YELLOW'], self.center, (int(self.end_effector[0]), int(self.end_effector[1])), 30)
        # (version2)
        for i in range(linkstyle+1):
            pg.draw.circle(screen, COLOR['BLACK'], (
                int(self.end_effector[0] -(i/linkstyle)* self.link_length[0]),
                int(self.end_effector[1] -(i/linkstyle)* self.link_length[1])
            ), 20)
        # draw value(theta) display
        text = FONT(20).render("{:6.2f} deg".format(self.theta[0]), True, COLOR['ORANGE'])
        rect = text.get_rect()
        screen.blit(text, (
            int(self.end_effector[0] -.5* self.link_length[0]) - rect[2]//2, 
            int(self.end_effector[1] -.5* self.link_length[1]) - rect[3]//2
        ))

    def drawTime(self, mode=0, x=710, y=670, mode2_time=0):
        # Mode:0 while run()
        if mode == 0:
            screen.blit(FONT(20).render("Total Time:{:6.2f} s".format(self.global_time), True, COLOR['ORANGE']), (25, 650))
            # text = FONT(18).render("Time:{:6.2f} s".format(self.timer/FPS), True, COLOR['GRAY'])
            # rect = text.get_rect()
            # pg.draw.rect(screen, COLOR['BACKGROUND'], (x, y, rect[2], rect[3]))
            # screen.blit(text, (x, y))

        # Mode:1 while runSimulation()
        if mode == 1:
            screen.blit(FONT(20).render("Total Time:{:6.2f} s".format(self.global_time + self.timer/FPS), True, COLOR['ORANGE']), (25, 650))

            text = FONT(18).render("Time:{:6.2f} s".format(self.timer/FPS), True, COLOR['GRAY'])
            rect = text.get_rect()
            pg.draw.rect(screen, COLOR['BACKGROUND'], (x, y, rect[2], rect[3]))
            screen.blit(text, (x, y))
        # Mode:2 while wait()
        elif mode == 2:
            text = FONT(20).render("Total Time:{:6.2f} s".format(self.global_time + mode2_time), True, COLOR['ORANGE'])
            rect = text.get_rect()
            pg.draw.rect(screen, COLOR['BACKGROUND'], (25, 650, rect[2], rect[3]))
            screen.blit(text, (25, 650))
            # pg.display.update((25, 650, rect[2], rect[3]))
    
    def plotTheta(self, mode=0, begin=(656,640), scale=(240,110)): # begin: origin(x,y), scale: (width,height)
        # (vertion2)
        pg.draw.circle(screen, COLOR['ORANGE'], (begin[0] + int(self.timer/self.total_time*scale[0]), 
        begin[1] - int((self.theta[0]-self.theta[1])/self.total_distance*scale[1])), 3)
        # (vertion1)
        # Mode:1
        # if mode == 1:
        #     self.theta_plot.append((0,0))
        #     self.theta_plot.append((int(self.timer/self.total_time * scale[0]), int((self.theta[0]-self.theta[1])/self.total_distance * scale[1])))
        # for xy in self.theta_plot:
        #     pg.draw.circle(screen, COLOR['ORANGE'], (xy[0]+begin[0], -xy[1]+begin[1]), 3)

        # Mode:-1 reach final position
        if mode == -1:
            text = FONT(18).render("{:4.2f} rad".format(DtoR(self.theta[0])), True, COLOR['ORANGE'])
            screen.blit(text, (begin[0]+scale[0]+10, begin[1]-scale[1]-10))
    
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

        # reach Omega max
        if self.alpha <= 0:
            text = FONT(18).render("{:.3f} rad/s".format(self.omega_max), True, COLOR['BLUE'])
            rect = text.get_rect()
            pg.draw.rect(screen, COLOR['BACKGROUND'], (begin[0]+scale[0]//3+5, begin[1]-scale[1]-25, rect[2], rect[3]))
            screen.blit(text, (begin[0]+scale[0]//3+5, begin[1]-scale[1]-25))

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

        # positive constant alpha
        if self.alpha > 0:
            text = FONT(18).render("{:.1f} rad/s^2".format(self.alpha), True, COLOR['RED'])
            rect = text.get_rect()
            pg.draw.rect(screen, COLOR['BACKGROUND'], (begin[0]+10, begin[1]-scale[1]//2+10, rect[2], rect[3]))
            screen.blit(text, (begin[0]+10, begin[1]-scale[1]//2+10))
        # negative constant alpha
        elif self.alpha < 0:
            text = FONT(18).render("{:.1f} rad/s^2".format(self.alpha), True, COLOR['RED'])
            rect = text.get_rect()
            pg.draw.rect(screen, COLOR['BACKGROUND'], (begin[0]+scale[0]//2, begin[1]+scale[1]//2-10-rect[3], rect[2], rect[3]))
            screen.blit(text, (begin[0]+scale[0]//2, begin[1]+scale[1]//2-10-rect[3]))

    def reset(self):
        print("\n>> RESET")
        for each_input_box in self.input_boxes:
            each_input_box.reset()
        self.input_boxes[0].able = True

        self.alpha = self.alpha_limit   # rad/s^2
        self.omega = 0.0                # rad/s
        self.theta = [0.0, 0.0]         # [current,initial] deg ***

        self.init()
        self.drive(0)
        self.run_simu = False

    def wait(self, wait_ms=5000, mode=1, begin=(30, 640)):
        print(">> WAIT {:.1f} s".format(wait_ms/1000))

        current_time = 0
        time_stamp = pg.time.get_ticks() # in milliseconds
        run = True
        while (pg.time.get_ticks() - time_stamp < wait_ms) and run:
            current_time = (pg.time.get_ticks() - time_stamp)/ 1000 # in second
            # draw simulation
            screen.blit(IMAGE['BACKGROUND_L'], (0, 0))
            screen.blit(FONT(22).render("Waiting process", True, COLOR['ORANGE']), (20, 20))

            for each_input_box in self.input_boxes:
                each_input_box.draw(0)
            self.drawTarget()
            self.drawEndEffector()
            self.drawTime(mode=2, mode2_time=current_time)
            # draw wait display
            time_left = int(wait_ms//1000 - current_time//1)
            for n in range(time_left):
                pg.draw.circle(screen, COLOR['ORANGE'], (begin[0] + (n*15), begin[1]), 5)
            #
            # Wait for end-effector working
            #
            if mode == 1: pg.display.update()
            for event in pg.event.get():
                # Exit Program
                if event.type == pg.QUIT:
                    self.run_simu = False
                    self.run = False
                    pg.quit()
                # Reset
                if event.type == pg.KEYDOWN and event.key == pg.K_r:
                    run = False
                    print("\n>> RESET")
                    self.reset()
            # CLOCK.tick(FPS)
        if run:
            self.global_time += current_time
            print(">> DONE")

    def end(self):
        pg.image.save(screen, 'screenshot.png')
        end_screen = pg.image.load('screenshot.png')
        screen.blit(end_screen, (0,0))
        fade = pg.Surface((winx,winy))
        fade.fill(COLOR['BLACK'])
        fade.set_alpha(100)
        screen.blit(fade, (0,0))
        text = FONT(24).render("Press any key to Rerun", True, COLOR['GRAY'])
        rect = text.get_rect()
        screen.blit(text, (winx//2 - rect[2]-20, winy//2 - rect[3]//2))
        pg.display.update()

        run = True
        while run:
            #
            # Wait for end-effector working
            #
            for event in pg.event.get():
                # Exit Program
                if event.type == pg.QUIT:
                    self.run_simu = False
                    self.run = False
                    pg.quit()
                # Reset
                if event.type == pg.KEYDOWN:
                    run = False
                    print("\n>> RESET")
                    self.reset()

input_station3 = InputBox('Station 4', x=474, y=714)
input_station2 = InputBox('Station 3', x=324, y=714, next_box=input_station3)
input_station1 = InputBox('Station 2', x=174, y=714, next_box=input_station2)
input_station0 = InputBox('Station 1', x= 24, y=714, next_box=input_station1, default=True)
input_list = [input_station0, input_station1, input_station2, input_station3]

Simulation = Simulation(input_list, max_rpm=10)
Simulation.run()