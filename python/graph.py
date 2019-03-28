import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from ttylReader import TTYLReader

fig, ax = plt.subplots()

maxX = 100

x = np.arange(0, maxX)
reader = TTYLReader("/dev/ttyS5", debug=False)
p = reader.readDataAsyncProcess()
time.sleep(4)
p.terminate()
# print(reader.getData())
print(reader.data)
# plt.plot(reader.getData())
# plt.show()
# time.sleep(3)
# line, = ax.plot(np.arange(maxX), [np.nan] * maxX)
#
#
#
# def init():  # only required for blitting to give a clean slate.
#     line.set_ydata([np.nan] * maxX)
#     return line,
#
#
# def animate(i):
#     data = reader.getData()
#     line.set_xdata(data.index)
#     line.set_ydata(data["yaw"])  # update the data.
#     return line,
#
#
# ani = animation.FuncAnimation(
#     fig, animate, init_func=init, interval=2, blit=True, save_count=50)
#
# # To save the animation, use e.g.
# #
# # ani.save("movie.mp4")
# #
# # or
# #
# # from matplotlib.animation import FFMpegWriter
# # writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# # ani.save("movie.mp4", writer=writer)
#
# plt.show()
# p.terminate()
# print(reader.getData()["yaw"].iloc[:-maxX])
