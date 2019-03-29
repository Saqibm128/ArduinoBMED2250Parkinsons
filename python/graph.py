import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time, sys
from ttylReader import readDataAsyncProcess

reader, p = readDataAsyncProcess()
time.sleep(3)


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

def init():
    ax.set_xlim(0,100)
    ax.set_ylim(-30, 180)
    return ln,

def update(frame):
    data = reader.getData()['x'].iloc[-100:]
    data = np.degrees(np.arcsin(data/3833))
    print(data.max())
    xdata = np.arange(100)
    ydata = data.values
    ln.set_data(xdata, ydata)
    return (ln,)

ani = FuncAnimation(fig, update,
                    frames=np.linspace(0, 2*np.pi, 2),
                    init_func=init,
                    blit=True,)
plt.show()

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# from matplotlib.animation import FFMpegWriter
# writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

# fig.show()

p.terminate()
