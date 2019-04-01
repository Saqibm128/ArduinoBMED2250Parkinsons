import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time, sys
from ttylReader import readDataAsyncProcess

reader, p = readDataAsyncProcess()


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r')

def plotAccelToFall(dfBack, dfAngVelBack, dfThigh, dfAngThigh):
    accelTotal = (dfBack['X'] ** 2 + dfBack['Y'] ** 2 + dfBack['Z'] ** 2) ** 0.5
    angVelBackTotal = (dfAngBack['X'] ** 2 + dfAngBack['Y'] ** 2 + dfAngBack['Z'] ** 2) ** 0.5
    angVelThighTotal = (dfAngThigh['X'] ** 2 + dfAngThigh['Y'] ** 2 + dfAngThigh['Z'] ** 2) ** 0.5
    accelThigh =(dfThigh['X'] ** 2 + dfThigh['Y'] ** 2 + dfThigh['Z'] ** 2) ** 0.5

    isMoving = ((accelTotal.rolling(10).max() - accelTotal.rolling(10).min()) > 4) &\
         ((accelThigh.rolling(10).max() - accelThigh.rolling(10).min()) > 4) & \
         ((angVelBackTotal.rolling(10).max() - angVelBackTotal.rolling(10).min()) > 60 / 360 * 2 * np.pi) &\
         ((angVelThighTotal.rolling(10).max() - angVelThighTotal.rolling(10).min()) > 60 / 360 * 2 * np.pi)

    isIntentionalAccel = (accelThigh > 9.8 * 1.05 & accelTotal > 9.8 * 1.05)
    isIntentionalAngVel = (angVelThighTotal.rolling(10).mean() > np.radians(340))
    isIntentional = isIntentionalAccel & isIntentionalAngVel

    anglesBack = dfBack['Z'].copy()
    anglesBack[anglesBack > 9.8] = 9.8
    anglesBack[anglesBack < -9.8] = -9.8
    anglesBack = anglesBack / 9.8
    anglesBack = np.degrees(np.arcsin(anglesBack))

    anglesThigh = dfThigh['Z'].copy()
    anglesThigh[anglesThigh > 9.8] = 9.8
    anglesThigh[anglesThigh < -9.8] = -9.8
    anglesThigh = anglesThigh / 9.8
    anglesThigh = np.degrees(np.arcsin(anglesThigh))

    isStanding = (anglesThigh > 35) & (anglesBack > 35) #we really gotta fix the sample rate

    t = np.arange(0, anglesThigh.shape[0]/10 + 0.1, 0.1)

    fig, ax1 = plt.subplots()
    ax1.plot(t, anglesBack, 'b-')
    ax1.set_xlabel('time (s)')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Back Angle (degrees)', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(t, isMoving & isStanding.shift(0) & (isIntentionalAccel | isIntentionalAngVel), 'r')
    ax2.set_ylabel('Fall Detection', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.title("Simulated Fall Detection")
    plt.show()

def init():
    ax.set_xlim(0,100)
    ax.set_ylim(-30, 90)
    return ln,

def update(frame):
    # print(reader.getData())
    data = reader.getData()['x'].iloc[-100:]
    # print(data)
    # print(np.arcsin(data/3833))

    data = np.degrees(np.arcsin(((data)/8500)))
    # print(data.index)
    xdata = np.arange(100 if len(data) > 100 else len(data))
    ydata = data.values
    # print(ydata)
    ln.set_data(xdata, ydata)
    return (ln,)

ani = FuncAnimation(fig, update,
                    frames=np.linspace(0, 2*np.pi, 2),
                    init_func=init)
plt.show()
reader.getData().to_csv("data/single_sensor_{}.csv".format(time.time()))

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
