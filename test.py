# import time
# import sys

# toolbar_width = 40

# # setup toolbar
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

# for i in range(toolbar_width):
#     time.sleep(0.1) # do real work here
#     # update the bar
#     sys.stdout.write("-")
#     sys.stdout.flush()

# sys.stdout.write("]\n") # this ends the progress bar

# from time import sleep
# from tqdm import tqdm
# for i in tqdm(range(0, 100)):
#     sleep(0.1)

# import numpy as np
# time = np.array([0])
# time.append(1)
# print(time)

# for i in range(1):
#     print("hel")

import math
# print('T0=', 3.1973371480945967*(math.pi)**.5)
# print('K0=', 5.667132540783528 / (math.pi**.5))
# print('K1=', 5.667132540783528 / (180**.5))
# print('T1=', 0.42240311995643554*(180)**.5)
s = 360
print(0.0235619449019234492884698253746*s + 1.2)
s = s/180*math.pi
print(1.35*s +1.2)