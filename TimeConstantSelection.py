# Module3 (FRA262) Group10 Time Contant Selection

import math
from matplotlib import colors
def RtoD(radian): return radian*180/math.pi
def DtoR(degree): return degree/180*math.pi

import matplotlib.pyplot as plt
import numpy as np

EX_distance = np.array([
    2.0*math.pi,
    1.9*math.pi,
    1.8*math.pi,
    1.7*math.pi,
    1.6*math.pi,
    1.5*math.pi,
    1.4*math.pi,
    1.3*math.pi,
    1.2*math.pi,
    1.1*math.pi,
    1.0*math.pi,
    0.9*math.pi,
    0.8*math.pi,
    0.7*math.pi,
    0.6*math.pi,
    0.5*math.pi,
    0.4*math.pi,
    0.3*math.pi,
    0.2*math.pi,
    0.1*math.pi,
    0.05*math.pi,
    0.02*math.pi,
    0.01*math.pi,
    0.005*math.pi
])

EX_distance_label = np.array([
    '2.0pi',
    '1.9pi',
    '1.8pi',
    '1.7pi',
    '1.6pi',
    '1.5pi',
    '1.4pi',
    '1.3pi',
    '1.2pi',
    '1.1pi',
    '1.0pi',
    '0.9pi',
    '0.8pi',
    '0.7pi',
    '0.6pi',
    '0.5pi',
    '0.4pi',
    '0.3pi',
    '0.2pi',
    '0.1pi',
    '0'
])

EX_Tk_v_max = np.array([
    9.55,
    9.15,
    8.74,
    8.33,
    7.91,
    7.48,
    7.04,
    6.60,
    6.16,
    5.70
])

EX_Tk_a_max = np.array([
    6.08,
    5.82,
    5.55,
    5.26,
    4.96,
    4.64,
    4.30,
    3.921,
    3.509,
    3.038,
    2.480,
    1.754,
    1.240,
    0.785,
    0.555,
    0.3921
])

Vmax = 10/30*math.pi *0.95 # rad/s (95%)

def findTk_byVmax(s, v=Vmax):
    return (-16*v + math.sqrt((16*v)**2 + 120*0.4*s)) / (2*0.4)
    # return 1.35*s +1.2
Find_Tk_v_max = np.array([])
for s in np.append(EX_distance, [0]):
    Find_Tk_v_max = np.append(Find_Tk_v_max, [findTk_byVmax(s)])

Find_Tk_v_max_1 = np.array([])
for s in np.append(EX_distance, [0]):
    Find_Tk_v_max_1 = np.append(Find_Tk_v_max_1, [findTk_byVmax(s, 8/30*math.pi *0.95)])

Find_Tk_v_max_2 = np.array([])
for s in np.append(EX_distance, [0]):
    Find_Tk_v_max_2 = np.append(Find_Tk_v_max_2, [findTk_byVmax(s, 5/30*math.pi *0.95)])

# print(findTk_byVmax(1.15*math.pi))

def findTk_byAmax(s): 
    return 3.1973371480945967*s**.5
    # return 3.2805403796777592*s**.48
Find_Tk_a_max = np.array([])
for s in np.append(EX_distance, [0]):
    Find_Tk_a_max = np.append(Find_Tk_a_max, [findTk_byAmax(s)])

# print(findTk_byAmax(math.pi))

# plt.figure('Time Constant Selection', figsize=[12.4, 7.6])
fig, ax = plt.subplots()
fig.set_size_inches(12.4, 7.6)
plt.title('Time Constant Selection')
plt.grid(True)

# Tk from v_max 
# plt.plot(EX_distance[:len(EX_Tk_v_max)], EX_Tk_v_max, 'o:', color='teal')
plt.plot(np.append(EX_distance, [0]), Find_Tk_v_max, 'teal')
plt.plot(np.append(EX_distance, [0]), Find_Tk_v_max_1, 'lightseagreen')
plt.plot(np.append(EX_distance, [0]), Find_Tk_v_max_2, 'darkturquoise')
# Tk from a_max
# plt.plot(EX_distance[-len(EX_Tk_a_max):], EX_Tk_a_max, 'o:', color='crimson')
plt.plot(np.append(EX_distance, [0]), Find_Tk_a_max, 'crimson')

# print(len(Find_Tk_v_max), len(Find_Tk_a_max))
temp1 = np.array([])
for i,a in enumerate(Find_Tk_a_max): 
    if a-Find_Tk_v_max[i]>0: temp1 = np.append(temp1, [a])
    else: temp1 = np.append(temp1, [Find_Tk_v_max[i]])
temp2 = np.array([])
for i,a in enumerate(Find_Tk_a_max): 
    if a-Find_Tk_v_max_1[i]>0: temp2 = np.append(temp2, [a])
    else: temp2 = np.append(temp2, [Find_Tk_v_max_1[i]])
temp3 = np.array([])
for i,a in enumerate(Find_Tk_a_max): 
    if a-Find_Tk_v_max_2[i]>0: temp3 = np.append(temp3, [a])
    else: temp3 = np.append(temp3, [Find_Tk_v_max_2[i]])

ax.fill_between(np.append(EX_distance, [0]), temp1, 10, 
facecolor='teal', alpha=0.1)
ax.fill_between(np.append(EX_distance, [0]), temp2, 10, 
facecolor='lightseagreen', alpha=0.1)
ax.fill_between(np.append(EX_distance, [0]), temp3, 10, 
facecolor='darkturquoise', alpha=0.1)
# ax.fill_between(np.append(EX_distance, [0]), Find_Tk_a_max, 10, 
# facecolor='crimson', alpha=0.1)

plt.xticks(np.append(EX_distance[:-4], [0]), labels=EX_distance_label)
plt.yticks(np.append(EX_Tk_v_max[:-1], EX_Tk_a_max[1:]))
plt.xlabel('Distance [rad]')
plt.ylabel('Tk [s]')
plt.axis([0, 2*math.pi, 0, 10])
plt.legend([
    'Tk from v_max (10rpm)',
    'Tk from v_max (8rpm)',
    'Tk from v_max (5rpm)',
    'Tk from a_max'], 
bbox_to_anchor =(0.26, 0.99), ncol = 1)

plt.show()