# Module3 (FRA262) Simulation Plot using matlab

import math
def RtoD(radian): return radian*180/math.pi
def DtoR(degree): return degree/180*math.pi

import matplotlib.pyplot as plt
import numpy as np

def printCol(l):
    for i in l: print(i)

omega_limit = 10                        # rpm
omega_limit = omega_limit/30*math.pi    # rad/s

time  = np.array([])    # ms
alpha = np.array([])    # rad/2^2
omega = np.array([])    # rad/s
theta = np.array([])    # rad

t_max = 5000            # ms
for t_ms in range(0, t_max+1, 10): # 0s to t_max s by 0.01s step
    time  = np.append(time,  [t_ms])
    alpha = np.append(alpha, [0.5])
    omega = np.append(omega, [0.5 * (t_ms/1000)])
    theta = np.append(theta, [0.25 * (t_ms/1000)**2])

# print(time)

plt.plot(time, alpha, 'r')
plt.plot(time, omega, 'b')
plt.plot(time, theta, 'g')

plt.grid(True)

plt.xlim([0, t_max])
# plt.xticks(np.arange(0, t_max+1, step=100))
plt.xlabel('time [ms]')
plt.legend(['alpha','omega','theta'])
plt.show()