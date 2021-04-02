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

import numpy as np
time = np.array([0])
time.append(1)
print(time)