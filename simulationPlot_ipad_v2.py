# Module3 (FRA262) Simulation Plot using matlab

import math
def RtoD(radian): return radian*180/math.pi
def DtoR(degree): return degree/180*math.pi

import matplotlib.pyplot as plt
import numpy as np

class SimulationPlot:
	def __init__(self):
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
		# set goal
		self.setGoal(2/2*math.pi)
		
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
			for time in self.time:
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
			for time in self.time:
				self.fAlpha(time, mode_warp=True)
				self.fOmega(time, mode_warp=True)
				self.fTheta(time, mode_warp=True)
		
		self.plot()
	
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
		
		plt.show()

sim = SimulationPlot()
sim.sim()
