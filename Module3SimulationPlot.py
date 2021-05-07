# Module3 (FRA262) Group10 Simulation Plot using Pygame, Matlab

import math
def RtoD(radian): return radian*180/math.pi
def DtoR(degree): return degree/180*math.pi

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

class SimulationPlot: # Simulation("Station [n]", [m] rad)
	def __init__(self, name, goal):
		self.name = name
		self.goal = goal

		self.alpha = np.array([])
		self.omega = np.array([])
		self.theta = np.array([])
	
	def setGoal(self, final_position, init_position=0):
		self.distance = final_position-init_position
	
	def setParameter(self, alpha_limit=0.5, omega_limit=(10/30*math.pi)):
		# set maximum acceleration default at 0.5rad/s^2
		self.alpha_limit = alpha_limit
		# set maximum velocity default at 10rpm
		self.omega_limit = omega_limit
	
	def sim(self, sampling=0.01):
		print("\n[ Start Plotting Simulation ]")

		# set goal
		self.setGoal(self.goal)
		
		# set Constant
		self.setParameter()
		
		# find maximum velocity
		self.w_max = math.sqrt(self.alpha_limit*self.distance)
		
		# max velocity <= 10rpm
		if self.w_max <= self.omega_limit:
			# find half way time
			self.t_half = math.sqrt(self.distance/self.alpha_limit)
			
			# set sampling time
			self.time = np.arange(0, self.t_half*2, sampling)
			print("\n> start calculation")
			for time in tqdm(self.time, desc='calculating'):
				self.fAlpha(time)
				self.fOmega(time)
				self.fTheta(time)
			
		# max velocity > 10rpm
		elif self.w_max > self.omega_limit:
			# find critical positions (2arrays)
			self.theta_cri = (
				self.omega_limit**2 /2/self.alpha_limit,
				self.distance - self.omega_limit**2 /2/self.alpha_limit
			)
			#print("critical pos", self.theta_cri)
			# find critical time points (2arrays)
			self.t_cri = (
				self.omega_limit/self.alpha_limit,
				(self.theta_cri[1]-self.theta_cri[0])/self.omega_limit + self.omega_limit/self.alpha_limit
			)
			#print("critical time", self.t_cri)
			# set sampling time
			self.time = np.arange(0, self.t_cri[0]+self.t_cri[1], sampling)
			print("\n> start calculation")
			for time in tqdm(self.time, desc='calculating'):
				self.fAlpha(time, mode_warp=True)
				self.fOmega(time, mode_warp=True)
				self.fTheta(time, mode_warp=True)
		
		# self.plot()	
		print("\n[ End Plotting Simulation ]")
			
	def fAlpha(self, time, mode_warp=False):
		# max velocity <= 10rpm
		if not mode_warp:
			# time <= t_half
			if time <= self.t_half:
				self.alpha = np.append(self.alpha, [self.alpha_limit])
			# time > t_half
			else:
				self.alpha = np.append(self.alpha, [-self.alpha_limit])
			
		# max velocity > 10rpm
		else:
			# time <= t_cri[0]
			if time <= self.t_cri[0]:
				self.alpha = np.append(self.alpha, [self.alpha_limit])
			# t_cri[0] < time <= t_cri[1]
			elif self.t_cri[0] < time <= self.t_cri[1]:
				self.alpha = np.append(self.alpha, [0])
			# t_cri[1] < time
			else:
				self.alpha = np.append(self.alpha, [-self.alpha_limit])
	
	def fOmega(self, time, mode_warp=False):
		# max velocity <= 10rpm
		if not mode_warp:
			# time <= t_half
			if time <= self.t_half:
				self.omega = np.append(self.omega, [self.alpha_limit*time])
			# time > t_half
			else:
				self.omega = np.append(self.omega, [self.w_max-self.alpha_limit*(time-self.t_half)])
			
		# max velocity > 10rpm
		else:
			# time <= t_cri[0]
			if time <= self.t_cri[0]:
				self.omega = np.append(self.omega, [self.alpha_limit*time])
			# t_cri[0] < time <= t_cri[1]
			elif self.t_cri[0] < time <= self.t_cri[1]:
				self.omega = np.append(self.omega, [self.omega_limit])
			# t_cri[1] < time
			else:
				self.omega = np.append(self.omega, [self.omega_limit - self.alpha_limit*(time-self.t_cri[1])])
	
	def fTheta(self, time, mode_warp=False):
		# max velocity <= 10rpm
		if not mode_warp:
			# time <= t_half
			if time <= self.t_half:
				self.theta = np.append(self.theta, [0.5*self.alpha_limit*time**2])
			# time > t_half
			else:
				self.theta = np.append(self.theta, [self.w_max*(time-self.t_half) - 0.5*self.alpha_limit*(time-self.t_half)**2 + self.distance/2])
			
		# max velocity > 10rpm
		else:
			# time <= t_cri[0]
			if time <= self.t_cri[0]:
				self.theta = np.append(self.theta, [0.5*self.alpha_limit*time**2])
			# t_cri[0] < time <= t_cri[1]
			elif self.t_cri[0] < time <= self.t_cri[1]:
				self.theta = np.append(self.theta, [self.omega_limit*(time-self.t_cri[0]) + self.theta_cri[0]])
			# t_cri[1] < time
			else:
				self.theta = np.append(self.theta, [self.omega_limit*(time-self.t_cri[1]) - 0.5*self.alpha_limit*(time-self.t_cri[1])**2 + self.theta_cri[1]])
	
	def plot(self):
		plt.figure('Plotting Simulation', figsize=[6.4, 7.6], facecolor=(0.176,0.192,0.235))
		ax = plt.axes()
		ax.set_facecolor((0.125,0.133,0.160))

		# plot alpha-time
		plt.subplot(311)
		plt.title('input distance : {:.1f} deg ({:.3f} rad)'.format(RtoD(self.distance), self.distance))
		
		plt.plot(self.time, self.alpha, 'r')
		plt.grid(True)
		plt.ylabel('alpha [rad/s^2]', color='r')
		plt.yticks([-self.alpha_limit, 0, self.alpha_limit], color='r')
		plt.xticks(np.append(np.arange(0, max(self.time)-0.5, 0.5), [max(self.time)]), '')
		
		# plot omega-time
		plt.subplot(312)
		plt.plot(self.time, self.omega, 'b')
		plt.grid(True)
		plt.ylabel('omega [rad/s]', color='b')
		plt.yticks(np.append(np.arange(0, max(self.omega)-0.25, 0.25), [max(self.omega)]), color='b')
		plt.xticks(np.append(np.arange(0, max(self.time)-0.5, 0.5), [max(self.time)]), '')
		
		# plot theta-time
		plt.subplot(313)
		plt.plot(self.time, self.theta, 'g')
		plt.grid(True)
		plt.ylabel('theta [rad]', color='g')
		plt.yticks(np.append(np.arange(0, max(self.theta)-0.5, 0.5), [max(self.theta)]), color='g')
		plt.xlabel('time [s]')
		plt.xticks(np.append(np.arange(0, max(self.time)-0.5, 0.5), [max(self.time)]))
		
		print("\n> show plot...")
		plt.show()

	def getData(self, command):
		if 		command=='name': return self.name
		elif 	command=='goal': return self.goal

import pygame as pg
pg.init()
pg.display.set_caption('Module3 Group10 Simulation')
pg.display.set_icon(pg.image.load('data/fibo_icon.jpg'))

CLOCK = pg.time.Clock()
FPS = 25	# frames/second
			# and calculation sampling time will be 1/FPS

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
def FONT(size): return pg.font.SysFont('couriernew', size, bold=True)

winx, winy = 1024, 768
screen = pg.display.set_mode((winx, winy))

class InputBox:
	def __init__(self, name, unit, x, y, next_box=None, scale=180, length=6, default=False):
		self.name = name
		self.unit = unit
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
		screen.blit(FONT(18).render(self.name, True, COLOR['WHITE'],), (self.x+12, self.y-30))
		# draw unit
		screen.blit(FONT(18).render("[{}]".format(self.unit), True, COLOR['GRAY'],), (self.x+self.w+10, self.y+10))
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
		# self.able = False

	def warp(self):
		self.value = str(float(self.value) + 360)

class Simulation:
	def __init__(self, input_list):
		self.input_list = input_list  # [0]position
		# queue and history
		self.next_input = []	# class <SimulationPlot> in <list>
								# add by append
		self.data = [] 			# class <SimulationPlot> in <list>
								# add by inset(0)
		self.queue = Queue()	# class <Queue>
		self.queue_count = 1	# set initial count is Station "1"
		# self-state
		self.state = 'STANDBY'	# set default state is STANDBY > DRIVE > WAIT
		# drawing parameters
		self.center = (330, 384)# pixels
		self.radius = 250       # pixels

	def run(self):
		self.run = True

		while self.run:
			# Draw background
			screen.fill(COLOR['BLACK'])
			screen.blit(IMAGE['BACKGROUND_L'], (0, 0))

			# Self-Draw
			self.draw()
			self.drawTarget()
			# Draw InputBox
			for input_box in self.input_list:
				input_box.draw()
			# Draw Queue
			self.queue.draw()

			pg.display.update()
            # Event
			for event in pg.event.get():

				# InputBox
				for input_box in self.input_list:
					input_box.handleEvent(event)
				
				# Press [Enter]
				if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.check():

					# for n in self.next_input:
					# 	print(RtoD(n.getData('goal')))

					self.next_input.append(
						SimulationPlot('to Station '+str(self.queue_count), DtoR(self.input_list[0].getValue()))
					)
					self.queue.update(self.next_input, self.data)
					self.queue_count += 1
					self.input_list[0].reset()  # reset input position box value

                # Exit Program
				if event.type == pg.QUIT or not self.run:
					self.run = False
					pg.quit()

			CLOCK.tick(FPS)
	
	def draw(self):
		# state STANDBY : wait for next inputs
		if self.state == 'STANDBY':
			if len(self.next_input) >0:			# has new inputs
				# calculate the input
				next_input = self.next_input.pop(0)
				next_input.sim(1/FPS)			# set sampling time by FPS
				# and store the data
				self.data.insert(0, next_input)
				# change state STANDBY => DRIVE
				self.state = 'DRIVE'

		# state DRIVE : draw motion of machine
		elif self.state == 'DRIVE':
			pass

		# state WAIT : wait end-effector 5 second
		elif self.state == 'WAIT':
			pass
	
	def drawTarget(self):
		c = len(self.next_input)
		if c>3: c=3
		for i in range(c):
			draw_x = self.center[0]-40 + self.radius*math.cos(self.next_input[i].getData('goal'))
			draw_y = self.center[1]-40 + self.radius*math.sin(self.next_input[i].getData('goal'))
			IMAGE['TARGET'][i].set_alpha(255 - (i*100))
			screen.blit(IMAGE['TARGET'][i], (draw_x, draw_y))
	# def drawTarget(self):
    #     for i, each_input_box in enumerate(self.input_boxes):
    #         if each_input_box.check():
    #             link_length_target = [self.radius*math.cos(DtoR(each_input_box.getValue())), self.radius*math.sin(DtoR(each_input_box.getValue()))]
    #             screen.blit(IMAGE['TARGET'][i], (self.center[0] + link_length_target[0] -40, self.center[1] + link_length_target[1] -40))

	def check(self):
		return True if self.input_list[0].check() and len(self.next_input)<9 else False
	
class Queue:
	def __init__(self):
		self.x = 660
		self.y = -15 # >= -self.h/10
		self.w =   0
		self.h = 560

		self.next_input = []
		self.data = []
		self.dummy = [SimulationPlot('Start', 0)]
		self.all = self.dummy

	def update(self, next_input, data):
		self.next_input = next_input
		self.data = data
		self.all = next_input[::-1] + data + self.dummy

	def draw(self):
		# check that all data is more than 10 or not
		start = 0
		idx = 0
		if len(self.all) < 10:
			start += 10-len(self.all)
		
		# draw
		txt_color = [COLOR['GRAY3'], COLOR['GRAY3']]
		for i in range(start, 10):
			# each element class <SimulationPlot> in self.all
			element = self.all[idx]
			# draw name
			screen.blit(FONT(20).render(element.getData('name'), True, txt_color[0],), (
				self.x, self.y+self.h-(self.h//10) * i)
			)
			# draw goal
			screen.blit(FONT(18).render("[{:6.2f} deg]".format(RtoD(element.getData('goal'))), True, txt_color[1],), (
				self.x+160, self.y+self.h-(self.h//10) * i)
			)
			idx += 1
			# change font's color
			if i == start+len(self.next_input) -1:
				txt_color = [COLOR['WHITE'], COLOR['GRAY2']]

Simulation = Simulation(
	[InputBox('Input Position', 'deg', x=700, y=650, default=True)]
)
Simulation.run()