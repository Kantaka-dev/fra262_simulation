# Module3 (FRA262) Simulation Plot using matlab

import math
def RtoD(radian): return radian*180/math.pi
def DtoR(degree): return degree/180*math.pi

import matplotlib.pyplot as plt
import numpy as np

class SimulationPlot:
	def __init__(self):
		self.time  = np.array([])    # ms
		self.alpha = np.array([])    # rad/2^2
		self.omega = np.array([])    # rad/s
		self.theta = np.array([])    # rad

	def run(self):
		# Setup --------------------------------------------------
		self.distance = 120								# deg
		self.distance = DtoR(self.distance)				# rad
		
		self.alpha_limit = 0.5							# rad/s^2
		self.omega_limit = 10                       	# rpm
		self.omega_limit = self.omega_limit/30*math.pi  # rad/s
		# assume that the acceleration is constant
		# v^2 = u^2 + 2as
		omega_max = math.sqrt(0 + 2*self.alpha_limit*self.distance/2)
		
		if omega_max < self.omega_limit:
			self.runTime(5000, 1)
		
		# self.t_max = 5000            				# ms
		
		self.plot()

	def runTime(self, t_total, mode, t_sampling=10):
		# Mode:1
		if mode==1:
			print("running mode:1")
			for t_ms in range(0, t_total+1, t_sampling): 
				self.time  = np.append(self.time,  [t_ms])
				self.alpha = np.append(self.alpha, [0.5])
				self.omega = np.append(self.omega, [0.5 * (t_ms/1000)])
				self.theta = np.append(self.theta, [0.25 * (t_ms/1000)**2])
		# Mode:0 
		elif mode==0:
			print("running mode:0")
			for t_ms in range(0, t_total+1, t_sampling): 
				self.time  = np.append(self.time,  [t_ms])
				self.alpha = np.append(self.alpha, [0])
				self.omega = np.append(self.omega, [self.omega[-1]])
				self.theta = np.append(self.theta, [0.25 * (t_ms/1000)**2])

	def plot(self):
		plt.plot(self.time, self.alpha, 'r')
		plt.plot(self.time, self.omega, 'b')
		plt.plot(self.time, self.theta, 'g')

		plt.grid(True)

		# plt.xlim([0, 5000])
		# plt.xticks(np.arange(0, t_max+1, step=100))
		plt.xlabel('time [ms]')
		plt.legend(['alpha','omega','theta'])
		plt.show()

graph = SimulationPlot()
graph.run()
